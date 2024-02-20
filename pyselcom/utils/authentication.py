import base64
import hmac
from config import Config


"""
    SELCOM API uses Base64 to encode all of the auth data sent to the API.
    This includes all of the data sent to the HEADER
"""

config = Config()


# Function encodes header digest data(Data sent to the Payload)
def digest_payload(timestamp: str, payload: dict) -> str:

    # timestamp is the current time
    # payload is the request payload data to be encoded

    # the structure of the digest (timestamp=[timezone as in header 2019-02-26T09:30:46+03:00]&field1=value1&fielf...in the order defined in Signed-Fields)
    # ReadMore https://developers.selcommobile.com/#authentication

    digestedData = f"timestamp={timestamp}"

    # loop payload
    for key in payload.keys():

        # digest each payload and add to digestedData
        digestedData += f"&{key}={payload[key]}"
    
    base64Data = base64.b64encode(hmac.digest(config.API_KEY.encode(), digestedData.encode(), 'sha256')).decode()


    return base64Data


# Function to return signed fiels array
def signed_fiels(payload: dict) -> list:

    keys = ",".join(payload.keys())

    return keys