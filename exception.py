from game.logger import logger

class ServerError(Exception):
    pass
# ===== SSL Exceptions =====

class SSLCertificateError(ServerError):
    """Raised when SSL certificate or key is missing or invalid."""
    def __init__(self, message="SSL certificate or key error"):
        super().__init__(message)
        logger.error("ssl_certificate_error", player=None, details=message)

class SSLHandshakeError(ServerError):
    """Raised when SSL handshake with client fails."""
    def __init__(self, client_addr, message="SSL handshake failed"):
        self.client_addr = client_addr
        super().__init__(f"{message}: {client_addr}")
        logger.warning("ssl_handshake_failed", player=client_addr, details=message)
