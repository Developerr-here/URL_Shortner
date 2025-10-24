from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import string,random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///links.db"
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    long_url = db.Column(db.String(300),nullable=False)
    short_url = db.Column(db.String(10),nullable=False)

with app.app_context():
    db.create_all()

# length=6 means the default short code will be 6 characters long (like aB9xD3).
def gen_short(length=6):

#     Creates a pool of characters to choose from:

# string.ascii_letters → all uppercase + lowercase letters (A–Z, a–z)

# string.digits → numbers (0–9)

# So total 62 possible characters for each position.
    characters = string.ascii_letters + string.digits


#     Starts an infinite loop.

# This loop will keep generating new short codes until it finds one that’s not already used.

    while True:


#         Randomly picks length (6) characters from characters.

# random.choices() → picks multiple random elements (with repetition).

# ''.join(...) joins them into a single string.
# Example: "a" + "B" + "9" + "x" + "D" + "3" → "aB9xD3"
        short_url = ''.join(random.choices(characters, k = length))


# Checks your database (table URL) to see if this short code already exists.

# URL.query.filter_by(short_url=short_url).first() → fetches first record that matches.

# if not ... means:

# If it doesn’t exist (unique),

# then return it — break out of the loop.

# This ensures no duplicate short URLs.
        if not URL.query.filter_by(short_url=short_url).first():
            return short_url

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        long_url=request.form.get('long_url')
        short_url = gen_short()
        url = URL(long_url = long_url, short_url = short_url)
        db.session.add(url)
        db.session.commit()


#         After saving, it shows result.html and passes the full shortened link:

# request.host_url = base URL of your app (e.g., http://127.0.0.1:5000/)

# So request.host_url + short_url → complete link like http://127.0.0.1:5000/aB9xD3
        return render_template('result.html',short_url=request.host_url+short_url)
    return render_template('index.html')

@app.route('/<short_url>')
# This defines a dynamic route.

# Example: /aB9xD3 → Flask automatically passes "aB9xD3" into the function as short_url.
def go(short_url):
#     Looks up the database for a record with the same short code.

# If not found, Flask automatically shows a 404 page (Not Found).
    url = URL.query.filter_by(short_url = short_url).first_or_404()

# If the record exists:

# redirect(url.long_url) sends the user to the original long URL.
    if url:
        return redirect(url.long_url)
    return "<h2>url not found</h2>"

    


if __name__ == "__main__":
    app.run()