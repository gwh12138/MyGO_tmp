from flask import Flask, render_template, request, redirect, url_for
import MySQLdb

app = Flask(__name__)
app.config.from_pyfile('config.py')


def get_db_connection():
    return MySQLdb.connect(
        host=app.config['DATABASE']['host'],
        user=app.config['DATABASE']['user'],
        passwd=app.config['DATABASE']['password'],
        db=app.config['DATABASE']['db']
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/resources')
def resources():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM farm_management.farm_resources")
    resources = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('resources.html', resources=resources)


@app.route('/products')
def products():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM farm_management.products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('products.html', products=products)


@app.route('/add_resource', methods=['POST'])
def add_resource():
    name = request.form['name']
    type = request.form['type']
    quantity = request.form['quantity']
    details = request.form['details']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO farm_management.farm_resources (name, type, quantity, details) VALUES (%s, %s, %s, %s)",
                   (name, type, quantity, details))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('resources'))


if __name__ == '__main__':
    app.run(debug=True)
