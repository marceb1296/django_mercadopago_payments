# django-mercadopago-payments

Integrate payments easily with Mercado Pago in your Django project!

## Clone the repository into your Django project and install dependencies

`git clone https://github.com/marceb1296/django_mercadopago_payments.git`

`pip install -r requirements.txt`

## In your settings.py

```
# Add django-mercadopago-payments to yours apps

INSTALLED_APPS = [
    ...
    'django_mercadopago_payments',
]

# You can get your credentials here https://www.mercadopago.com.mx/settings/account/credentials
# In the previous version, Mercado Pago provided both production and test tokens.
# Now, we need to create separate test accounts and use them with the production token

MERCADOPAGO_TOKEN = "prod_token"

# Return url checkout for production
MERCADOPAGO_IS_PROD = True

# Your redirect URLs after payment https://www.mercadopago.com.mx/developers/es/docs/checkout-pro/checkout-customization/user-interface/redirection

MERCADOPAGO_BACK_URLS = {
	"success": "https://www.tu-sitio/success",
	"failure": "https://www.tu-sitio/failure",
	"pending": "https://www.tu-sitio/pendings"
}

# Redirect the user after payment automatically

MERCADOPAGO_AUTO_RETURN = True

# Preferred url for receive MercadoPago payment Notifications. Only works in Production
# More info here https://www.mercadopago.com.mx/developers/es/docs/woocommerce/additional-content/your-integrations/notifications/ipn


MERCADOPAGO_IPN = "https://www.tu-sitio/notify/IPN"

# Allow Mercado Pago credit payment

MERCADOPAGO_ALLOW_CREDIT = True


# The statement descriptor is up to 16 characters of text on the payer's credit card statement to identify the purchase.

MERCADOPAGO_STATEMENT_DESCRIPTOR = "MIBUSINESS"
```

> [!IMPORTANT]
> IPN notifications will be discontinued. We recommend migrating to Webhooks notifications. More information at the provided link

## In your views.py

```
...
# Import module
from django_mercadopago_payments.payment import Payment

# Create preference

class YourView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        # Init

        payment = Payment()

        # Set product, quantity and unit price. You can see all category_id here https://api.mercadopago.com/item_categories

        my_items = [
            {
                'id': my_product_id, # required
                'title': product_name, # required,
                'description": "My awesome product",
                'picture_url: my_product_img_url
                'category_id': 'otros',
                'quantity': product_quantity, # required
                "currency_id": "MXN", # required
                'unit_price': product_unit_price # required
            }
        ]

        payment.set_items(my_items)

        # Set payer info

        payment.set_payer_info(
            name="name",
            surname="first_name",
            email="email",
            phone={
                "area_code": "",
                "phone" xxxxx # required
            }
        )

        # Set payer address

        payment.set_shipment_address(
            street_name = street_name, # required
            zip_code =  zip_code, # required
            city = city,
            state = state,
            number = number,
            floor = floor,
            apartment = apartment,
            country_name = country_nam,
        )

        # Exclude payment methods and types. You can check all exclude and types payments here https://www.mercadopago.com.mx/developers/es/live-demo/checkout-pro

        methods = [{'id': 'bitcoin'}]
	    types = [{'id': 'digital_currency'}]

        payment.exclude_payment_methods(methods=methods, types=types)

        # Set a ship cost

        payment.set_shipments(n)

        # By default, mercadopago accept payments till 24 months
        # Adjust as your requirements

        payment.set_installments(n)

        # Finally, you can get payment url calling the get_url function
        # You can use external_reference to associate ship products
        external_reference, pay_url = payment.get_url()

        # Normal post method

        return redirect(pay_url)

        # Ajax, axios, fetch... post method

        return JsonResponse({'pay_url': pay_url})

# Get preference by ID

class YourView(LoginRequiredMixin, View):
    def get(self, request, preference, *args, **kwargs):

        # Init

        payment = Payment()

        # You can use external_reference to associate ship products
        external_reference, pay_url = payment.get_url(preference)

        # Normal post method

        return redirect(pay_url)

        # Ajax, axios, fetch... post method

        return JsonResponse({'pay_url': pay_url})

```

## Contact for any error, doubt or suggestion

Email: marce_1996hr@hotmail.com
