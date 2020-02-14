from flask import Flask, redirect, request, url_for
from flask_cors import CORS
import json
import os
import sqlite3
import db
import requests
from oauthlib.oauth2 import WebApplicationClient
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

# Internal imports
from usersdb import init_db_command
from user import User

app=Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = "super secret key"


# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
GOOGLE_CLIENT_ID = '833516466041-7dcqaf16fqn9qln34is6g0at9emdj3sb.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'JZUk2T1e6x2jB4vdtI8mWdsB'
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/")
def index():
    if current_user.is_authenticated:
       return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/product", methods=["POST", "GET"])
def product():
    if request.method == "GET":

        productId = request.args.get('id', '')
        product = db.getProductById(productId)

        return {
            "id": product[0],
            "url": product[1],
            "imgSrc": product[2],
            "title": product[3]
        }

    if request.method == "POST":

        URL = "http://api.linkpreview.net"
        search = request.args.get('url', '')

        PARAMS = {'q': search, 'key': '5e420e68bcc55aeb243b18dbf50afe1a0ca7968c319d5'} 

        r = requests.get(url = URL, params = PARAMS) 

        data = r.json()

        db.insertProduct(data["url"], data["image"], data["description"])
        print(data)
        return {
            "url": data["url"],
            "imgSrc": data["image"],
            "title": data["description"]
        }

@app.route("/products")
def products():

    def keymap(product):
        return {
            "id": product[0],
            "url": product[1],
            "imgSrc": product[2],
            "title": product[3]
        }

    return {
        "products": list(map(keymap, db.getAllProducts()))
    }

@app.route("/review", methods=["POST"])
def review():
    if request.method == "POST":

        productId = request.args.get('id', '')
        review = request.args.get('review', '')

        db.insertReview(productId, review)

        return {
            "id": productId,
            "review": review,
        }

@app.route("/reviews")
def reviews():

    productId = request.args.get('id', '')

    return {
        "reviews": db.getAllReviewsByProductId(productId)
    }

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

if __name__=="__main__":
    app.run(ssl_context="adhoc")