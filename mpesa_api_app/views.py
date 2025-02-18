from django.shortcuts import render
from django.http import JsonResponse
from .mpesa_OAuth import get_mpesa_access_token
import requests
import base64
import datetime
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

#display form
def form(request):
    return render(request, 'mpesa.html')

#testing token generation
def get_token_view():
    '''endpoint to retrive the access token'''
    # this shows you are authenticate to access mpesa request
    token = get_mpesa_access_token() # from mpesa_OAuth file
    if token:
        return JsonResponse({"access_token": token})
    return JsonResponse({"errror": "failed to get token"}, status=400)

def stk_push(request):
    #mpesa access token from mpesa_OAuth file
    access_token = get_mpesa_access_token()

    if not access_token:
        return JsonResponse({"error": "Failed to get mpesa access token"}, status=400)

    #if http req is post from ie from form
    if request.method == 'POST':
        amount = request.POST.get('amount') #attr(name) - amt
        phone_number = request.POST.get('phone_number') #attr(name) - phone_number
        #format phone number
        def format_phone_no(phone_number):
            """Formats the phone number to the required 254XXXXXXXX format."""
            if phone_number.startswith('0'):
                phone_number = '254' + phone_number[1:]
            elif phone_number.startswith('+254'):
                phone_number = '254' + phone_number[4:]
            elif not phone_number.startswith('254'):
                phone_number = '254' + phone_number
            return phone_number
        if phone_number:
            formatted_phone_number = format_phone_no(phone_number)
        else:
            return JsonResponse({"error": "phone number is required"}, status=400)
        # validating amount
        if not amount:
            return JsonResponse({"error": "amount is required"}, status=400)
        try:
            amount = int(amount) #covert to integrer
            if amount <= 0:
                return JsonResponse({"error": "amount must be greater than 0"}, status=400)
        except ValueError:
            return JsonResponse({"error": "amount must be a number"}, status=400)

    # time format - Y-M-D-H-M-S using detetime module
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # mpesa password created using {business_shortcode, passkey, timestamp}
    #  Base64 encoding transforms binary data into an ASCII string format (....)
    # decode - decodes this byte string back into a regular string (str)
    password = base64.b64encode(
        f"{settings.MPESA_CONFIG['business_shortcode']}{settings.MPESA_CONFIG['passkey']}{timestamp}".encode()
    ).decode('utf-8')

    # STK - Short Code Push
    # base_url - holds base url for mpesa api
    # stk_url - holds complete url sent to http post req with other amt,phone
    stk_url = f"{settings.MPESA_CONFIG['base_url']}/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
    "BusinessShortCode": settings.MPESA_CONFIG['business_shortcode'], # paybill or till no
    "Password": password, # base64-encoded businness_shortcode + passkey + timestamp
    "Timestamp": timestamp, # y-m-d-h-m-s
    "TransactionType": "CustomerPayBillOnline", # for till number
    "Amount": amount,  # Change dynamically
    "PartyA": formatted_phone_number,  # Change dynamically - customer phone number
    "PartyB": settings.MPESA_CONFIG['business_shortcode'], # paybil or till
    "PhoneNumber": formatted_phone_number,  # Change dynamically - same customer phone number
    "CallBackURL": settings.MPESA_CONFIG['callback_url'], # api endpoint for receiving responses
    "AccountReference": "Mbaya's Apartment", # business name
    "TransactionDesc": "Payment for shares", # description of transaction
    }
    # post
    response = requests.post(stk_url, json=payload, headers=headers)

    return JsonResponse(response.json())
