from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import AnimeTitle
from django.contrib import messages
from .filters import indexFilter
import random
import os
import subprocess


# Create your views here.
#################################    TESTING PAGES    #################################
def testing(request):
    return render(request, "testingPage.html")

def testing2(request):

    if AnimeTitle.objects.exists():
        lastInsertedAnimeId = AnimeTitle.objects.last().id
        RandomAnimeList = []
        while(len(RandomAnimeList) < 3):
            k = random.randrange(0,int(lastInsertedAnimeId)+1)
            if AnimeTitle.objects.filter(id=k).exists():
                #print("#print the index    :",k)
                if k not in RandomAnimeList:
                    RandomAnimeList.append(k)
            if len(AnimeTitle.objects.all()) < 3:
                return render(request, "DatabaseEmpty.html")
        #print("RandomAnimeList    :",RandomAnimeList)

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
                #print("LatestAnimeIndex    :",LatestAnimeIndex)
            LatestAnimeIndex-=1
        for i in range(0,20):
            if i in range(0,len(ListOfLatestAnimes)):
                LatestObjests.append(get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[i]))
            else:
                LatestObjests.append(AnimeTitle(id="0",title="Add More Anime to fillspace",summery="",profile="asd"
                ,extrapick_1="asd",extrapick_2="asd",extrapick_3="asd",extrapick_4="asd"))

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sN = open(BASE_DIR+"\\recentlyWatched.qaw",'r')
        recently_watched = sN.readline()
        sN.close()
        recently_watched = list(list(map(int, recently_watched.split())))
        #print(recently_watched)
        recent_Anime = []
        for i in recently_watched:
            recent_Anime.append(get_object_or_404(AnimeTitle, pk=i))
        #print(recent_Anime)

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

        'recent_1':recent_Anime[0],
        'recent_2':recent_Anime[1],
        'recent_3':recent_Anime[2],
        'recent_4':recent_Anime[3],
        'recent_5':recent_Anime[4],
        'recent_6':recent_Anime[5],
        'recent_7':recent_Anime[6],
        'recent_8':recent_Anime[7],
        'recent_9':recent_Anime[8],
        'recent_10':recent_Anime[9],
        }
        #print("ALL INDIVIDUAL OBJECTS")
        #return render(request, "DatabaseEmpty.html")
        return render(request, "testingpage2.html", context)
    else:
        return render(request, "DatabaseEmpty.html")

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
    if Anime_object.noOfEPs() == "Dir Deleted":

        return HttpResponse("This anime Directory Doesnot exist in the Computer _ Enter correct path and try Again")

    epList=Anime_object.AnimeEpisodes()
    epListRange = []
    for i in range(0,len(epList)):
        epListRange.append(i)
    Ep_plus_Link = zip(epList,epListRange)
    #Anime_object_summary = Anime_object.summery
    #Anime_object_summary = Anime_object_summary.replace("\n","")
    context = {
    #'Anime_object_summary':Anime_object_summary,
    'Anime':Anime_object,
    'Ep_plus_Link':Ep_plus_Link

    }
    return render(request,"animeTitle.html",context)


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
                #print("#print the index    :",k)
                if k not in RandomAnimeList:
                    RandomAnimeList.append(k)
            if len(AnimeTitle.objects.all()) < 3:
                return render(request, "DatabaseEmpty.html")
        #print("RandomAnimeList    :",RandomAnimeList)

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
                #print("LatestAnimeIndex    :",LatestAnimeIndex)
            LatestAnimeIndex-=1
        for i in range(0,20):
            if i in range(0,len(ListOfLatestAnimes)):
                LatestObjests.append(get_object_or_404(AnimeTitle, pk=ListOfLatestAnimes[i]))
            else:
                LatestObjests.append(AnimeTitle(id="0",title="Add More Anime to fillspace",summery="",profile="asd"
                ,extrapick_1="asd",extrapick_2="asd",extrapick_3="asd",extrapick_4="asd"))

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sN = open(BASE_DIR+"\\recentlyWatched.qaw",'r')
        recently_watched = sN.readline()
        sN.close()
        recently_watched = list(list(map(int, recently_watched.split())))
        #print(recently_watched)
        recent_Anime = []
        for i in recently_watched:
            recent_Anime.append(get_object_or_404(AnimeTitle, pk=i))
        #print(recent_Anime)

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

        'recent_1':recent_Anime[0],
        'recent_2':recent_Anime[1],
        'recent_3':recent_Anime[2],
        'recent_4':recent_Anime[3],
        'recent_5':recent_Anime[4],
        'recent_6':recent_Anime[5],
        'recent_7':recent_Anime[6],
        'recent_8':recent_Anime[7],
        'recent_9':recent_Anime[8],
        'recent_10':recent_Anime[9],
        }
        #print("ALL INDIVIDUAL OBJECTS")
        #return render(request, "DatabaseEmpty.html")
        return render(request, "startPage.html", context)
    else:
        return render(request, "DatabaseEmpty.html")

