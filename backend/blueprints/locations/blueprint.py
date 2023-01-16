from flask import Blueprint, render_template, request, jsonify
import requests
import json

location_page = Blueprint('location_page', __name__)


@location_page.route('/location_page', methods=['GET'])
def nearbyweb():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    info = requests.get(f'http://127.0.0.1:5000/recomnear?latitude={latitude}&longitude={longitude}')
    posts=info.json()
    
    return render_template('nearby.html', posts=posts)
