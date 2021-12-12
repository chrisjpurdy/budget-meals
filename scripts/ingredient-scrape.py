from mongo_api import save_ingredient_to_db, save_ingredients_to_db
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def convert_tesco_ingredient(ingredient_element):
    # Ingredient object template
    ingredient = {
        "name": None,
        "price": None,
        "unit": None,
        "url": None,
        "imgUrl": None
    }

    title = ingredient_element.find(attrs={'data-auto': 'product-tile--title'})
    ingredient["name"] = title.contents[0]
    ingredient["url"] = title["href"]

    price = ingredient_element.find(class_="price-per-sellable-unit").find("span", attrs={'data-auto': 'price-value'})
    ingredient["price"] = price.contents[0]

    price_per_unit = ingredient_element.find(class_="price-per-quantity-weight").find("span", attrs={'data-auto': 'price-value'})
    ingredient["pricePer"] = price_per_unit.contents[0]

    unit = ingredient_element.find(class_="price-per-quantity-weight").find("span", class_="weight")
    ingredient["unit"] = unit.contents[0]

    image = ingredient_element.find(class_="product-image__container").find("img")
    ingredient["imgUrl"] = image["src"]

    def extractPromoData(promotion_li):
        offer = promotion_li.find("span", class_="offer-text").contents[0]
        dates = promotion_li.find("span", class_="dates").contents[0]
        return {
            "offer": offer,
            "dates": dates,

        }

    promotions = ingredient_element.find("ul", class_="product-promotions")
    if (promotions):
        ingredient["promotions"] = list(map(extractPromoData, promotions.find_all("li", class_="product-promotion")))

    return ingredient


def tesco_playwright_scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.tesco.com/groceries/en-GB/shop/fresh-food/all")

        soup = BeautifulSoup(page.content(), features="lxml")
        ingredients = [convert_tesco_ingredient(product) for product in soup.find_all("div", class_="product-tile")]
        browser.close()
        return ingredients


if __name__ == '__main__':
    ingredients = tesco_playwright_scrape()
    #print(ingredients[0])
    #save_ingredient_to_db(ingredients[0])
    save_ingredients_to_db(ingredients)
