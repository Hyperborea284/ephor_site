from .models import UserAccessLog

class UserAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = self.get_client_ip(request)
        user_agent = request.headers.get('User-Agent', '')
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)

        # Salvar no banco de dados
        UserAccessLog.objects.create(
            ip_address=ip_address,
            user_agent=user_agent,
            latitude=latitude,
            longitude=longitude
        )

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
