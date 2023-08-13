from flask import Flask , render_template , redirect ,  request
import random
import string
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__ ,template_folder="template")
app.app_context().push()
basedir = os.path.abspath(os.path.dirname(__file__))

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Init db
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short = db.Column(db.String)
    long = db.Column(db.String)

    def __int__(self, short=short, long=long):
        self.short = short
        self.long = long




    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'short': self.short,
            'long': self.long,
        }


shortened_url = {}

def generate_short_url(length = 6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url


@app.route("/" , methods=['GET' , 'POST'])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = generate_short_url()
        url = Users(short = short_url , long = long_url)
        db.session.add(url)
        db.session.commit()
        while short_url in shortened_url:
            short_url = generate_short_url()

        shortened_url[short_url] = long_url
        return f"Shortened Url: {request.url_root}{short_url}"
    return render_template("index.html")


@app.route("/<short_url>")
def redirect_url(short_url):
    print(short_url)
    s = db.session.query(Users).filter(Users.short == short_url).first()
    if s.long:
        return redirect(s.long)
    else:
        " URL not found"



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0" )