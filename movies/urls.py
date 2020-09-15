from django.urls import path
from . import view2
app_name="movies"

urlpatterns =[
    path('', view2.main, name="main"),
    path('Action/', view2.movie_Action, name='Action'),
    path('Comedy',view2.movie_comedy,name="Comedy"),
    path('Animation/',view2.movie_Animation,name="Animation"),
    path('documentary',view2.movie_documentary,name="Documentary"),
    path('horror',view2.movie_horror,name="Horror"),
    path('romance',view2.movie_romance,name="Romance"),
    path('SF',view2.movie_SF,name="SF"),
    path('thriller',view2.movie_thriller,name="Thriller"),
    path('moviePickUp/', view2.moviePickUp, name="pickup"),
    path('search/', view2.search, name="search"),
    path('<int:id>/', view2.detail, name="detail"),
    path('<int:id>/comment/create/',view2.commentCreate, name="commentCreate"),
    path('<int:id>/comments/<int:comment_id>/delete/', view2.commentDelete, name='commentDelete'),
    path('<int:id>/score/create/',view2.scoreCreate, name="scoreCreate"),
    path('person/', view2.person, name="person"),
]