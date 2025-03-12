from flask import Flask, make_response

app = Flask(__name__)

# rota que manipula a criação do cookie
@app.route('/cookie1')
def cookie1():
    text = '<h1>Um cookie foi definido<h1/>'
    response = make_response(text)
    response.set_cookie('primeiro_cookie', 'teste')
    return response