def video(request, Anime_id, video_id):
    Anime_object = get_object_or_404(AnimeTitle, pk=Anime_id)
    video_urls = Anime_object.AnimeEpisodesLink()
    video_url = video_urls[video_id]
    if video_id == 0:
        prev = -1
    if video_id > 0 :
        prev = video_id - 1
    if video_id == (int(Anime_object.noOfEPs())-1):
        next = -1
    if video_id < (int(Anime_object.noOfEPs())-1):
        next = video_id + 1
    video_NAME = Anime_object.AnimeEpisodes()[video_id]
    video_Public_Url = str(video_url)
    video_Public_Url = "http://192.168.43.57"+video_Public_Url[16:]

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sN = open(BASE_DIR+"\\recentlyWatched.qaw",'r')
    recently_watched = sN.readline()
    sN.close()
    recently_watched = list(list(map(int, recently_watched.split())))
    if Anime_id not in recently_watched:
        popped = recently_watched.pop()
        recently_watched.insert(0,Anime_id)
        test_list = [str(i) for i in recently_watched]
        convert_to_str = ' '.join(test_list)
        sN = open(BASE_DIR+"\\recentlyWatched.qaw",'w')
        sN.write(convert_to_str)
        sN.close()

    #print("video_Public_Url +++++ ",video_Public_Url)
    context = {
    'EP_name': video_NAME,
    'Anime_id': Anime_id,
    'video':video_url,
    'video_Public_Url':video_Public_Url,
    'prev' : prev,
    'next' : next,
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
    #print(querry)
    querrys = querry.split()
    searchAnime = AnimeTitle.objects.filter(genres__icontains=querry)
    for i in querrys:
        searchAnime = searchAnime.union(AnimeTitle.objects.filter(genres__icontains=i))
    #print(querrys)
    context = {
    'animes':searchAnime,
    'querry':querry,
    }
    return render(request, "searchPage.html", context)
    # return HttpResponse("A webpage")

def notify(request,optional_parameter=''):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ###  NEED TO LEARN THIS FORM BELOW #####
    ### If the user tries to Change the Avoid LIst in the Below section
    querry = request.GET.get('avoidList', False)
    if querry is not False:

        sN = open(BASE_DIR+"\\Dir_Avoid.qaw",'w')
        sN.write(str(querry).replace("\r\n",","))
        sN.close()
    #If User tries to change the File manually by opening the notepad
    if optional_parameter == "openAFileInNotepad":
        subprocess.Popen(["notepad.exe",BASE_DIR+"\\Dir_Avoid.qaw"])

    # Reading the file that stores the location of the Anime Folders
    fileOpen = open(BASE_DIR+"\\AnimeLocation.txt",'r')
    Anime_dir = fileOpen.readline()
    fileOpen.close()
    # making list of all ITEMS in the folder   -- >  AllDirs = os.listdir(Anime_dir)
    #
    # making list of all DIRECTORY in theat folder
    allDirs = [ name for name in os.listdir(Anime_dir) if os.path.isdir(os.path.join(Anime_dir, name)) ]

    ###### The Former way of Utracking the REGESTERDED Anime -->  SLOW O(i*(j^2))
    ###
    ###    #print(registeredDirectoryAddresses)
    ###    for i in allDirs:
    ###        for j in AnimeTitle.objects.all():
    ###            ##print(f"Checkin for {i} in Object {j}")
    ###            if i in j.directory_address:
    ###                Registered.append(i)
    ###                break
    ###
    ###

    ##### NEW way of tracking REGISTERED Anime  --> Faster  O(i*j)

    # LIST of all the anime that are registered ....
    registeredDirectoryAddresses = [j.directory_address for j in AnimeTitle.objects.all()]
    Registered = []
    for i in allDirs:
        #print("if DIr name  :",Anime_dir+i)
        if Anime_dir+i in registeredDirectoryAddresses:
            Registered.append(i)

    Deleted_Anime = []

    Avoid_folder = []
    csv_reader = ""
    try:
        with open(BASE_DIR+"\\Dir_Avoid.qaw", 'r') as csv_file:
            csv_reader = csv_file.read()
            Avoid_folder = csv_reader.split(",")
            if "album.css" in Avoid_folder:
                Avoid_folder = Avoid_folder.remove("album.css")
    except:
        c = open(BASE_DIR+"\\Dir_Avoid.qaw", 'w')
        c.close()
        with open(BASE_DIR+"\\Dir_Avoid.qaw", 'r') as csv_file:
            csv_reader = csv_file.read()
            Avoid_folder = csv_reader.split(",")
            if "album.css" in Avoid_folder:
                Avoid_folder = Avoid_folder.remove("album.css")
    #print(Avoid_folder)
    if optional_parameter == '':
        pass
        #print("DoinNothin")
    elif optional_parameter == 'openAFileInNotepad':
        pass
        #print("DoinNothin")
    elif optional_parameter == 'clearTheWholeFrikinStuff_IwantItClean':
        fileOpen = open(BASE_DIR+"\\Dir_Avoid.qaw",'w')
        fileOpen.close()
    elif optional_parameter in Avoid_folder:
        pass
        #print("DoinNothin")
    elif optional_parameter == "album.css":
        pass
        #print("DoinNothin")
    else:
        #print("=======",optional_parameter)
        fileOpen = open(BASE_DIR+"\\Dir_Avoid.qaw",'a')
        fileOpen.write(optional_parameter+",")
        fileOpen.close()
        Avoid_folder.append(optional_parameter)
    with open(BASE_DIR+"\\Dir_Avoid.qaw", 'r') as csv_file:
        csv_reader = csv_file.read()
        Avoid_folder = csv_reader.split(",")
        if "album.css" in Avoid_folder:
            Avoid_folder = Avoid_folder.remove("album.css")
    #print("AVOID FOLDER _____  ",Avoid_folder)
    Unregistered = set(allDirs) - set(Registered)
    Unregistered = set(Unregistered) - set(Avoid_folder)
    Unregistered = list(Unregistered)
    Unregistered.sort()
    Unregistered_add = [Anime_dir+i for i in Unregistered ]
    Unregistered_links = zip(Unregistered,Unregistered_add)

    for j in AnimeTitle.objects.all():
        if j.noOfEPs() == 0:
            Deleted_Anime.append(get_object_or_404(AnimeTitle, pk=j.id))
        if j.noOfEPs() == "Dir Deleted":
            Deleted_Anime.append(get_object_or_404(AnimeTitle, pk=j.id))
    with open(BASE_DIR+"\\Dir_Avoid.qaw", 'r') as csv_file:
        csv_reader = csv_file.read()
    csv_reader = csv_reader.replace(",","\n")
    context = {
    'Deleted_Anime':Deleted_Anime,
    'Unregistered':Unregistered,
    'Registered':Registered,
    'Unregistered_links':Unregistered_links,
    'Avoid_folder':csv_reader,
    'AvoidFile':BASE_DIR+"\\Dir_Avoid.qaw",
    }
    #return HttpResponse(f"The info here includes <br><br> Registered Anime  _  -  _  {Registered}<br><br> Unregistered Anime  _  -  _  {Unregistered} <br><br> Deleted Anime  _  -  _  {Deleted_Anime}")
    return render(request, "notifyPage.html", context)
