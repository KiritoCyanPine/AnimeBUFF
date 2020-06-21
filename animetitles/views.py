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

def testing4(request, video_id):
    context = {
    'video':video_id,
    }
    return render(request, "testingPage4.html", context)


#################################    OFFICIALLY USEABLE PAGES    #################################

def welcomePage(request):
    return render(request, "DatabaseEmpty.html")

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
    if AnimeTitle.objects.exists():
        lastInsertedAnimeId = AnimeTitle.objects.last().id
        RandomAnimeList = []
        while(len(RandomAnimeList) < 3):
            k = random.randrange(0,int(lastInsertedAnimeId)+1)
            if AnimeTitle.objects.filter(id=k).exists():
                print("print the index    :",k)
                if k not in RandomAnimeList:
                    RandomAnimeList.append(k)
            if len(AnimeTitle.objects.all()) < 3:
                return render(request, "DatabaseEmpty.html")
        print("RandomAnimeList    :",RandomAnimeList)
        courasel_1 = AnimeTitle.objects.filter(id=RandomAnimeList[0])
        courasel_2 = AnimeTitle.objects.filter(id=RandomAnimeList[1])
        courasel_3 = AnimeTitle.objects.filter(id=RandomAnimeList[2])
        LatestAnimeIndex = lastInsertedAnimeId
        LatestObjests = []
        ListOfLatestAnimes = []
        while len(ListOfLatestAnimes) < 20:
            if LatestAnimeIndex < 1:
                break
            if AnimeTitle.objects.filter(id=LatestAnimeIndex).exists():
                ListOfLatestAnimes.append(LatestAnimeIndex)
                print("LatestAnimeIndex    :",LatestAnimeIndex)
            LatestAnimeIndex-=1
        for i in range(0,20):
            if i in range(0,len(ListOfLatestAnimes)):
                LatestObjests.append(get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[i]))
            else:
                LatestObjests.append(AnimeTitle(id="0",title="Add More Anime to fillspace",summery="",profile="asd",extrapick_1="asd",extrapick_2="asd",extrapick_3="asd",extrapick_4="asd"))
        context = {
        'courasel_1':courasel_1,
        'courasel_2':courasel_2,
        'courasel_3':courasel_3,
        'Latest_1':LatestObjests[0],
        'Latest_2':LatestObjests[1],
        'Latest_3':LatestObjests[2],
        'Latest_4':LatestObjests[3],
        'Latest_5':LatestObjests[4],
        'Latest_6':LatestObjests[5],
        'Latest_7':LatestObjests[6],
        'Latest_8':LatestObjests[7],
        'Latest_9':LatestObjests[8],
        'Latest_10':LatestObjests[9],
        'Latest_11':LatestObjests[10],
        'Latest_12':LatestObjests[11],
        'Latest_13':LatestObjests[12],
        'Latest_14':LatestObjests[13],
        'Latest_15':LatestObjests[14],
        'Latest_16':LatestObjests[15],
        'Latest_17':LatestObjests[16],
        'Latest_18':LatestObjests[17],
        'Latest_19':LatestObjests[18],
        'Latest_20':LatestObjests[19],
        }
        print("ALL INDIVIDUAL OBJECTS")
        #return render(request, "DatabaseEmpty.html")
        return render(request, "startPage.html", context)
    else:
        return render(request, "DatabaseEmpty.html")


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
