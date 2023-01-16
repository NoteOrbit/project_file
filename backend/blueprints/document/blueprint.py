from flask import Blueprint, render_template, request, jsonify

doc_page = Blueprint('doc_page', __name__)


@doc_page.route('/doc_page', methods=['GET'])
def display():
    """
    View function for displaying the home page.
    Output:
       Rendered HTML page.
    """

    # products = product_catalog.list_products()

    return render_template('document_api.html')
