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
# Create your views here.

def reviewList(request):
    reviews = Review.objects.all()

    return render(request, 'reviewList.html', {'reviews':reviews})
def reviewAfter(request):
    reviews_spo = Review.objects.all()
    reviews=reviews_spo.filter(spo__contains="포함")

    return render(request, 'reviewAfter.html', {'reviews':reviews})
def reviewBefore(request):
    reviews_spo = Review.objects.all()
    reviews=reviews_spo.filter(spo__contains="미포함")

    return render(request, 'reviewBefore.html', {'reviews':reviews})

def reviewdetale(requset,id):
    review = Review.objects.get(id=id)
    comment_form = DetgleForm()
    return render(requset, 'reviewDetail.html', {'comment_form':comment_form, 'review':review, })

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['title', 'movie_title', 'genre', 'content','spo','tag']
    #fields = ['title', 'description', 'content', 'tags']
    success_url = reverse_lazy('review:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        # 업로드 파일 열기
        files = self.request.FILES.getlist("files")
        for file in files:
            attach_file = ReviewAttachFile(post=self.object, filename=file.name,
                                         size=file.size, content_type=file.content_type,
                                         upload_file=file)
            attach_file.save()
        return response


class ReviewUpdateView(OwnerOnlyMixin, UpdateView):
    model = Review
    fields = ['title', 'movie_title', 'genre', 'content','spo','tag']
    success_url = reverse_lazy('review:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        delete_files = self.request.POST.getlist("delete_files")
        files = self.request.FILES.getlist("files")
        for file in files:
            attach_file = ReviewAttachFile(post=self.object, filename=file.name,
                                         size=file.size, content_type=file.content_type,
                                         upload_file=file)
            attach_file.save()

        for fid in delete_files:  # fid는 문자열 타입
            file = ReviewAttachFile.objects.get(id=int(fid))
            file_path = os.path.join(settings.MEDIA_ROOT, str(file.upload_file))
            os.remove(file_path)  # 실제 파일 삭제
            file.delete()  # 모델삭제(테이블 행 삭제

        return response
def createReview(request):

    if request.method == 'POST':
        form = CreateReview(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('review:index')
        else:
            return redirect('movies:main')
    else:
        form = CreateReview()
        return render(request, 'createReview.html', {'form':form})

def delete(request, review_id):
    review = Review.objects.get(id=review_id)
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
            review.save()
            return redirect('/review/' + str(id))

    # 수정사항을 입력하기 위해 페이지에 처음 접속했을 때
    else:
        form = CreateReview()
        return render(request, 'review/createReview.html', {'form': form})
class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html'

class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Review

    def get_queryset(self):
        return Review.objects.filter(tags__name=self.kwargs.get('tag'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context


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

def search(request):
    review = Review.objects.all()
    # GET request의 인자중에 searchword값이 있으면 가져오고, 없으면 빈 문자열 넣기
    if request.method == "GET":
        searchword = request.GET.get('searchword', '')
        resultReview = []

        if searchword:  # searchword가 있다면
            searchReview = review.filter(movie_title__contains=searchword)  # 제목에 searchword가 포함된 레코드만 필터링
            if searchReview:
                # 영화 여러개 저장위해 데이터의 개수
                review_count = searchReview.count()
                for c in range(review_count):
                    # 데이터들 resultMovie리스트에 저장
                    # 원본 주석처리
                    # resultMovie.append({searchMovie[c].title:searchMovie[c].id})
                    resultReview.append({'title': searchReview[c].title, 'id': searchReview[c].id})
                    # 디테일 페이지 이동위해 id값도 넘겨준다
                return render(request, 'review/searchresult.html',
                              {'movie': review, 'searchMovie': searchReview, 'resultMovie': resultReview})
            else:
                # 아무것도 입력하지 않는다면,
                return render(request, 'movies/searchresult.html', {'resultMovie': resultReview})

        return render(request, 'movies/search.html')
    # mainpage에서는
    # <검색기능>작품의 제목,배우,감독을 검색해 해당 영화의 디테일 페이지로 연결하는 역할을 한다.
    # 일단 작품의 제목으로 검색하는 것을 구현
    # <로그인버튼>