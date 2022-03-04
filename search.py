""" utilizes the USDA Food Central API to track calorie and macro consumption """
import requests

##############################################
# REFERS TO A LOCAL FILE HOLDING THE API KEY #
from config import API_KEY                   #
key = f"&api_key={API_KEY}" # REPLACE WITH OWN API KEY     #
##############################################

page_size = "&pageSize="
base_url = "https://api.nal.usda.gov/fdc/v1/foods/"

def search_fc(query, results="10"):
    """ searches the USDA food central API """

    fquery = "%20".join(list(query.split())) # changes "search terms lol" to "search%20terms%20lol"
    url = base_url + "search?query=" + fquery + page_size + results + key
    rq = requests.get(url)

    return rq.json()["foods"]
