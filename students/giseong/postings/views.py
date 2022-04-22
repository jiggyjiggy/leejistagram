import json

from django.http     import JsonResponse
from django.views    import View

from postings.models import Posting
from postings.models import Image

from users.models    import User

from users.utils import check_token


class PostingView(View):
    @check_token
    def post(self, request):
        try:
            data = json.loads(request.body)

            user           = request.user
            board          = data["board"]
            image_url_list = data["image_url"]

            posting = Posting.objects.create(
                board = board,
                user  = user
            )

            for image_url in image_url_list:
                Image.objects.create(
                    image_url = image_url,
                    posting   = posting
                )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)


    def get(self, request):
        try:
            postings = Posting.objects.all()
            results = []

            for posting in postings:
                images = posting.image_set.all()
                images_list = []

                for image in images:
                    images_list.append(
                        {
                            "posting_image_url" : image.image_url
                        }
                    )

                results.append(
                    {
                        "user_name"          : posting.user.name,
                        "posting_board"      : posting.board,
                        "posting_created_at" : posting.created_at,
                        "image_url" : images_list
                    }
                )

            return JsonResponse({'results' : results}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)