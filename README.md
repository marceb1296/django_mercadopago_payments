# django-mercadopago-payments

Integrate payments easily with Mercado Pago in your Django project!

## Clone the repository into your Django project and install dependencies 

`git clone https://github.com/marceb1296/django-mercadopago-payments.git`

`pip install -r requirements.txt`

## In your settings.py

```
#Add django-mercadopago-payments to yours apps
INSTALLED_APPS = [
    ...
    'django_mercadopago_payments',
]

#You can get your credentials here https://www.mercadopago.com.mx/developers/panel/credentials
MERCADOPAGO_TOKENS = {
    #Like always, in development mode use test access token
    #if you don't set 'test' key, automatically will take 'prod' key
    'test': "TEST...",
    'prod': "..."  
}

#Your redirect URLs after payment
MERCADOPAGO_BACK_URLS = {
	"success": "https://www.tu-sitio/success",
	"failure": "https://www.tu-sitio/failure",
	"pending": "https://www.tu-sitio/pendings"
}

#Declare this var if you want redirect the user after payment automatically
MERCADOPAGO_AUTO_RETURN = True
```

## In your views.py

```
...
from django_mercadopago_payments.payment import Payment

class YourView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        #Start class
        payment = Payment()

        #Set product, quantity and unit price. You can see all category_id here https://api.mercadopago.com/item_categories
        #If you have more than 1 article, use a for loop 
        payment.preference_data['items'].append(
	    {'title': product_name, 'category_id': 'otros', "currency_id": "MXN", 'quantity': product_quantity, 'unit_price': product_unit_price}
	)

        #Set payer info
        payment.set_payer_info(
	    name="name",
	    surname="first_name",
	    email="email",
	    phone="phone"
	)

        #Set payer address
        payment.set_shipment_address(street_name="address", zip_code=11111)
	
        #Exclude payment methods and types. You can check all exclude and types payments here https://www.mercadopago.com.mx/developers/pt/guides/resources/localization/payment-methods#bookmark_payment_means_by_country
        methods = {'id': 'bitcoin'}
	types = {'id': 'digital_currency'}
	payment.exclude_payment_methods(methods=methods, types=types)

        #if you want set a ship cost
        ship = 1
        payment.set_shipments(ship)

        #By default, mercadopago accept payments till 24 months
        #If you want set just 1 or till 6, just add this line 
        payment.set_installments(n)

        #Finally, you can get payment url calling the get_url function
        pay_url = payment.get_url()
 
        return redirect(pay_url)
			    
```

## Contact for any error, doubt or suggestion
Email: marce_1996hr@hotmail.com
