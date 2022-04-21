from django.urls    import path

from postings.views import PostingView

urlpatterns = [
    path('/postings', PostingView.as_view())
]