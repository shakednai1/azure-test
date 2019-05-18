import mysql.connector
from mysql.connector import errorcode
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

# Obtain connection string information from the portal



# Construct connection string
try:
    conn = mysql.connector.connect(user="shaked@shaked-test-db", password="Aa123456",
                                  host="shaked-test-db.mysql.database.azure.com", port=3306, database="search-history")
    print("Connection established")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with the user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = conn.cursor()

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


if __name__ == "__main__":
	app.run()