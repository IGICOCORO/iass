from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import traceback

class DisableCSRF(MiddlewareMixin):
	def process_request(self, request):
		setattr(request, '_dont_enforce_csrf_checks', True)

# class CheckServerStatusMiddleware:
# 	def __init__(self, get_response):
# 		self.get_response = get_response

# 	def __call__(self, request):
		
# 		# izitararengana mbanza kuraba ko serveur iriko irazakira
# 		server_statuses = Service.objects.order_by("id")

# 		if server_statuses and server_statuses.first().status == STOPPED:
# 			return JsonResponse(data={
# 				'code': 'Service Unavailable',
# 				'message': "Maintance en cours!"
# 			}, status=503)
		
# 		response = self.get_response(request)

# 		# ntaco mpindura ku zisanzwe zamaze kurengana

# 		return response

class ExceptionMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		return response

	def process_exception(self, request, exception:Exception):
		
		message = str(exception)
		if "Duplicate entry '" in message:
			message =  "Umwanya wo gusubiramwo iki igikorwa uku nyene nturakwira."
			data = {
				'code': 'Internal server error',
				'message': message
			}
			return JsonResponse(data=data, status=500)
	
		try:
			raise exception
		except Exception:
			lines = traceback.format_exc().splitlines()
			list_errors = []
			for line in lines:
				if __package__ in str(line):
					list_errors.append(str(line).split("/")[-1])
			if len(list_errors) > 1:
				for line in list_errors[-2:]:
					print("[ERREUR]", str(line))
			else:
				print("[ERREUR]", str(list_errors[0]))
		data = {
			'code': 'Internal server error',
			'message': str(exception)
		}
		return JsonResponse(data=data, status=500)