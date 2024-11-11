import os
from flask import Flask
app = Flask(__name__)

@app.route("/")
def main():
    return "Welcome!"

@app.route('/how are you')
def hello():
    return 'I am good, how about you?'

@app.route('/kv')
def kv():
    KV_NAME = os.getenv('KV_NAME')
    VAULT_NAME = "https://"+KV_NAME+".vault.azure.net/"
    KEY_VAULT_SECRET_NAME = os.getenv('SECRET_NAME')
    OUTPUT='KeyVault name is '+VAULT_NAME+", secret name is "+KEY_VAULT_SECRET_NAME

    return OUTPUT

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
