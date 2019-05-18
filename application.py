import pyodbc
from flask import Flask, render_template, request
from azure.cognitiveservices.search.websearch import WebSearchAPI
from msrest.authentication import CognitiveServicesCredentials

app = Flask(__name__)

# bing search client connection
subscription_key = "2e702b743ba744a6be5948828d355d6b"
client = WebSearchAPI(CognitiveServicesCredentials(subscription_key))

# sql database connection
# server = 'db-shaked-test.database.windows.net,1443'
# database = 'db-shaked-test'
# username = 'shaked@db-shaked-test'
# password = 'Aa123456'
# driver = '{SQL Server}'
cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:db-shaked-test.database.windows.net,1433;"
                      "Database=db-shaked-test;Uid=shaked@db-shaked-test;Pwd=Aa123456;"
                      "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30")
cursor = cnxn.cursor()

def search_insta(val):
    web_data = client.web.search(query=val)
    for web_page in web_data.web_pages.value:
        if web_page.url.startswith("https://www.instagram.com/"):
            return web_page.url

# def get_result_from_db(to_search):
#     cursor.execute("SELECT * from dbo.search_history where search_name = '{}'".format(to_search))
#     all = cursor.fetchone()
#     return all[1]

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/search")
def search():
    to_search = request.args.get('value', 0)
    res = search_insta(to_search)
    return res

# @app.route("/search")
# def search():
#     to_search = request.args.get('value', 0)
#     try:
#         res = get_result_from_db(to_search)
#     except:
#         res = search_insta(to_search)
#     return res


# if __name__ == "__main__":
# 	app.run()