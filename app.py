from flask import Flask, request

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

        return {
            "id": productId,
            "url": "test.com",
            "imgSrc": "test.jpg",
            "title": "Test Title"
        }

    if request.method == "POST":

        url = request.args.get('url', '')
        imgSrc = request.args.get('imgSrc', '')
        title = request.args.get('title', '')

        return {
            "url": url,
            "imgSrc": imgSrc,
            "title": title
        }

@app.route("/products")
def products():
    return {
        "products": [
            {
            "id": 1,
            "url": "test.com",
            "imgSrc": "test.jpg",
            "title": "Test Title 1"
            },
            {
            "id": 2,
            "url": "test.com",
            "imgSrc": "test.jpg",
            "title": "Test Title 2"
            },
            {
            "id": 3,
            "url": "test.com",
            "imgSrc": "test.jpg",
            "title": "Test Title 3"
            }
        ]
    }

@app.route("/review", methods=["POST"])
def review():
    if request.method == "POST":

        productId = request.args.get('id', '')
        review = request.args.get('review', '')

        return {
            "id": productId,
            "review": review,
        }

@app.route("/reviews")
def reviews():

    productId = request.args.get('id', '')

    return {
        "reviews": [
            {
            "id": 1,
            "review": "This could be good",
            },
            {
            "id": 2,
            "review": "This could be good",
            },
            {
            "id": 3,
            "review": "This could be good",
            }
        ]
    }

if __name__=="__main__":
    app.run(debug=True)