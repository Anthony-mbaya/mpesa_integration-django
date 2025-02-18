import requests
from requests.auth import HTTPBasicAuth #encodes the consumer key and secret for secure transmission
from django.conf import settings

def get_mpesa_access_token():
    '''generates OAuth token from saf API for authenticaing mpesa request'''
    #base_url = https://sandbox.safaricom.co.ke
    #?grant_type=client_credentials - query param tell use of consumer key and secret
    url = f"{settings.MPESA_CONFIG['base_url']}/oauth/v1/generate?grant_type=client_credentials"
    consumer_key = settings.MPESA_CONFIG['consumer_key']
    consumer_secret = settings.MPESA_CONFIG['consumer_secret']

    # get req to the token usiing basicAuth - encodes consumer key and secret
    res = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    if res.status_code == 200:
        return res.json().get('access_token')
    return None