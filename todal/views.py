from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render
from movies.models import Movie
from review.models import Review
def cnt_Review(ran):
    review = Review.objects.order_by('-read_cnt')
    resultReview = []
    for I in range(ran):
        resultReview.append({'title': review[I].title, 'Mtitle': review[I].movie_title, 'user': review[I].user, 'id': review[I].id,'A': I + 1,
                             'date': review[I].create_date, 'SNImg': review[I].SNImg})
    return resultReview
def homeview(request):
    movie = Movie.objects.all()
    resultReview = []
    if request.method == "GET":
        searchword = request.GET.get('searchword', '')
        resultMovie = []

        if searchword:  # searchword가 있다면
            searchMovie = movie.filter(title__contains=searchword)  # 제목에 searchword가 포함된 레코드만 필터링
            if searchMovie:
                # 영화 여러개 저장위해 데이터의 개수
                movie_count = searchMovie.count()
                for c in range(movie_count):
                    # 데이터들 resultMovie리스트에 저장
                    # 원본 주석처리
                    # resultMovie.append({searchMovie[c].title:searchMovie[c].id})
                    resultMovie.append({'title': searchMovie[c].title, 'id': searchMovie[c].id})
                    # 디테일 페이지 이동위해 id값도 넘겨준다
                # print(resultMovie)
                return render(request, 'movies/searchresult.html',
                              {'movie': movie, 'searchMovie': searchMovie, 'resultMovie': resultMovie})
            else:
                # 아무것도 입력하지 않는다면,
                return render(request, 'movies/searchresult.html', {'resultMovie': resultMovie})

    resultReview = cnt_Review(3)
    return render(request, 'home.html', {'reviews': resultReview})

def infoview(request):


    return render(request, 'info.html')



class OwnerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "Owner only can update/delete the object"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object() #모델 인스턴스 얻기
        if self.request.user != self.object.owner:
            self.handle_no_permission()
        return super().get(request, *args, **kwargs)