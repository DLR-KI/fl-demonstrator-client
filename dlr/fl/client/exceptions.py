import json
from requests import Response


class CommunicationException(Exception):
    """
    Server communication exception base class.
    """
    def __init__(self, response: Response, *args, **kwargs) -> None:
        """
        Create a new communication exception.

        Args:
            response (Response): http response from the server
        """
        message = "Something really went wrong with the server response!"
        try:
            message = response.text
            message = json.loads(message)["message"]
        except Exception:
            pass
        super().__init__(message, *args, **kwargs)
        self.response = response


class MetricsUploadException(CommunicationException):
    """Global model metrics upload (to the server) exception."""
    pass


class ModelDownloadException(CommunicationException):
    """Global model download (from the server) exception."""
    pass


class ModelUploadException(CommunicationException):
    """Local model upload (to the server) exception."""
    pass
