from lxml import html
from playwright.sync_api import sync_playwright

def convert_tesco_ingredient(ingredient_element):
    # Ingredient object template
    ingredient = {
        "name": None,
        "price": None,
        "pricePerUnit": None,
        "unit": None,
        "url": None,
        "imgUrl": None
    }

    title = ingredient_element.xpath("//a[contains(@data-auto, 'product-title--title')]")
    ingredient["name"] = title.text_content()
    ingredient["url"] = title.get("href")

    price = ingredient_element.xpath("//div[contains(@class, 'price-per-sellable-unit')]//span[contains(@data-auto, 'price-value')]")
    ingredient["price"] = price.text_content()

    price_per_unit = ingredient_element.xpath("//div[contains(@class, 'price-per-quantity-weight')]//span[contains(@data-auto, 'price-value')]")
    ingredient["pricePer"] = price_per_unit.text_content()

    unit = ingredient_element.xpath("//div[contains(@class, 'price-per-quantity-weight')]//span[contains(@class, 'weight')]")
    ingredient["unit"] = unit.text_content()

    image = ingredient_element.xpath("//div[contains(@class, 'product-image__container')]/img")
    ingredient["imgUrl"] = image.get("src")

    print("Ingredient scraped: ", end="")
    print(ingredient)

    return ingredient


def tesco_fresh_ingredient_scrape():

    #s = Session()

    cookies = {"ADRUM": "s=1637520884911&r=https%3A%2F%2Fwww.tesco.com%2Fgroceries%2Fen-GB%2Fshop%2Ffresh-food%2Fall%3F0"}

    r = Request('GET', )
    #r = s.get(r"https://www.tesco.com/groceries/en-GB/shop/fresh-food/all")
    r = requests.get(r"https://www.tesco.com/groceries/en-GB/shop/fresh-food/all", cookies=cookies)
    print(r.text)

    tree = html.fromstring(r.text)

    ingredients = [convert_tesco_ingredient(i) for i in tree.find_class("product-tile")]


if __name__ == '__main__':
    tesco_fresh_ingredient_scrape()



def tesco_playwright_scrape():

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://playwright.dev")
        print(page.title())
        browser.close()