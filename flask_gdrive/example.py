from flask import Flask
from flask_gdrive import GDriveStatic
import markdown

app = Flask(__name__)
gs = GDriveStatic(app, 'flask_gdrive', 'credentials.json')

app.route("/gstatic/<fpath>")(gs.fileHandler)

@app.route("/")
def home():
    result = gs.fileHandler("Blank.md")[0].decode()
    html = markdown.markdown(result)
    print(gs.g_url_for("1a5.jpg"))
    return html, 200


app.run(debug=True)