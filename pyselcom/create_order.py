from typing import Optional
from utils.config import Config
from utils.authentication import digest_payload, signed_fiels
import requests
import json
import uuid
from pytz import timezone
import base64


"""
Create a order to SELCOM API

---------------------------

How Selcon API works

    - First you'll have to create an order to selcom API
    - After order creation you can send request to checkout an order you created
"""

config = Config()

class OrderMinimal(object):

    def __init__(
            self,
            buyer_email: str, 
            buyer_name: str, 
            buyer_phone: str, 
            amount: int, 
            currency: Optional[str] = "TZS", 
            redirect_url: Optional[str] = None, 
            cancel_url: Optional[str] = None, 
            buyer_remarks: Optional[str] = None,
            merchant_remarks: Optional[str] = None,
            no_of_items: Optional[int] = 1,
            header_colour: Optional[str] = None,
            link_colour: Optional[str] = None,
            button_colour: Optional[str] = None,
            expiry: Optional[str] = None,
        ) -> None:
        
        self.buyer_email = buyer_email
        self._buyer_name = buyer_name
        self._buyer_phone = buyer_phone
        self._amount = amount
        self._currency = currency
        self._redirect_url = redirect_url
        self._cancel_url = cancel_url
        self._buyer_remarks = buyer_remarks
        self._merchant_remarks = merchant_remarks
        self._no_of_items = no_of_items
        self._header_colour = header_colour
        self._link_colour = link_colour
        self._button_colour = button_colour
        self._expiry = expiry


        # amount settle
        @property
        def amount(self):
            return self.amount
        
        @amount.setter
        def amount(self, value):
            if value < 1000:
                raise ValueError("Amount cannot be less than 1000")
            self._amount = value


        # method for creating an minimal order
        def order_minimal_request(self) -> dict:
            time = timezone('Africa/Dar_es_Salaam')
            signedKey = base64.b64encode(config.API_KEY.encode()).decode()


            #making request to create a new minimal order in selcom API
            url = config.SELCOM_BASE_URL + config.MINIMAL_ORDER_REQUEST_URL

            payload = json.dumps({
                "vendor": config.VENDOR,
                "order_id": uuid.uuid4().hex,
                "buyer_email": self._buyer_email,
                "buyer_name": self._buyer_name,
                "buyer_phone": self._buyer_phone,
                "amount": self._amount,
                "currency": self._currency,
                "no_of_items": self._no_of_items,
            })

            headers = {
                'Digest-Method': 'HS256',
                'Digest': digest_payload(timestamp=timezone, payload=payload),
                'Authorization': f'SELCOM {signedKey}',
                'Signed-Fields': signed_fiels(payload=payload), 
                'Timestamp': time, 
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            return json.loads(response.text)