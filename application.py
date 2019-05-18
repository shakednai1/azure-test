import requests
import pyodbc
from flask import Flask, render_template, request
from azure.cognitiveservices.search.websearch import WebSearchAPI
from msrest.authentication import CognitiveServicesCredentials

app = Flask(__name__)

# bing search client connection
subscription_key = "2e702b743ba744a6be5948828d355d6b"
client = WebSearchAPI(CognitiveServicesCredentials(subscription_key))

# sql database connection
server = 'db-shaked-test.database.windows.net'
database = 'db-shaked-test'
username = 'shaked@db-shaked-test'
password = 'Aa123456'
driver= '{ODBC Driver 13 for SQL Server}'
# import pdb; pdb.set_trace()
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='
                                                                   ''+database+';UID='+username+';PWD='+ password)
print('The cnection is workkkkkk' + cnxn)
# cursor = cnxn.cursor()
# cursor.execute("SELECT * from search_history")
# all = cursor.fetchall()
# import pdb; pdb.set_trace()


def search_insta(val):
    web_data = client.web.search(query=val)
    for web_page in web_data.web_pages.value:
        if web_page.url.startswith("https://www.instagram.com/"):
            return web_page.url


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/search")
def search():
    # TODO : find in data base - if not exist search from bing
    to_search = request.args.get('value', 0)
    res = search_insta(to_search)
    return res

# if __name__ == "__main__":
# 	app.run()