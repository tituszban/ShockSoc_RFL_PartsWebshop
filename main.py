from flask import Flask, render_template, redirect, url_for, request
from random import randint
import math
import json
app = Flask(__name__)

transactions = {}

stock = {
        "000": {"description": "Brushless Outrunner and 30A ESC", "qty": 2, "price": 15},
        "100": {"description": "Brushed Motor 2 Pack", "qty": 10, "price": 3},
        "200": {"description": "Brushed ESC 20A", "qty": 10, "price": 4.5},
        "400": {"description": "XT60U 5 Pairs", "qty": 5, "price": 3.5}
    }


def format_money(m):
    whole = math.floor(m)
    decimal = math.floor((m - whole) * 100)
    decimal = '00' if decimal == 0 else str(decimal)
    return("£%d.%s" % (whole, decimal))


def load_stock():
    global stock
    for key in stock.keys():
        stock[key]['disp_price'] = format_money(stock[key]['price'])


def new_session_id():
    id = randint(10000000, 99999999)
    if id in transactions.keys():
        return new_session_id()
    return id


@app.route('/details/<int:transaction_id>')
def details(transaction_id):
    return render_template('details.html', transaction_id=transaction_id)


@app.route('/details/<int:transaction_id>', methods=['POST'])
def details_submit(transaction_id):
    name = request.form['name']
    email = request.form['email']
    ssid = request.form['ssid']
    if int(ssid) < 200000000 or name == '' or email == '':
        return redirect(url_for('details', transaction_id=transaction_id))
    transactions[transaction_id]['name'] = name
    transactions[transaction_id]['email'] = email
    transactions[transaction_id]['ssid'] = ssid
    return redirect(url_for('shop', transaction_id=transaction_id))


@app.route('/shop/<int:transaction_id>')
def shop(transaction_id):
    return render_template('shop.html', transaction_id=transaction_id, stock=stock, transaction=transactions[transaction_id])


@app.route('/shop/<int:transaction_id>', methods=['POST'])
def shop_submit(transaction_id):
    keys = [key for key in request.form.keys() if key in stock]
    transactions[transaction_id]['order items'] = {key: {'qty': int(request.form[key]),
                                                         'price': stock[key]['price'] * int(request.form[key]),
                                                         'disp_price': format_money(stock[key]['price'] * int(request.form[key]))}
                                                   for key in keys
                                                   if request.form[key] != '' and request.form[key] != '0'}
    transactions[transaction_id]['sum price'] = format_money(sum([transactions[transaction_id]['order items'][key]['price']
                                                     for key in transactions[transaction_id]['order items'].keys()]))
    if transactions[transaction_id]['order items'] == {}:
        return redirect(url_for('shop', transaction_id=transaction_id))
    return redirect(url_for('review', transaction_id=transaction_id))


@app.route('/review/<int:transaction_id>')
def review(transaction_id):
    return render_template('review.html', transaction_id=transaction_id, stock=stock, transaction=transactions[transaction_id])


@app.route('/review/<int:transaction_id>', methods=['POST'])
def review_submit(transaction_id):
    transactions[transaction_id]['session state'] = 'complete'
    return render_template('reciept.html', transaction_id=transaction_id, stock=stock,
                           transaction=transactions[transaction_id])

@app.route('/new_session')
def new_session():
    transaction_id = new_session_id()
    transactions[transaction_id] = {'session state':'incomplete'}
    return redirect(url_for('details', transaction_id=transaction_id))

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_transactions')
def get_transactions():
    return json.dumps(transactions, ensure_ascii=False)

if __name__ == '__main__':
    load_stock()
    app.run(host='0.0.0.0', debug=True)