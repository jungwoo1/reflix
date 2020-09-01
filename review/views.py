from django.shortcuts import render, redirect
from .forms import CreateReview
from .models import Review
# Create your views here.

def reviewList(requset):
    reviews = Review.objects.all()
    return render(requset, 'reviewList.html', {'reviews':reviews})



def createReview(request):

    if request.method == 'POST':
        form = CreateReview(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('review:reviewList')
        else:
            return redirect('movies')
    else:
        form = CreateReview()
        return render(request, 'createReview.html', {'form':form})
