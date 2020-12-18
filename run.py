import os
import ssl
from nebracy import create_app


app = create_app(os.getenv('FLASK_ENV', 'Production'))

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(r'instance\cert.pem', r'instance\privkey.pem')
    app.run(ssl_context=context, debug=True)
