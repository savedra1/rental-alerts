import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_requests_session() -> requests.Session():
    """
    Returns a session obect with a mounted retry strategy
    used to support provision/deprovisioning resources.
    """
    session = requests.Session()

    # Define a retry strategy
    retry_strategy = Retry(
        total=3,
        status_forcelist=[500, 501, 502, 503, 504],  # List of status codes to retry on
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],  # HTTP methods to retry
        backoff_factor=3,  # sleep 3 seconds between retries
        raise_on_status=False  # Don't raise an exception for these status codes
    )
    # Create an adapter with the retry strategy
    adapter = HTTPAdapter(max_retries=retry_strategy)

    # Mount the adapter to the session for all http and https requests
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session   