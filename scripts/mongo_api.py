import requests
import json

API_KEY = "jWXbi4nWZuRWar0RJ7nLsGg8nvxZsOdXg8OpH5gHUDGMbunm93hwIzemiLJpDkWV"

ENDPOINT = "https://data.mongodb-api.com/app/data-elech/endpoint/data/beta"

def save_ingredient_to_db(ingredient):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": API_KEY
    }
    response = requests.post(ENDPOINT + "/action/insertOne", headers=headers, json={
        "dataSource": "ScrapedData",
        "database": "Ingredients",
        "collection": "Tesco",
        "document": ingredient
    })
    print(response.text)
    print(response.reason)
    # check that x is an ok response


def save_ingredients_to_db(ingredients):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": API_KEY
    }
    response = requests.post(ENDPOINT + "/action/insertMany", headers=headers, json={
        "dataSource": "ScrapedData",
        "database": "Ingredients",
        "collection": "Tesco",
        "documents": ingredients
    })
    # check that x is an ok response