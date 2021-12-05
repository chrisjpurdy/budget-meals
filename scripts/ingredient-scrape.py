from lxml import html
from mongo_api import save_ingredient_to_db
from playwright.sync_api import sync_playwright

def convert_tesco_ingredient(ingredient_element, i):
    # Ingredient object template
    ingredient = {
        "name": None,
        "price": None,
        "pricePerUnit": None,
        "unit": None,
        "url": None,
        "imgUrl": None
    }

    title = ingredient_element.xpath("//a[contains(@data-auto, 'product-tile--title')]")
    ingredient["name"] = title[i].text_content()
    ingredient["url"] = title[i].get("href")

    price = ingredient_element.xpath("//div[contains(@class, 'price-per-sellable-unit')]//span[contains(@data-auto, 'price-value')]")
    ingredient["price"] = price[i].text_content()

    price_per_unit = ingredient_element.xpath("//div[contains(@class, 'price-per-quantity-weight')]//span[contains(@data-auto, 'price-value')]")
    ingredient["pricePer"] = price_per_unit[i].text_content()

    unit = ingredient_element.xpath("//div[contains(@class, 'price-per-quantity-weight')]//span[contains(@class, 'weight')]")
    ingredient["unit"] = unit[i].text_content()

    image = ingredient_element.xpath("//div[contains(@class, 'product-image__container')]/img")
    ingredient["imgUrl"] = image[i].get("src")

    #print("Ingredient scraped: ", end="")
    #print(ingredient)

    return ingredient


def tesco_playwright_scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.tesco.com/groceries/en-GB/shop/fresh-food/all")

        tree = html.document_fromstring(page.content())
        ingredients = [convert_tesco_ingredient(val, i) for i, val in enumerate(tree.find_class("product-tile"))]
        browser.close()
        return ingredients


if __name__ == '__main__':
    for ingredient in tesco_playwright_scrape():
        save_ingredient_to_db(ingredient)
