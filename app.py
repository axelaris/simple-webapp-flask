import os
import signal
from flask import Flask
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

@app.route("/")
def main():
    return "Welcome!"

@app.route('/shutdown')
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)

@app.route('/pid')
def getpid():
    return str(os.getpid())

@app.route('/ver')
def ver():
    return '24-11-12.12-0'

@app.route('/kv')
def kv():
    KV_NAME = os.getenv('KV_NAME')
    KEY_VAULT_SECRET_NAME = os.getenv('SECRET_NAME')

    try:
        if 'MSI_CLIENT_ID':
            credential = DefaultAzureCredential(
                managed_identity_client_id=os.getenv('MSI_CLIENT_ID')
            )
        else:
            raise Exception
    except Exception:
        logger.error('Failed to obtain access token', exc_info=True)
        raise Exception(
            'Failed to obtain access token'
        )

    try:
        secret_client = SecretClient(
            vault_url=f"https://{KV_NAME}.vault.azure.net/", credential=credential)
        secret = secret_client.get_secret(f"{KEY_VAULT_SECRET_NAME}")
    except Exception:
        logger.error('Failed to get secret', exc_info=True)
        raise Exception(
            'Failed to get secret'
        )

    OUTPUT='KeyVault name is '+KV_NAME+", secret name is "+KEY_VAULT_SECRET_NAME+", value is "+secret.value

    return OUTPUT

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
