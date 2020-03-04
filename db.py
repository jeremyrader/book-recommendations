import sqlite3

def connect():
    print('creating db')
    conn=sqlite3.connect("recommendations.db")
    cur=conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS product (id INTEGER PRIMARY KEY, url text, imgSrc text, title text, description text, addedBy text)")
    cur.execute("CREATE TABLE IF NOT EXISTS review (id INTEGER PRIMARY KEY, productId INTEGER, review text, addedBy text, FOREIGN KEY(productId) REFERENCES product(id))")
    
    conn.commit()
    conn.close()

def insertProduct(url, imgSrc, title, description, userId):
    print(imgSrc)
    print(title)
    print(description)
    print(userId)
    print(url)
    conn=sqlite3.connect("recommendations.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO product VALUES (NULL,?,?,?,?,?)", (url, imgSrc, title, description, userId))
    conn.commit()
    conn.close()

def getAllProducts():
    conn=sqlite3.connect("recommendations.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM product")
    rows=cur.fetchall()
    conn.close()
    return rows

def getProductById(productId):
    conn=sqlite3.connect("recommendations.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM product WHERE id = ?", (productId,))
    rows=cur.fetchone()
    conn.close()
    return rows

def insertReview(productId, review, userId):
    conn=sqlite3.connect("recommendations.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO review VALUES (NULL,?,?,?)", (productId, review, userId))
    conn.commit()
    conn.close()

def getAllReviewsByProductId(productId):
    conn=sqlite3.connect("recommendations.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM review WHERE productId = ?", (productId,))
    rows=cur.fetchall()
    conn.close()
    return rows
