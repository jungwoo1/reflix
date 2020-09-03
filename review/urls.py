from django.urls import path
import review.views

app_name="review"


urlpatterns =[
    path('reviewList/',review.views.reviewList, name="index"),
    path('reviewList/after',review.views.reviewAfter, name="after"),
    path('reviewList/before',review.views.reviewBefore, name="before"),
    path('createReview/',review.views.createReview, name="crReview"),
    path('editReview/<int:id>',review.views.edit, name="editReview"),
    path('crview',review.views.ReviewCreateView.as_view(), name="text"),
    path('<int:id>',review.views.reviewdetale, name="redetail"),
    path('<int:id>/comment/create/',review.views.commentCreate, name="commentCreate"),
    path('<int:id>/comments/<int:comment_id>/delete/', review.views.commentDelete, name='commentDelete')
]