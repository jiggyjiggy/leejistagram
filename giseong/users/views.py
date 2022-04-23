import jwt
import json
import bcrypt

from django.http            import JsonResponse
from django.conf            import settings
from django.views           import View
from django.core.exceptions import ValidationError

from users.models           import User
from users.validators       import (
                                validate_email,
                                validate_password,
                                duplicated_email
                            )


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name         = data['name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']

            validate_email(email)
            duplicated_email(email)
            validate_password(password)

            hashed_password = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt())
            decoded_hashed_password = hashed_password.decode('UTF-8')

            User.objects.create(
                name         = name,
                email        = email,
                password     = decoded_hashed_password,
                phone_number = phone_number
            )
            return JsonResponse({'message' : 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except ValidationError as error:
            return JsonResponse({'message' : error.message}, status=error.code)


class LogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']

            user = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)

            access_token = jwt.encode({'id' : user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            print(access_token)

            return JsonResponse({
                'message'      : 'SUCCESS',
                'access_token' : access_token
            }, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_EMAIL"}, status=401)


class TokenCheckView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            payload = jwt.decode(data['Authorization'], settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            user = User.objects.get(id=payload['id'])

            if User.objects.filter(id=user.id).exists():
                return JsonResponse({'message' : 'WELCOME'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status=403)

        except jwt.InvalidSignatureError:
            return JsonResponse({'message' : 'INVALID_SIGNATURE'}, status=403)

        except jwt.DecodeError:
            return JsonResponse({'message' : 'INVALID_PAYLOAD'}, status=403)