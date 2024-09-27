import secrets
import string
from typing import Dict, List, Optional

import mercadopago
from django.conf import settings

from .exception import HttpPaymentException


class Payment():

    def __init__(self):

        self.__preference_data = {
            "items": [],
            "payer": {}
        }
        self.__prod = getattr(settings, "MERCADOPAGO_IS_PROD", False)
        self.__create_preference()

    def __create_preference(self):

        # token handler

        token = getattr(settings, "MERCADOPAGO_TOKEN", None)

        if not token:
            raise AttributeError(
                'Unable to find MERCADOPAGO_TOKEN in settings.py. Did you perhaps forget to include it?')

        # Agrega credenciales
        self.sdk = mercadopago.SDK(token)

        # Redirect Urls

        get_back_urls = getattr(settings, "MERCADOPAGO_BACK_URLS", None)

        if not get_back_urls:
            raise AttributeError(
                'Unable to find MERCADOPAGO_BACK_URLS in settings.py. Did you perhaps forget to include it?')

        if not get_back_urls.get('success'):
            raise LookupError(
                'Unable to find the "success" key of MERCADOPAGO_BACK_URLS in settings.py. Did you perhaps forget to include it?')

        if not get_back_urls.get('failure'):
            raise LookupError(
                'Unable to find the "failure" key of MERCADOPAGO_BACK_URLS in settings.py. Did you perhaps forget to include it?')
        if not get_back_urls.get('pending'):
            raise LookupError(
                'Unable to find the "pending" key of MERCADOPAGO_BACK_URLS in settings.py. Did you perhaps forget to include it?')

        self.__preference_data["back_urls"] = get_back_urls

        # Auto-return after payment

        auto_return = getattr(settings, "MERCADOPAGO_AUTO_RETURN", False)

        if auto_return:
            self.__preference_data["auto_return"] = "approved"

        # IPN

        ipn = getattr(settings, "MERCADOPAGO_IPN", None)

        if ipn:
            self.__preference_data["notification_url"] = ipn

        # Allow Mercado Pago credit

        allow_credit = getattr(settings, "MERCADOPAGO_ALLOW_CREDIT", False)
        if allow_credit:
            self.__preference_data["purpose"] = "onboarding_credits"

        #  Text on the payer's credit card statement to identify the purchase

        statement_descriptor = getattr(
            settings, "MERCADOPAGO_STATEMENT_DESCRIPTOR", False)
        if allow_credit and len(statement_descriptor) < 17:
            self.__preference_data["statement_descriptor"] = statement_descriptor

    def exclude_payment_methods(self, methods: Optional[List[Dict[str, str]]] = None, types: Optional[List[Dict[str, str]]] = None):

        if self.__preference_data.get('payment_methods'):
            self.__preference_data['payment_methods']["excluded_payment_methods"] = methods or [
            ]
            self.__preference_data['payment_methods']["excluded_payment_types"] = types or [
            ]
        else:
            self.__preference_data['payment_methods'] = {
                'excluded_payment_methods': methods or [],
                'excluded_payment_types': types or []
            }

    def set_installments(self, installments: int = 1):
        if self.__preference_data.get('payment_methods'):
            self.__preference_data['payment_methods']["installments"] = installments

        else:
            self.__preference_data['payment_methods'] = {
                "installments": installments
            }

    def only_accounts(self, value: bool = False):
        self.__preference_data["purpose"] = "wallet_purchase"

    def set_expiry(self, start: str, end: str):
        """
            Set expiry in format ISO 8601: yyyy-MM-dd'T'HH:mm:ssz.
        """

        self.__preference_data["expires"] = True
        self.__preference_data["expiration_date_from"] = start
        self.__preference_data["expiration_date_to"] = end

    def set_shipments(self, ship: int):

        if self.__preference_data.get('shipments'):
            self.__preference_data['shipments']['cost'] = ship
            self.__preference_data['shipments']['mode'] = "not_specified"
        else:
            self.__preference_data['shipments'] = {
                'cost': ship,
                "mode": "not_specified"
            }

    def set_shipment_address(self, **kwargs):
        """
            Sets the shipment address in the preference data dictionary.

            Keyword Arguments:
            - street_name (str): The street name of the shipment address.
            - zip_code (str): The zip code of the shipment address.
            - city Optional(str): The city of the shipment address.
            - state Optional(str): The state of the shipment address.
            - number Optional(str): The number of the shipment address.
            - floor Optional(str): The floor of the shipment address.
            - apartment Optional(str): The apartment of the shipment address.
            - country_name Optional(str): The country name of the shipment address.
        """

        if self.__preference_data.get('shipments'):
            self.__preference_data['shipments']['receiver_address'] = {
                'street_name': kwargs.get('street_name', ""),
                'zip_code':  kwargs.get('zip_code', ''),
                'city': kwargs.get('city', ''),
                'state': kwargs.get('state', ''),
                'number': kwargs.get('number', ''),
                'floor': kwargs.get('floor', ''),
                'apartment': kwargs.get('apartment', ''),
                'country_name': kwargs.get('country_name', '')
            }
        else:
            self.__preference_data['shipments'] = {
                'receiver_address': {
                    'street_name': kwargs.get('street_name', ""),
                    'zip_code':  kwargs.get('zip_code', ''),
                    'city': kwargs.get('city', ''),
                    'state': kwargs.get('state', ''),
                    'number': kwargs.get('number', ''),
                    'floor': kwargs.get('floor', ''),
                    'apartment': kwargs.get('apartment', ''),
                    'country_name': kwargs.get('country_name', '')
                }
            }

    def set_payer_info(self, **kwargs):
        """
            Sets payer information in the preference data dictionary.

            Keyword Arguments:
            - name (str): Payer's name.
            - surname (str): Payer's surname.
            - email (str): Payer's email address.
            - phone (dict): Dictionary containing payer's phone details with keys:
                    - area_code Optional(str): Payer's phone area code.
                    - number (str): Payer's phone number.
        """

        if kwargs.get('name'):
            self.__preference_data['payer']['name'] = kwargs.get('name')
        if kwargs.get('surname'):
            self.__preference_data['payer']['surname'] = kwargs.get('surname')
        if kwargs.get('email'):
            self.__preference_data['payer']['email'] = kwargs.get('email')
        if kwargs.get('phone'):
            phone = kwargs.get("phone")
            self.__preference_data['payer']['phone'] = {
                'area_code': phone.get("area_code", ""), 'number': phone.get('number')}

    def set_items(self, items: List[Dict[str, Dict]]):
        """
            Sets the items for the payment with the provided list of item details.

            Args:
            - items (list of dict): A list of dictionaries where each dictionary represents an item with the following keys:
                - id (str): The product ID
                - title (str): The name of the product
                - description (str): A description of the product (optional).
                - picture_url (str): The URL of the product image (optional).
                - category_id (str): The category ID of the product  (optional).
                - quantity (int): The quantity of the product
                - currency_id (str): The currency ID for the product price  (optional).
                - unit_price (float): The unit price of the product
        """

        if items:
            self.__preference_data["items"].extend(items)

    def _create_external_reference(self):
        reference = ""

        for _ in range(30):
            reference += secrets.choice(string.ascii_letters + string.digits)

        return reference

    def get_url(self, preference: Optional[str] = None):

        external_reference = self._create_external_reference()

        if preference:
            preference_response = self.sdk.preference().get(preference)
        else:
            self.__preference_data["external_reference"] = external_reference
            preference_response = self.sdk.preference().create(self.__preference_data)

        preference = preference_response["response"]

        if not 200 <= preference_response.get("status") <= 204:

            raise HttpPaymentException(detail=preference.get(
                'message', ""), code=preference.get('status', 400))

        if self.__prod:
            response = preference["init_point"]
        else:
            response = preference["sandbox_init_point"]
        return preference.get("external_reference"), response
