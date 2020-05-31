from django.shortcuts import render, get_object_or_404
from .models import AnimeTitle

# Create your views here.

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
