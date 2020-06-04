from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import AnimeTitle
from django.contrib import messages
from .filters import indexFilter

# Create your views here.
#################################    TESTING PAGES    #################################
def testing(request):
    return render(request, "testingPage.html")

def testing2(request):
    anime_list_item = AnimeTitle.objects
    context = {
    'animes':anime_list_item,
    }
    return render(request, "testingPage2.html", context)

def testing3(request,anime_id):
    Anime_object = get_object_or_404(AnimeTitle, pk=anime_id)
    return render(request,"animeTitle.html",{'Anime':Anime_object})


#################################    OFFICIALLY USEABLE PAGES    #################################
def animeTitle(request,anime_id):
    Anime_object = get_object_or_404(AnimeTitle, pk=anime_id)
    Ep_plus_Link = zip(Anime_object.AnimeEpisodes(),Anime_object.AnimeEpisodesLink())
    context = {
    'Anime':Anime_object,
    'Ep_plus_Link':Ep_plus_Link

    }
    return render(request,"animeTitle.html",context)


def start(request):
    return render(request, "startPage.html")


def main(request):
    anime_list_item = AnimeTitle.objects
    context = {
    'animes':anime_list_item,
    }
    return render(request, "mainPage.html" , context)

def animeIndexes(request):
    anime_list_item = AnimeTitle.objects
    context = {
    'animes':anime_list_item,
    }
    return render(request, "animeIndexPage.html" , context)

def animeIndexesfilter(request):
    querry = request.GET['shortlist']
    searchAnime = AnimeTitle.objects.filter(genres__icontains=querry)
    context = {
    'animes':searchAnime,
    'querry':querry,
    }
    return render(request, "animeIndexPage.html", context)



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

def searchGenre(request):
    querry = request.GET['querry1']
    print(querry)
    querrys = querry.split()
    searchAnime = AnimeTitle.objects.filter(genres__icontains=querry)
    for i in querrys:
        searchAnime = searchAnime.union(AnimeTitle.objects.filter(genres__icontains=i))
    print(querrys)
    context = {
    'animes':searchAnime,
    'querry':querry,
    }
    return render(request, "searchPage.html", context)
    # return HttpResponse("A webpage")
