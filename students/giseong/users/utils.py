import jwt

from django.http import JsonResponse
from django.conf import settings

from users.models import User

def check_token(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers.get('Authorization')
            payload      = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            request.user = User.objects.get(id=payload['id'])

            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=403)

        except jwt.InvalidSignatureError:
            return JsonResponse({'message': 'INVALID_SIGNATURE'}, status=403)

        except jwt.DecodeError:
            return JsonResponse({'message': 'INVALID_PAYLOAD'}, status=403)

    return wrapper