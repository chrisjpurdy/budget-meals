import requests
import json

API_KEY = "gi8655avHrN3ZW5Ph31v99PzEsL4Noh6Dr9uklsOrVe4D9Qw08mtt8CCXzw91Ofy"

ENDPOINT = "https://data.mongodb-api.com/app/data-elech/endpoint/data/beta"

def save_ingredient_to_db(ingredient):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": API_KEY
    }
    response = requests.post(ENDPOINT + "/action/insertOne", headers=headers, json={
        "dataSource": "Recipes",
        "database": "ScrapedData",
        "collection": "Ingredients",
        "document": ingredient
    })
    # check that x is an ok response

