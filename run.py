from os import getenv as env
import ssl
from nebracy import create_app


app = create_app(env("FLASK_CONFIG"))

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(r'local\cert.pem', r'local\privkey.pem')
    app.run(ssl_context=context, debug=True)
