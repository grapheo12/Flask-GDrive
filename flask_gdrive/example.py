from flask import Flask
from flask_gdrive import GDriveStatic, GDriveDB
import markdown

app = Flask(__name__)
gs = GDriveStatic(app, 'credentials.json', 'token.pickle', 'flask_gdrive')
db_arr = {
    "user": "1m6ypUXZa4KFR3XLtHWnyz-I6h3TZY5WdrDBgYcLOAc8"
}
db = GDriveDB(app, 'credentials.json', 'token.pickle', db_arr)
app.route("/gstatic/<fpath>")(gs.fileHandler)

@app.route("/")
def home():
    result = gs.fileHandler("Blank.md")[0].decode()
    html = markdown.markdown(result)
    print(gs.g_url_for("1a5.jpg"))
    print(db.gdrive_db)
    db.gdrive_db["user"][0][0] = 'bird'
    new_row = ["hati", 200, 100, " jvncvk hkty]-pl87hg"]
    db.gdrive_db["user"].append(new_row)
    db.update("user")
    return html, 200


app.run(debug=True)