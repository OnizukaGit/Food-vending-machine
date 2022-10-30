from flask import Flask,request,render_template,redirect,url_for
from psycopg2 import connect,ProgrammingError
from sql_utils import execute_sql

app = Flask(__name__)


def show_product_sql(cursor_prodcut):
    SHOW_PRODUCT = "SELECT name,price FROM Product"
    cursor_prodcut.execute(SHOW_PRODUCT)


def get_product_sql(cursor_get_product,name):
    GET_PRODUCT = "select * from product where name=%s "
    cursor_get_product.execute(GET_PRODUCT,(name,))


def buy_product_sql(cursor_buy_product,price):
    BUY_PRODUCT = "select * from product where price=%s "
    cursor_buy_product.execute(BUY_PRODUCT,(price,))


@app.route("/", methods=["GET","POST"])
def show_get_buy_product_start_page():
    if request.method == "GET":
        cnx = connect(host="localhost", password="coderslab", user="postgres", database="snack_machine")
        cnx.autocommit = True
        cursor = cnx.cursor()
        show_product_sql(cursor)
        show = cursor.fetchall()
        cnx.close()
        cursor.close()
        return render_template("start_page.html", show=show)
    elif request.method == "POST":
        get = request.form.get("get")
        cnx = connect(host="localhost", password="coderslab", user="postgres", database="snack_machine")
        cnx.autocommit = True
        cursor = cnx.cursor()
        get_product_sql(cursor,get)
        get = cursor.fetchone()
        cnx.close()
        cursor.close()
        return render_template("get_product.html", item=get)


@app.route("/admin", methods=["GET","POST"])
def admin_panel():
    if request.method == "GET":
        return render_template("admin_panel.html")
    else:
        password = request.form.get("password")
        if password == "admin":
            return render_template("select.html")
        else:
            pass


@app.route("/choose", methods=["GET","POST"])
def choose_panel():
    if request.method == "GET":
        return render_template("select.html")
    else:
        add_product = request.form.get("add_product")
        delete_product = request.form.get("delete_product")
        if add_product:
            return render_template("add.html")
        elif delete_product:
            return render_template("delete.html")


def add_product_sql(add_product,name,price):
    ADD_PRODUCT ="""insert into product (name, price)
            values (%s, %s)"""
    values = (name,price)
    add_product.execute(ADD_PRODUCT,values)


@app.route("/add", methods=["GET", "POST"])
def add_panel():
    if request.method == "GET":
        return render_template("add.html")
    else:
        product = request.form.get("product")
        price = request.form.get("price")
        cnx = connect(host="localhost", password="coderslab", user="postgres", database="snack_machine")
        cnx.autocommit = True
        cursor = cnx.cursor()
        if product is None:
            return "Błąd"
        else:
            add_product_sql(cursor,product,price)
    return redirect(url_for('show_get_buy_product_start_page'))


def delete_product_sql(cursor, name):
    DELETE_PRODUCT_SQL= "delete from product where name=%s"
    cursor.execute(DELETE_PRODUCT_SQL, (name,))

def delete_product_ID(cursor, name):
    DELETE_PRODUCT_SQL= "delete from product where id=%s"
    cursor.execute(DELETE_PRODUCT_SQL, (name,))

@app.route("/delete", methods=["GET","POST"])
def delete_product():
    if request.method == "GET":
        return render_template("delete.html")
    else:
        delete = request.form.get("delete")
        cnx = connect(host="localhost", password="coderslab", user="postgres", database="snack_machine")
        cnx.autocommit = True
        cursor = cnx.cursor()
        if delete is None:
            return "Błąd"
        else:
            delete_product_sql(cursor,delete)
            cnx.close()
            cursor.close()
        return redirect(url_for('show_get_buy_product_start_page'))


@app.route("/get", methods=["GET","POST"])
def buy_product():
    if request.method == "GET":
        return render_template("get_product.html")
    else:
        cash = float(request.form.get("cash"))
        price = float(request.form.get("price"))
        get = request.form.get("get")

        if cash < price:
            return "Błąd: wpłacono za mało gotówki"
        else:
            cnx = connect(host="localhost", password="coderslab", user="postgres", database="snack_machine")
            cnx.autocommit = True
            cursor = cnx.cursor()
            delete_product_sql(cursor, get)
        reszta = cash - price
        cnx.close()
        cursor.close()
        return render_template("end.html", bilon=reszta)

if __name__ == "__main__":
    app.run(port=5001)