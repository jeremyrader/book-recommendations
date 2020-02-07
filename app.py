from flask import Flask, request
import db

app=Flask(__name__)

@app.route("/")
def index():
    return {
        "author": "Jeremy Rader",
        "project": "Zennify Recommendations"
    }

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

        url = request.args.get('url', '')
        imgSrc = request.args.get('imgSrc', '')
        title = request.args.get('title', '')

        db.insertProduct(url, imgSrc, title)

        return {
            "url": url,
            "imgSrc": imgSrc,
            "title": title
        }

@app.route("/products")
def products():
    return {
        "products": db.getAllProducts()
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

if __name__=="__main__":
    app.run(debug=True)