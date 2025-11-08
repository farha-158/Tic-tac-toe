import ssl
from game import create_app, socketio
from exception import SSLCertificateError 

app = create_app()

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
try:
    context.load_cert_chain("cert.pem", "key.pem")
except FileNotFoundError as e:
    raise SSLCertificateError(f"Certificate or key file not found: {e}")
except ssl.SSLError as e:
    raise SSLCertificateError(f"Invalid certificate or key: {e}")

socketio.run(app,host="0.0.0.0", port=5000, ssl_context=context)