# -*- coding: utf-8 -*-
from flask import Flask, request, Response
from flask_cors import CORS
import requests

class OpenHABProxy:
    def __init__(self, openhab_base_url):
        self.openhab_base_url = openhab_base_url
        self.app = Flask(__name__)
        CORS(self.app)  # Aktiviere CORS für die Flask-Anwendung

        self.app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])(self.proxy)
        self.app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])(self.proxy)

    def run(self, host='localhost', port=5000):
        self.app.run(host=host, port=port)

    def proxy(self, path):
        url = self.openhab_base_url + '/' + path
        headers = request.headers  # Verwende die Header des eingehenden Requests

        if request.method == 'GET':
            response = requests.get(url, headers=headers, params=request.args)
        elif request.method == 'POST':
            response = requests.post(url, headers=headers, json=request.json)
        elif request.method == 'PUT':
            response = requests.put(url, headers=headers, json=request.json)
        elif request.method == 'DELETE':
            response = requests.delete(url, headers=headers, json=request.json)

        # Erstelle die Flask-Antwort mit dem Inhalt und dem Statuscode der openHAB-Antwort
        flask_response = Response(response.content, status=response.status_code, headers=response.headers)

        # Setze die CORS-Header in der Flask-Antwort
        flask_response.headers['Access-Control-Allow-Origin'] = '*'
        flask_response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        flask_response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'

        return flask_response

if __name__ == '__main__':
    openhab_base_url = 'https://openhab.example.com/rest'  # Ersetze dies mit der tatsächlichen openHAB-URL

    proxy = OpenHABProxy(openhab_base_url)
    proxy.run()
