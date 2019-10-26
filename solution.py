
from werkzeug.exceptions import HTTPException
import gnupg
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/decryptMessage', methods=['POST'])
def decryptMessage():

    if not request.data:
        return jsonify(dict(error='Empty body'))

    content = request.get_json()

    message = content.get('message')
    passphrase = content.get('passphrase')

    if not message or not passphrase:
        return jsonify(dict(error='Invalid Body'))

    gpg = gnupg.GPG(os.popen("which gpg").read().strip())

    decrypted_data = str(gpg.decrypt(message, passphrase=passphrase))

    if len(decrypted_data) == 0:
        return jsonify(dict(error='Invalid Passphrase'))


    return jsonify(dict(DecryptedMessage=f"{decrypted_data.strip()}"))



@app.errorhandler(HTTPException)
def error_handler(error):
    """
    Standard Error Handler
    """
    if isinstance(error, HTTPException):
        return jsonify({
            'statusCode': error.code,
            'error': error.name,
            'description': error.description
        }), error.code


if __name__ == '__main__':
    app.run()
