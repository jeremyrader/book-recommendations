from flask import Flask, request, jsonify
from flask_cors import CORS
import db
import requests

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

    return jsonify(list(map(keymap, db.getAllProducts())))

@app.route("/review", methods=["POST"])
def review():
    if request.method == "POST":

        productId = request.args.get('id', '')
        review = request.args.get('review', '')

        db.insertReview(productId, review)

        return jsonify({
            "id": productId,
            "review": review,
        })

@app.route("/reviews")
def reviews():

    productId = request.args.get('id', '')

    return jsonify(db.getAllReviewsByProductId(productId))

if __name__=="__main__":
    app.run(debug=True)