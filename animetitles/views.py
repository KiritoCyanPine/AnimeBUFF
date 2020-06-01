from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import AnimeTitle
from django.contrib import messages

# Create your views here.

def testing(request):
    return render(request, "testingPage.html")

def animeTitle(request,anime_id):
    Anime_object = get_object_or_404(AnimeTitle, pk=anime_id)
    return render(request,"animeTitle.html",{'Anime':Anime_object})


def start(request):
    return render(request, "startPage.html")


def main(request):
    anime_list_item = AnimeTitle.objects
    context = {
    'animes':anime_list_item,
    }
    return render(request, "mainPage.html" , context)


def start(request):
    return render(request, "startPage.html")


def video(request, video_id):
    context = {
    'video':video_id,
    }
    return render(request, "videoPlayer/index.html", context)

def search(request):
    querry = request.GET['search']
    if len(querry) > 78 :
        searchAnime = []
    else:
        searchAnime = AnimeTitle.objects.filter(title__icontains=querry)
    context = {
    'animes':searchAnime,
    'querry':querry,
    }
    return render(request, "searchPage.html", context)
    # return HttpResponse("A webpage")
