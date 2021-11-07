import requests
from lxml import html
import json


def find_recipe_data(url):
    r = requests.get(url)
    assert r.encoding == "utf8", "Encoding of returned data was incorrect - utf8 required!"

    tree = html.fromstring(r.text)

    recipe_json = {
        "rating": None,
        "recipe": None
    }

    for structured_data in tree.xpath('//script[contains(@type, "application/ld+json")]'):
        text = structured_data.text_content()
        if '"@type":"Recipe"' in text:
            recipe_json["recipe"] = json.loads(text)
        elif '"@type":"AggregateRating"' in text:
            recipe_json["rating"] = {
                "score": None,
                "reviews": None,
            }
            recipe_json["rating"]["score"] = float(json.loads(text)["aggregateRating"]["ratingValue"])
            recipe_json["rating"]["reviews"] = int(json.loads(text)["aggregateRating"]["reviewCount"])

    assert recipe_json["recipe"] is not None, "Could not locate recipe in \"application/ld+json\" format!"
    assert recipe_json["rating"] is not None, "Could not locate rating in \"application/ld+json\" format!"

    print(json.dumps(recipe_json, indent=3))

    return recipe_json


def find_recipies_bbcgoodfood():
    root_url = "https://www.bbcgoodfood.com/"

    quick_recipe_url = "https://www.bbcgoodfood.com/search/recipes?q=Quick+recipes"

    r = requests.get(quick_recipe_url)

    tree = html.fromstring(r.text)
    tree.xpath()



if __name__ == "__main__":
    find_recipe_data("https://www.bbcgoodfood.com/recipes/sponge-cake")