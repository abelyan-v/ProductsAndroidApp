from flask import Flask, render_template, request
import mysql.connector
import hashlib
import string
import random

db = mysql.connector.connect(host='localhost',
                            database='products_order',
                            user='root',
                            password='')
cursor = db.cursor()

app = Flask(__name__)


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/products1')
def products():
    userId = 1;
    sql = "SELECT * FROM products"
    cursor.execute(sql)
    sql_response_fetchall = cursor.fetchall()
    print(sql_response_fetchall)
    response = ""
    for item in sql_response_fetchall:
        numberSql = f"SELECT number FROM cart WHERE user_id = {userId} AND product_id = {item[0]}"
        try:
            cursor.execute(numberSql)
            numberSql_response_fetchall = cursor.fetchall()
            number = numberSql_response_fetchall[0][0]
        except:
            number = 0
        response = response + f"{item[0]} {item[1]} {item[2]} {number},"
    response = response[:-1]
    print(response)
    return response

@app.route('/products', methods=['POST'])
def products_output():
    userId = request.form.get("userid");
    sql = "SELECT * FROM products"
    cursor.execute(sql)
    sql_response_fetchall = cursor.fetchall()
    print(sql_response_fetchall)
    response = ""
    for item in sql_response_fetchall:
        numberSql = f"SELECT number FROM cart WHERE user_id = {userId} AND product_id = {item[0]}"
        try:
            cursor.execute(numberSql)
            numberSql_response_fetchall = cursor.fetchall()
            number = numberSql_response_fetchall[0][0]
        except:
            number = 0
        response = response + f"{item[0]} {item[1]} {item[2]} {number},"
    response = response[:-1]
    print(response)
    return response

@app.route('/cart1')
def cart1():
    userId = 1
    sql = f"SELECT product_id,number FROM cart WHERE user_id = {userId}"
    cursor.execute(sql)
    sql_response_fetchall = cursor.fetchall()
    response = ""
    for item in sql_response_fetchall:
        sql1 = "SELECT `name`,`price` FROM `products` WHERE 1"
        cursor.execute(sql1)
        sql1_response_fetchall = cursor.fetchall()
        response = response + f"{item[0]} {sql1_response_fetchall[0][0]} {sql1_response_fetchall[0][1]} {item[1]},"
    response = response[:-1]
    return response

@app.route('/cart', methods=['POST'])
def cart():
    userId = request.form.get("userid")
    sql = f"SELECT product_id,number FROM cart WHERE user_id = {userId}"
    cursor.execute(sql)
    sql_response_fetchall = cursor.fetchall()
    response = ""
    for item in sql_response_fetchall:
        sql1 = f"SELECT `name`,`price` FROM `products` WHERE id = {item[0]}"
        cursor.execute(sql1)
        sql1_response_fetchall = cursor.fetchall()
        response = response + f"{item[0]} {sql1_response_fetchall[0][0]} {sql1_response_fetchall[0][1]} {item[1]},"
    response = response[:-1]
    return response

@app.route('/registration', methods=['POST'])
#, methods=['POST']
def registration():
    #one = request.form.get("one");
    username = request.form.get("username")
    first_name = request.form.get("name")
    last_name = request.form.get("lname")
    password = request.form.get("password")
    password_md5 = hashlib.md5(bytes(password, 'utf-8')).hexdigest()
    confirm_password = request.form.get("confirmPassword")
    e_mail = request.form.get("email")
    tel_number = request.form.get("pnumber")
    if (password == confirm_password):
        sql = f"INSERT INTO `users`(`username`, `password`, `first_name`, `last_name`, `e_mail`, `tel_number`) VALUES ('{username}','{password_md5}','{first_name}','{last_name}','{e_mail}','{tel_number}')"
        print(sql)
        cursor.execute(sql)
        db.commit()
        return "Registration"
    else:
        return "Incorrect password confirm"

@app.route('/authorisation', methods=['POST'])
def authorisation():
    username = request.form.get("username")
    password = request.form.get("password")
    print(username)
    print(password)
    password_md5 = hashlib.md5(bytes(password, 'utf-8')).hexdigest()
    sql = f"SELECT * FROM `users` WHERE `username`='{username}'"
    try:
        cursor.execute(sql)
        sql_response_fetchall = cursor.fetchall()
        if (sql_response_fetchall[0][2] == password_md5):
            random_string = generate_random_string(32)
            return f"{sql_response_fetchall[0][0]}"
        else:
            return "incorrect"
    except:
        return "not found"

@app.route('/product_plus', methods=['POST'])
def product_plus():
    user_id = 1
    product_id = request.form.get("id")
    sql = f"SELECT * FROM `cart` WHERE `user_id`={user_id} AND `product_id`={product_id}"
    try:
        cursor.execute(sql)
        sql_response_fetchall = cursor.fetchall()
        sql1 = f"UPDATE `cart` SET `number`='{sql_response_fetchall[0][2] + 1}' WHERE `user_id`={user_id} AND `product_id`={product_id}"
        cursor.execute(sql1)
        db.commit()
        return "updated"
    except:
        sql1 = f"INSERT INTO `cart`(`user_id`, `product_id`, `number`) VALUES ('{user_id}','{product_id}','1')"
        cursor.execute(sql1)
        db.commit()
        return "inserted"

@app.route('/product_minus', methods=['POST'])
def product_minus():
    user_id = 1
    product_id = request.form.get("id")
    sql = f"SELECT * FROM `cart` WHERE `user_id`={user_id} AND `product_id`={product_id}"
    try:
        cursor.execute(sql)
        sql_response_fetchall = cursor.fetchall()
        if (sql_response_fetchall[0][2] != 1):
            sql1 = f"UPDATE `cart` SET `number`='{sql_response_fetchall[0][2] - 1}' WHERE `user_id`={user_id} AND `product_id`={product_id}"
            cursor.execute(sql1)
            db.commit()
            return "updated"
        else:
            sql1 = f"DELETE FROM `cart` WHERE `user_id`={user_id} AND `product_id`={product_id}"
            cursor.execute(sql1)
            db.commit()
            return "deleted"
    except:
        return "nothing"

if __name__ == '__main__':
    app.run(host='0.0.0.0')