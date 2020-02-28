from flask import Flask, request, jsonify
from flask_cors import CORS
import db
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as gRequest

app=Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/")
def index():
    return jsonify({
        "author": "Jeremy Rader",
        "project": "Zennify Recommendations"
    })

@app.route("/product", methods=["POST", "GET"])
def product():
    if request.method == "GET":

        productId = request.args.get('id', '')
        product = db.getProductById(productId)

        return jsonify({
            "id": product[0],
            "url": product[1],
            "imgSrc": product[2],
            "title": product[3]
        })

    if request.method == "POST":

        URL = "http://api.linkpreview.net"
        search = request.args.get('url', '')
        userId = request.args.get('userName', '')

        PARAMS = {'q': search, 'key': '5e420e68bcc55aeb243b18dbf50afe1a0ca7968c319d5'} 

        r = requests.get(url = URL, params = PARAMS) 

        data = r.json()

        db.insertProduct(data["url"], data["image"], data["description"], userId)

        return jsonify({
            "url": data["url"],
            "imgSrc": data["image"],
            "title": data["description"]
        })

@app.route("/products")
def products():

    def keymap(product):
        return {
            "id": product[0],
            "url": product[1],
            "imgSrc": product[2],
            "title": product[3],
            "userId": product[4]
        }

    return jsonify(list(map(keymap, db.getAllProducts())))

@app.route("/review", methods=["POST"])
def review():
    if request.method == "POST":

        productId = request.args.get('id', '')
        review = request.args.get('review', '')
        userId = request.args.get('userName', '')

        db.insertReview(productId, review, userId)

        return jsonify({
            "id": productId,
            "review": review,
        })

@app.route("/reviews")
def reviews():

    productId = request.args.get('id', '')

    return jsonify(db.getAllReviewsByProductId(productId))

@app.route('/auth', methods=['POST'])
def auth():
    token = request.args.get('token', '')

    CLIENT_ID = '833516466041-7dcqaf16fqn9qln34is6g0at9emdj3sb.apps.googleusercontent.com'

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, gRequest.Request(), CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        GSUITE_DOMAIN_NAME = 'zennify.com'

        # If auth request is from a G Suite domain:
        if 'hd' not in idinfo or idinfo['hd'] != GSUITE_DOMAIN_NAME:
            raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']

        return jsonify({'authorized': True})

    except ValueError:
        return jsonify({'authorized': False})


if __name__=="__main__":
    app.run(debug=True)