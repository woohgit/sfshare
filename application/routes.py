from flask import current_app as app, render_template, request
from flask import jsonify
import os
from . import zkill_share


@app.template_filter()
def calculate_tax(price):
    # the price is always 20%
    tax = price * 0.20
    return round(tax)

@app.template_filter()
def calculate_price(price, involved):
    tax = calculate_tax(price)
    return round((price - tax) / involved)

@app.template_filter()
def currency(amount):
    return "{:,.0f}".format(round(int(amount), 2))


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/', methods=['GET', 'POST'])
def index():
    version = os.getenv("GIT_SHA")
    error_message = None
    zkill_links = None
    results = []
    if request.method == 'POST':
        zkill_links = request.form["zkill_links"]

    if zkill_links is not None:
        links = zkill_links.splitlines()
        for link in links:
            try:
                if link:
                    buy, sell = zkill_share.get_buy_sell_from_appraisal(link)
                    results.append({"link": link, "buy": buy, "sell": sell, "error": None})
                else:
                    continue
            except Exception as e:
                error_message = "Error while parsing the input. (%s) for URL %s" % (str(e), link)
                results.append({"link": link, "buy": None, "sell": None, "error": error_message})

    return render_template('index.html',
                           zkill_links=zkill_links,
                           results=results,
                           error_message=error_message,
                           version=version)
