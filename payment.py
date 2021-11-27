from django.conf import settings


import mercadopago

class Payment():
	
	
	def __init__(self):
		
		self.preference_data = {
			"items": [],
			"payer": {}
		}
		self.prod = False
		self.create_preference()
	
	
	def create_preference(self):
	
		try:
			get_token = settings.MERCADOPAGO_TOKENS
		except:
			raise AttributeError('No se ha encontrado MERCADOPAGO_TOKENS en el archivo settings.py, ¿Olvidaste agreagrlo?')
			
		if get_token.get('test'):
			token = get_token.get('test')
		elif get_token.get('prod'):
			self.prod = True
			token = get_token.get('prod')
		else:
			raise LookupError('No se ha encontrado ningun token en MERCADOPAGO_TOKENS del archivo settings.py, ¿Olvidaste agregarlos?')
								
		# Agrega credenciales
		self.sdk = mercadopago.SDK(token)			
			
		try:
			get_back_urls = settings.MERCADOPAGO_BACK_URLS
		except:
			raise AttributeError('No se ha encontrado MERCADOPAGO_BACK_URLS en el archivo settings.py, ¿Olvidaste agreagrlo?')
			
		if not get_back_urls.get('success'):
			raise LookupError('No se ha podido encontrar la key "success" en MERCADOPAGO_BACK_URLS del archivo settings.py, ¿Olvidaste agregarla?')
		if not get_back_urls.get('failure'):
			raise LookupError('No se ha podido encontrar la key "failure" en MERCADOPAGO_BACK_URLS del archivo settings.py, ¿Olvidaste agregarla?')
		if not get_back_urls.get('pending'):
			raise LookupError('No se ha podido encontrar la key "pending" en MERCADOPAGO_BACK_URLS del archivo settings.py, ¿Olvidaste agregarla?')
		
		self.preference_data["back_urls"] = get_back_urls
				
		try:
			if settings.MERCADOPAGO_AUTO_RETURN:
				self.preference_data["auto_return"] = "approved"
		except:
			pass 
		
			
	def exclude_payment_methods(self, methods=None, types=None, installments=1):
		
		if methods and types:
			self.preference_data['payment_methods'] = {
				'excluded_payment_methods': [methods],
				'excluded_payment_types': [types]
			}			
	
	
	def set_installments(self, n):
		self.preference_data['payment_methods'] = {
				"installments": n
		}			
	
		
	def set_shipments(self, ship):
			
			self.preference_data['shipments'] = {
				'cost': ship,
				"mode": "not_specified"
			}
	
	
	def set_shipment_address(self, street_name=None, zip_code=None):
		if street_name and zip_code:
			self.preference_data['shipments'] = {'receiver_address': {'street_name': street_name, 'zip_code': zip_code}}
		
	
	def set_payer_info(self, **kwargs):
		
		if kwargs.get('name'):
			self.preference_data['payer']['name'] = kwargs.get('name')
		if kwargs.get('surname'):
			self.preference_data['payer']['surname'] = kwargs.get('surname')
		if kwargs.get('email'):
			self.preference_data['payer']['email'] = kwargs.get('email')
		if kwargs.get('phone'):
			self.preference_data['payer']['phone'] = {'area_code': '', 'number': kwargs.get('phone')}
			
	
	def get_url(self):
		
		preference_response = self.sdk.preference().create(self.preference_data)
		preference = preference_response["response"]
		if self.prod:
			response = preference["init_point"]
		else:
			response = preference["sandbox_init_point"]
		return response
	
	