from typing import Optional
from utils.config import Config
from utils.authentication import digest_payload, signed_fiels
import requests
import json
import datetime
import base64


"""
Process a order to SELCOM API

---------------------------

How Selcon API works

    - First you'll have to create an order to selcom API
    - After order creation you can send request to checkout an order you created

This class processes the order which is the checkout of the order,
It will initiate a payment to end-user
"""

config = Config()

class ProcessOrder(object):

    def __init__(
            self,
            transaction_id: str, 
            order_id: str, 
            msisdn: str, # phone number for initiate payment
        ) -> None:
        
        self._transaction_id = transaction_id
        self._order_id = order_id
        self._msisdn = msisdn


    # method for processing mobile money payment
    def wallet_pull_payment(self) -> dict:
        time = str(datetime.datetime.now())
        signedKey = base64.b64encode(config.API_KEY.encode()).decode()


        #making request to process payment
        url = config.SELCOM_BASE_URL + config.WALLET_PAYMENT_URL

        payload = {
            "transid": self._transaction_id,
            "order_id": self._order_id,
            "msisdn": self._msisdn,
        }

        headers = {
            'Digest-Method': 'HS256',
            'Digest': digest_payload(timestamp=time, payload=payload),
            'Authorization': f'SELCOM {signedKey}',
            'Signed-Fields': signed_fiels(payload=payload), 
            'Timestamp': time, 
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        return json.loads(response.text)