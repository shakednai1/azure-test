from flask import Flask, render_template
from azure.cognitiveservices.search.websearch import WebSearchAPI
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials

app = Flask(__name__)

subscription_key = "2e702b743ba744a6be5948828d355d6b"
client = WebSearchAPI(CognitiveServicesCredentials(subscription_key))

def search():
    web_data = client.web.search(query="Beyonce")
    for web_page in web_data.web_pages.value:
        if web_page.url.startswith("https://www.instagram.com/"):
            return web_page.url

@app.route("/")
def hello():
    return render_template("index.html")

