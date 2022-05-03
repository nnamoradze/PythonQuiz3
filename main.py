import json
import sqlite3
import requests

BASE_URL = "https://fedeperin-harry-potter-api-en.herokuapp.com/db"

response = requests.get(BASE_URL)

# print(response.text)
# print(response.headers)
# print(response.status_code)            # <---პირველი საკითხი
# print(response.content)

apiData = response.json()

json_file = open("json_file.json", "w")
json.dump(response.json(), json_file, indent=4)  # <---მეორე საკითხი

connection = sqlite3.connect("harry_potter.sqlite3")
cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE if not exists spells(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, usages TEXT)")  # <---ვქმნი მონაცემთა ბაზას
cursor.execute(
    "CREATE TABLE if not exists characters(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, house TEXT, image_url TEXT)")
cursor.execute(
    "CREATE TABLE if not exists books(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, description TEXT)")

data_of_spells = apiData["spells"]
data_of_characters = apiData["characters"]
data_of_books = apiData["books"]

spells = apiData["spells"]
for spell in range(len(spells)):
    spell_item_name = data_of_spells[spell]["spell"]
    spell_item_usage = data_of_spells[spell]["use"]
    cursor.execute("INSERT INTO spells (name,usages) VALUES (?,?)",
                   (spell_item_name,
                    spell_item_usage,))  # <---მონაცემთა ბაზაში შემაქვს api-დან წამოღებული შელოცვები და მისი გამოყენებები
    connection.commit()

characters = apiData["characters"]
for character in range(len(characters)):
    character_item_name = data_of_characters[character]["character"]
    house_item_usage = data_of_characters[character]["hogwartsHouse"]
    image_item_url = data_of_characters[character]["image"]
    cursor.execute("INSERT INTO characters (name, house, image_url) VALUES (?,?,?)",
                   (character_item_name, house_item_usage,
                    image_item_url,))  # <---მონაცემთა ბაზაში შემაქვს api-დან წამოღებული პერსონაჟების ინფორმაციები
    connection.commit()

books = apiData["books"]
for book in range(len(books)):
    book_item_title = data_of_books[book]["title"]
    book_item_author = data_of_books[book]["author"]
    book_item_description = data_of_books[book]["description"]
    cursor.execute("INSERT INTO books (title,author,description) VALUES (?,?,?)",
                   # <---მონაცემთა ბაზაში შემაქვს api-დან წამოღებული წიგნების შესახებ ინფორმაცია
                   (book_item_title, book_item_author, book_item_description,))
    connection.commit()
