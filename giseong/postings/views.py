import json

from django.http     import JsonResponse
from django.views    import View

from postings.models import Posting
from postings.models import Image
from postings.models import Comment
from postings.models import Like

from users.models import User

from users.utils  import check_token


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
                        "posting_id"         : posting.id,
                        "posting_board"      : posting.board,
                        "posting_created_at" : posting.created_at,
                        "image_url" : images_list
                    }
                )

            return JsonResponse({'results' : results}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)


class CommentView(View):
    @check_token
    def post(self, request):
        try:
            data = json.loads(request.body)

            user    = request.user
            posting = Posting.objects.get(id=data["posting_id"])    # filter 쓰면 querset으로 반환
            comment = data["comment"]

            Comment.objects.create(
                comment = comment,
                user    = user,
                posting = posting   # create 시에는 instance로 반환해줘야함
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    def get(self, request):
        try:
            postings = Posting.objects.all()

            results = []

            for posting in postings:
                comments = posting.comment_set.all()
                comments_info = []

                for comment in comments:
                    user_email = User.objects.get(email=comment.user.email).email
                    comments_info.append(
                        {
                            "user_email": user_email,
                            "comment_id" :comment.id,
                            "posting_comment" : comment.comment,
                            "created_at": comment.created_at
                        }
                    )

                results.append(
                    {
                        "posting_id" : posting.id,
                        "comments_list" : comments_info
                    }
                )
            return JsonResponse({'results' : results}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class LikeView(View):
    @check_token
    def post(self, request):
        try:
            data = json.loads(request.body)

            user       = request.user
            posting_id = data['posting_id']

            user_like     = Like.objects.filter(user=user, posting_id=posting_id)
            posting_likes = Like.objects.filter(posting_id=posting_id)

            like_info = []

            if user_like.exists():
                user_like.delete()

                like_info.append({
                    # "user_like_existence" : False,
                    "posting_likes" : posting_likes.count()
                })
                return JsonResponse({'message': 'SUCCESS', 'like_info': like_info}, status=200)

            else:
                Like.objects.create(user=user, posting_id=posting_id)

                like_info.append({
                    # "user_like_existence": True,
                    "posting_likes": posting_likes.count()
                })
                return JsonResponse({'message': 'SUCCESS', 'like_info': like_info}, status=200)

        except:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    @check_token
    def get(self, request):
        try:
            user = request.user

            like_postings = Like.objects.filter(user=user)
            results = []
            for like_posting in like_postings:
                results.append({
                    "like_posting" : like_posting.posting_id
                })
            return JsonResponse({'message': 'SUCCESS', 'results': results}, status=200)

        except:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)