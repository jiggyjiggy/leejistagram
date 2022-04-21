import json

from django.http     import JsonResponse
from django.views    import View

from postings.models import Posting
from postings.models import Image

from users.models    import User


class PostingView(View):
    def post(self, request):
        data = json.loads(request.body)

        user = User.objects.get(username=data.get('user', None))

        image = data["image"]
        board = data["board"]
        user_name = data["name"]

        Posting.objects.create(
            image = image,
            board = board
        )


        return JsonResponse({'message': 'SUCCESS'}, status=201)

    def get(self, request):
        postings = Posting.objects.all()
        print(postings)
        results = []

        for posting in postings:
            results.append(
                {
                    "user_name"          : posting.user.name,
                    "posting_image"      : posting.image,
                    "posting_board"      : posting.board,
                    "posting_created_at" : posting.created_at
                }
            )

        return JsonResponse({'results' : results}, status=200)