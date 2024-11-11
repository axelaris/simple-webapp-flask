import os
from flask import Flask
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

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
            vault_url=f"https://{VAULT_NAME}.vault.azure.net/", credential=credential)
        secret = secret_client.get_secret(f"{KEY_VAULT_SECRET_NAME}")
    except Exception:
        logger.error('Failed to get secret', exc_info=True)
        raise Exception(
            'Failed to get secret'
        )

    OUTPUT='KeyVault name is '+VAULT_NAME+", secret name is "+KEY_VAULT_SECRET_NAME+", value is "+secret.value

    return OUTPUT

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
