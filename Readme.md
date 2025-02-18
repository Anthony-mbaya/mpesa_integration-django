# MPESA INTEGRTION - STK PUSH
1. https://developer.safaricom.co.ke/
    account creation and app get:
        CONSUMER_KEY
        CONSUMER_SECRET
    APIS - Mpesa Express get:
        BUSINESS_SHORTCODE
        PASSKEY
        MPESA_BASE_URL
        CALLBACK_URL
2. configure in settings.py with .env {import load_dotenv and load_dotenv()}
3. i requests
4. mpesa access token file - for authenticating mpesa request
5. views - test access token
6. views - access the token in the stk push def for authentication to access mpesa req , create timestamp, password, stk_url, payload
7. html to create phone to handle custom input