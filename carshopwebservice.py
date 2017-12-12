# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template
from flask import g
import sqlite3


app = Flask(__name__)
app.DATABASE = 'carshop.db'

# Utility


def make_dicts(cur, row):
    return dict((cur.description[idx][0], value) for idx, value in enumerate(row))


def exception_handler(e):
    if e.__class__.__name__ == 'KeyError':
        e.value = 'KeyError'

    elif e.__class__.__name__ == 'ValueError':
        e.value = 'ValueError'

    elif e.__class__.__name__ == 'OperationError':
        e.value = 'OperationError'
    else:
        e.value = e.__class__.__name__


def connect_db():
    rv = sqlite3.connect(app.DATABASE)
    rv.row_factory = make_dicts
    return rv


# GET


@app.route("/carmodels", methods=['GET'])
def return_car_models():
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM CarModel')
    carmodels = cur.fetchall()
    g.db.close()
    return jsonify({'carmodels': carmodels})


@app.route('/sales', methods=['GET'])
def return_sales():
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM Sales')
    sales = cur.fetchall()
    g.db.close()
    return jsonify({'sales': sales})


@app.route('/employees')
def return_employees():
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM Employee')
    employees = cur.fetchall()
    g.db.close()
    return jsonify({'employees': employees})


@app.route('/employeesales')
def return_employee_sales():
    g.db = connect_db()
    cur = g.db.execute('SELECT e.id,e.name,e.email, SUM(c.price) AS "sales" FROM Employee e LEFT JOIN Sales s ON e.id = s.employeeId LEFT JOIN CarModel c ON c.id = s.carModelId GROUP BY e.id')
    employeesales = cur.fetchall()
    g.db.close()
    return jsonify({'employeesales': employeesales})

# POST


@app.route("/addcarmodel", methods=['POST'])
def add_car_model():
    try:
        g.db = connect_db()
        data = request.get_json()
        brand = data['brand']
        model = data['model']
        price = data['price']
        cur = g.db.execute("INSERT INTO CarModel (brand, model, price) VALUES (?,?,?)", (brand, model, price))
        g.db.commit()
        cur = g.db.execute('SELECT * FROM CarModel ORDER BY id DESC LIMIT 1;')
        carmodels = cur.fetchall()
        return jsonify({'carmodels': carmodels})
    except Exception as e:
        exception_handler(e)
        return e.value
    finally:
        g.db.close()


@app.route("/addemployee", methods=['POST'])
def add_employee():
    try:
        g.db = connect_db()
        data = request.get_json()
        name = data['name']
        email = data['email']
        print name
        cur = g.db.execute("INSERT INTO Employee (name, email) VALUES (?,?)", (name, email))
        print name
        g.db.commit()
        cur = g.db.execute('SELECT * FROM Employee ORDER BY id DESC LIMIT 1;')
        employees = cur.fetchall()
        return jsonify({'employees': employees})
    except Exception as e:
        exception_handler(e)
        return e.value
    finally:
        g.db.close()

# PUT


@app.route("/updatecarmodel", methods=['PUT'])
def update_car_model():
    try:
        g.db = connect_db()
        data = request.get_json()
        id = data['id']
        brand = data['brand']
        model = data['model']
        price = data['price']
        cur = g.db.execute("Update CarModel SET brand = ?, model = ?, price = ? WHERE id = ?", (brand, model, price, id))
        g.db.commit()
        cur = g.db.execute("SELECT * FROM CarModel WHERE id = ?", (id,))
        carmodel = cur.fetchall()
        return jsonify({'carmodel': carmodel})
    except Exception as e:
        exception_handler(e)
        return e.value
    finally:
        g.db.close()


@app.route("/updateemployee", methods=['PUT'])
def update_employee():
    try:
        g.db = connect_db()
        data = request.get_json()
        id = data['id']
        name = data['name']
        email = data['email']
        cur = g.db.execute("Update Employee SET name = ?, email = ? WHERE id = ?", (name, email, id))
        g.db.commit()
        cur = g.db.execute("SELECT * FROM Employee WHERE id = ?", (id,))
        employees = cur.fetchall()
        return jsonify({'employees': employees})
    except Exception as e:
        exception_handler(e)
        return e.value
    finally:
        g.db.close()


# DELETE


@app.route("/deletecarmodel", methods=['DELETE'])
def delete_car_model():
    try:
        g.db = connect_db()
        data = request.get_json()
        id = data['id']
        cur = g.db.execute("DELETE FROM CarModel WHERE id = ?", (id,))
        g.db.commit()
        cur = g.db.execute("SELECT * FROM CarModel")
        carmodels = cur.fetchall()
        return jsonify({'carmodels': carmodels})
    except Exception as e:
        exception_handler(e)
        return e.value
    finally:
        g.db.close()


@app.route("/deleteemployee", methods=['DELETE'])
def delete_employee():
    try:
        g.db = connect_db()
        data = request.get_json()
        id = data['id']
        cur = g.db.execute("DELETE FROM Employee WHERE id = ?", (id,))
        g.db.commit()
        cur = g.db.execute("SELECT * FROM Employee")
        employees = cur.fetchall()
        return jsonify({'employees': employees})
    except Exception as e:
        exception_handler(e)
        return e.value
    finally:
        g.db.close()

# Application routes


@app.route("/")
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
