from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import AnimeTitle
from django.contrib import messages
from .filters import indexFilter
import random


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
    anime_list_item = AnimeTitle.objects.order_by('title')
    context = {
    'animes':anime_list_item,
    }
    return render(request, "mainPage.html" , context)


def start(request):
    lastInsertedAnimeId = AnimeTitle.objects.last().id
    RandomAnimeList = []
    while(len(RandomAnimeList) < 3):
        k = random.randrange(1,int(lastInsertedAnimeId))
        if AnimeTitle.objects.filter(id=k).exists():
            if k not in RandomAnimeList:
                RandomAnimeList.append(k)
    courasel_1 = AnimeTitle.objects.filter(id=RandomAnimeList[0])
    courasel_2 = AnimeTitle.objects.filter(id=RandomAnimeList[1])
    courasel_3 = AnimeTitle.objects.filter(id=RandomAnimeList[2])
    LatestAnimeIndex = lastInsertedAnimeId
    ListOfLatestAnimes = []
    while len(ListOfLatestAnimes) < 20:
        if AnimeTitle.objects.filter(id=LatestAnimeIndex).exists():
            ListOfLatestAnimes.append(LatestAnimeIndex)
        LatestAnimeIndex-=1
    Latest_1 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[0])
    Latest_2 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[1])
    Latest_3 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[2])
    Latest_4 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[3])
    Latest_5 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[4])
    Latest_6 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[5])
    Latest_7 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[6])
    Latest_8 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[7])
    Latest_9 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[8])
    Latest_10 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[9])
    Latest_11 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[10])
    Latest_12 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[11])
    Latest_13 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[12])
    Latest_14 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[13])
    Latest_15 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[14])
    Latest_16 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[15])
    Latest_17 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[16])
    Latest_18 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[17])
    Latest_19 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[18])
    Latest_20 = get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[19])
    context = {
    'courasel_1':courasel_1,
    'courasel_2':courasel_2,
    'courasel_3':courasel_3,
    'Latest_1':Latest_1,
    'Latest_2':Latest_2,
    'Latest_3':Latest_3,
    'Latest_4':Latest_4,
    'Latest_5':Latest_5,
    'Latest_6':Latest_6,
    'Latest_7':Latest_7,
    'Latest_8':Latest_8,
    'Latest_9':Latest_9,
    'Latest_10':Latest_10,
    'Latest_11':Latest_11,
    'Latest_12':Latest_12,
    'Latest_13':Latest_13,
    'Latest_14':Latest_14,
    'Latest_15':Latest_15,
    'Latest_16':Latest_16,
    'Latest_17':Latest_17,
    'Latest_18':Latest_18,
    'Latest_19':Latest_19,
    'Latest_20':Latest_20,
    }
    print("ALL INDIVIDUAL OBJECTS")
    return render(request, "startPage.html", context)


def video(request, video_id):
    context = {
    'video':video_id,
    }
    return render(request, "videoPlayer/videoPlayer.html", context)

def search(request):
    querry = request.GET['search']
    if len(querry) > 78 :
        searchAnime = []
    else:
        searchAnimeNAME = AnimeTitle.objects.filter(title__icontains=querry)
        searchAnimeOTHER_NAMES = AnimeTitle.objects.filter(otherNames__icontains=querry)
        searchAnime = searchAnimeNAME.union(searchAnimeOTHER_NAMES)
    context = {
    'animes':searchAnime,
    'querry':querry,
    }
    return render(request, "searchPage.html", context)
    # return HttpResponse("A webpage")

def randomise(request):
    anime_list_item = AnimeTitle.objects.order_by('?')
    context = {
    'animes':anime_list_item,
    }
    return render(request, "mainPage.html" , context)

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
