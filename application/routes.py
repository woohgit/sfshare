from flask import current_app as app, render_template, request
from flask import jsonify
import os
from . import zkill_share


@app.template_filter()
def calculate_tax(price):
    # the price is always 20%
    tax = price * 0.20
    return tax

@app.template_filter()
def calculate_price(price, involved):
    tax = calculate_tax(price)
    return (price - tax) / involved

@app.template_filter()
def currency(amount):
    return "{:,.0f}".format(round(int(amount), 2))


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/', methods=['GET'])
def index():
    version = os.getenv("GIT_SHA")
    zkill_link = request.args.get("zkill_link")
    error_message = None

    if zkill_link is not None:
        try:
            buy, sell = zkill_share.get_buy_sell_from_appraisal(zkill_link)
        except Exception as e:
            buy, sell = None
            error_message = "Error while parsing the input. (%s)" % str(e)

    else:
        buy, sell = None

    return render_template('index.html',
                           zkill_link=request.args.get("zkill_link", ""),
                           buy=buy,
                           sell=sell,
                           error_message=error_message,
                           version=version)
