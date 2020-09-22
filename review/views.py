from django.shortcuts import render, redirect
from .forms import CreateReview,DetgleForm
from .models import Review,Detgle,ReviewAttachFile
from django.views.generic import TemplateView,ListView,CreateView,UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from todal.views import OwnerOnlyMixin
import os
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from todal.views import cnt_Review
from movies.view2 import pagenate
# Create your views here.

def genre_Count(reviews):
    genre_count = []
    if reviews:
        genre_count.append({'comedy': len(reviews.filter(genre__contains="코미디")),
                        'documentary': len(reviews.filter(genre__contains="다큐멘터리")),
                        'animation': len(reviews.filter(genre__contains="애니메이션")),
                        'thriller': len(reviews.filter(genre__contains="스릴러")),
                        'SF': len(reviews.filter(genre__contains="SF")),
                        'action': len(reviews.filter(genre__contains="액션")),
                        'romance': len(reviews.filter(genre__contains="로맨스")),
                        'horror': len(reviews.filter(genre__contains="공포")),
                        })
    return genre_count[0]

def reviewList(request):
    reviews = Review.objects.order_by('-create_date')
    genre_count=genre_Count(reviews)
    cnt_review = cnt_Review(4)
    if request.method == "GET":
         reviews = search(request,reviews)
    reviews = pagenate(request, reviews,4)
    return render(request, 'reviewList.html', {'reviews':reviews,'genre_count':genre_count, 'cnt_review':cnt_review})

def reviewAfter(request):
    reviews_spo = Review.objects.order_by('-create_date')
    reviews=reviews_spo.filter(spo__contains="포함")
    genre_count = genre_Count(reviews)
    cnt_review = cnt_Review(4)
    if request.method == "GET":
         reviews = search(request,reviews)


    return render(request, 'reviewAfter.html', {'reviews':reviews,'genre_count':genre_count,'cnt_review':cnt_review})
def reviewBefore(request):
    reviews_spo = Review.objects.order_by('-create_date')
    reviews=reviews_spo.filter(spo__contains="미포함")
    genre_count = genre_Count(reviews)
    cnt_review = cnt_Review(4)
    if request.method == "GET":
         reviews = search(request,reviews)


    return render(request, 'reviewBefore.html', {'reviews':reviews,'genre_count':genre_count,'cnt_review':cnt_review})

def reviewdetale(request,id):
    review = Review.objects.get(id=id)
    reviews = Review.objects.all()
    genre_count = genre_Count(reviews)
    comment_form = DetgleForm()
    cnt_review = cnt_Review(4)
    if request.method == "GET":
        if reviews != search(request,reviews):
            reviews = search(request,reviews)
            return render(request, 'reviewList.html', {'reviews':reviews,'genre_count':genre_count})

    return render(request, 'reviewDetail.html', {'comment_form':comment_form, 'review':review,'reviews':reviews,'genre_count':genre_count,
                                                 'cnt_review':cnt_review })


def createReview(request):

    if request.method == 'POST':
        form = CreateReview(request.POST,request.FILES)

        if form.is_valid():
            form.instance.user = request.user
            form.save()

            return redirect('review:index')
        else:
            print(form.errors)
            return redirect('review:index')
    else:
        form = CreateReview()
        return render(request, 'createReview.html', {'form':form})

def delete(request, id):
    review = Review.objects.get(id=id)
    review.delete()
    return redirect('review:index')

def edit(request,id):
    review = Review.objects.get(id=id)
    # 글을 수정사항을 입력하고 제출을 눌렀을 때
    if request.method == "POST":
        form = CreateReview(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            # {'name': '수정된 이름', 'image': <InMemoryUploadedFile: Birman_43.jpg 	(image/jpeg)>, 'gender': 'female', 'body': '수정된 내용'}
            review.title = form.cleaned_data['title']
            review.movie_title = form.cleaned_data['movie_title']
            review.genre = form.cleaned_data['genre']
            review.spo = form.cleaned_data['spo']
            review.content = form.cleaned_data['content']
            review.SNImg = form.cleaned_data['SNImg']
            review.save()
            return redirect('/review/' + str(id))

    # 수정사항을 입력하기 위해 페이지에 처음 접속했을 때
    else:
        form = CreateReview()
        return render(request, 'review/createReview.html', {'form': form})


# 댓글 생성하기
@login_required
def commentCreate(request, id):
    #   # 댓글 작성 폼을 list에서 보여줌.
    comment_form = DetgleForm(request.POST)
    if comment_form.is_valid():
        # 유저정보, 몇번 글 넣어야 하는지 전달할거니까 기다려
        review = Review.objects.get(id=id)
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.review = review
        comment.save()

    return redirect('review:redetail',id)


# 댓글 삭제하기
@login_required
def commentDelete(request, id, comment_id):
    comment = Detgle.objects.get(id=comment_id)
    if comment.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this Comment")
    else:
        comment.delete()
    return redirect('review:redetail', id)

def search(request,review):
    # GET request의 인자중에 searchword값이 있으면 가져오고, 없으면 빈 문자열 넣기
    searchword = request.GET.get('searchword', '')
    if searchword:  # searchword가 있다면
        searchReview = review.filter(movie_title__contains=searchword)  # 제목에 searchword가 포함된 레코드만 필터링
    else:
        searchReview = review
    return searchReview

    # mainpage에서는
    # <검색기능>작품의 제목,배우,감독을 검색해 해당 영화의 디테일 페이지로 연결하는 역할을 한다.
    # 일단 작품의 제목으로 검색하는 것을 구현
    # <로그인버튼>