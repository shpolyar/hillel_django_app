from .models import UserStat


class UserStatMiddleware:

    def __init__(self, get_response):
        self.response = get_response

    def __call__(self, request):
        headers = request.headers
        UserStat.objects.create(headers=headers)

        response = self.response(request)
        return response
