from flask import Blueprint, render_template, request, jsonify

home_page = Blueprint('home_page', __name__)


@home_page.route('/', methods=['GET'])
def display():
    """
    View function for displaying the home page.
    Output:
       Rendered HTML page.
    """

    # products = product_catalog.list_products()

    return render_template('index.html')
