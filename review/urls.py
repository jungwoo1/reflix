from django.urls import path
import review.views
app_name="review"


urlpatterns =[
    path('',review.views.reviewList, name="reviewList"),
    path('createReview/',review.views.createReview, name="crReview")
]