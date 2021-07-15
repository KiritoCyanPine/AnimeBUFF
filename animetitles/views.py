from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import AnimeTitle
from django.contrib import messages
from django.http import JsonResponse
import random
import os
import cv2
import re
import subprocess
import threading, socket
from mal import Anime
from shutil import which


def generateOSTthumbnail():
    OSTstorage = os.path.join(AnimeFileLocation(),"[]Anime_OST")
    new_dir = os.path.join(OSTstorage, 'thumbnail')
    try:
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
            print("this created a dir")
    except OSError:
        print("that directory already exists..")

    vid_list_url = [os.path.join(OSTstorage, i) for i in os.listdir(OSTstorage)
                    if '.mkv' in i or '.mp4' in i or '.webm' in i]
    vid_list = [i for i in os.listdir(OSTstorage) if '.mkv' in i or '.mp4' in i or '.webm' in i]
    vid_list_plus_url = zip(vid_list, vid_list_url)

    for i, j in vid_list_plus_url:
        try:
            currentframe = 0
            pic_name = (os.path.join(os.path.join(OSTstorage, 'thumbnail'), i) + '.jpg')
            if os.path.exists(pic_name):
                continue
            cam = cv2.VideoCapture(j)
            f_p_s = cam.get(cv2.CAP_PROP_FPS)
            cam.set(cv2.CAP_PROP_POS_FRAMES, f_p_s*5)
            ret, frame = cam.read()
            cv2.imwrite(pic_name, frame)
            thumb_dir = os.listdir(new_dir)
            for l in thumb_dir:
                if l[:-4] not in vid_list:
                    #print("l[:-4]", l[:-4])
                    #print(os.path.join(new_dir, l))
                    #print(pic_name)
                    os.rename(os.path.join(new_dir, l), pic_name)
            cam.release()
            cv2.destroyAllWindows()
        except FileExistsError:
            print("+++++++++++++++++++ FILE EXISTS ERROR +++++++++++++++")
            pass

def AnimeFileLocation():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        fileOpen = open(BASE_DIR+"\\AnimeLocation.txt",'r')
        Anime_dir = fileOpen.readline()
        fileOpen.close()
    except:
        fileOpen = open(BASE_DIR+"\\AnimeLocation.txt",'r')
        Anime_dir = fileOpen.readline()
        fileOpen.close()
    return Anime_dir


def collectOST():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    anime_dir = AnimeFileLocation()
    osts_dir = anime_dir+"[]Anime_OST"
    ost_list = [i for i in os.listdir(osts_dir) if  ".mkv" in i or ".mp4" in i or".webm" in i or ".avi" in i ]
    #print(ost_list)
    file = open(BASE_DIR+"\\Ost_list.qwa",'w',encoding='utf-8')
    file.close()
    file = open(BASE_DIR+"\\Ost_list.qwa",'a',encoding='utf-8')
    for i in ost_list:
        file.write(i+"\n")
    file.close()

def Subtitle(Anime_object,video_id):
    from distutils.spawn import find_executable
    if find_executable('mkvextract') is None:
        return "Package not found"
    PATH_TO_STATIC = "D:\programming\Tutorial_Django\AnimeBUFF-project\AnimeBUFF\static\SubtitlesForAnime.vtt"
    video_NAME = Anime_object.AnimeEpisodes()[video_id]
    print("VIDNAME::" , Anime_object.directory_address+"\\"+video_NAME+".mkv")
    video_directory_address = Anime_object.directory_address+"\\"+video_NAME+".mkv"
    commandEmulate = 'mkvmerge "'+video_directory_address+'" -i '
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    print(commandEmulate)
    try:
        proc = subprocess.check_output(f'{commandEmulate}', startupinfo=si)
        proc=str(proc)
        proc = proc.split(r'\r\n')
        audio = 0
        for i in proc:
            if 'audio' in i:
                audio+=1
            if 'subtitles' in i:
                k = i
                break
        if audio>=2:
            return False
        a = re.findall(r'[0-9]+', k)
        mkvSubtitle = 'mkvextract tracks "'+video_directory_address+'" '+a[0]+':subs.ass && ass-to-vtt subs.ass > "'+PATH_TO_STATIC+'"'
        print(mkvSubtitle)
        os.system(f'cmd /c "{mkvSubtitle}"')
        subtitle_present = True
    except:
        subtitle_present = False
    return subtitle_present

def AJAX_playInVLC(request):
    def play_VLC(video_address):
        os.system(f'cmd /c "vlc -Iskins {video_address}"')
    try:
        anime_id = request.GET["animeID"]
        video_id = request.GET["videoID"]
        Anime_object = get_object_or_404(AnimeTitle, pk=int(anime_id))
        video_NAME = Anime_object.VidList()[int(video_id)]
        video_address = '"'+Anime_object.directory_address+"\\"+video_NAME+'"'
        try:
            t1 = threading.Thread(target=play_VLC, args=(video_address,))
            t1.start()
        except:
            print("**VLC THREAD NOT ANSWERING**")
        #play_VLC(video_address)
        return JsonResponse({"message":"opening VLC Media Player..."})
    except:
        return JsonResponse({"message":"video could not be played in VLC"})


def AJAX_autoPlay(request):
    if request.is_ajax() and request.method == 'POST':
        k=open("autoplay.ini", 'r')
        ins = k.read()
        k.close()
        if ins == "1":
            k=open("autoplay.ini", 'w')
            k.write("0")
            k.close()
            return JsonResponse({"changeShowAgainVar":"false"})
        else:
            k=open("autoplay.ini", 'w')
            k.write("1")
            k.close()
            return JsonResponse({"changeShowAgainVar":"true"})

    else:
        return JsonResponse({"message":"nothing changed"})


def AJAX_folderManager(request):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ###  NEED TO LEARN THIS FORM BELOW #####
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
    with open(BASE_DIR+"\\Dir_Avoid.qaw", 'r') as csv_file:
        csv_reader = csv_file.read()
        Avoid_folder = csv_reader.split(",")
        if "album.css" in Avoid_folder:
            Avoid_folder = Avoid_folder.remove("album.css")
    ##print("AVOID FOLDER _____  ",Avoid_folder)
    Unregistered = set(allDirs) - set(Registered)
    Unregistered = set(Unregistered) - set(Avoid_folder)
    Unregistered = list(Unregistered)
    Unregistered.sort()
    Unregistered_add = [Anime_dir+i for i in Unregistered ]
    Unregistered_links = zip(Unregistered,Unregistered_add)

    for j in AnimeTitle.objects.all():
        if j.noOfEPs() == 0:
            Deleted_Anime.append(j.id)
        if j.noOfEPs() == "Dir Deleted":
            Deleted_Anime.append(j.id)

    Deleted_Anime_Name = [get_object_or_404(AnimeTitle, pk=i).title for i in Deleted_Anime]
    print(Deleted_Anime_Name)
    context = {
    'Deleted_Anime_Name':Deleted_Anime_Name,
    'Deleted_Anime':Deleted_Anime,
    'Unregistered':Unregistered,
    'Registered':Registered,
    'Unregistered_links':Unregistered_add,
    }
    return JsonResponse(context)


def AJAX_getDataFromMal(request, animeId):
    Anime_object = get_object_or_404(AnimeTitle, pk=animeId)
    mal_id = Anime_object.mal_anime_link.split('/')
    try:
        for l in mal_id:
            if l.isnumeric():
                mal_id = l
                break
        mal_Anime = Anime(int(mal_id))
        score = mal_Anime.score
        scoreForPie = int((float(score)/10)*360)
        scoreForPieALT = 360 - scoreForPie
        if float(score) > 7.2:
            score_color = ' 54 ,256 , 54'
        else:
            score_color = '256 ,256 , 256'
        popularity = mal_Anime.popularity
        status = mal_Anime.status
        rating = mal_Anime.rating
        studios = mal_Anime.studios
        rank = mal_Anime.rank

        print("###########\n",score, popularity,status,mal_Anime)
        context = {
        'score':score,
        'popularity':popularity,
        'status':status,
        'rating':rating,
        'studios':studios,
        'scoreForPie':scoreForPie,
        'scoreForPieALT':scoreForPieALT,
        'score_color':score_color,
        'rank':rank,
        }
    except Exception:
        pass
    return JsonResponse(context)

# Create your views here.
#################################    TESTING PAGES    #################################
def testing(request,optional_parameter=''):
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
    ##print("AVOID FOLDER _____  ",Avoid_folder)
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
    return render(request, "testingPage.html", context)


def testing2(request):
    try:
        t1 = threading.Thread(target=collectOST)
        t1.start()
    except:
        print("THear is some problem in OST_LIST creation")

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
    deleteOldImages()
    Anime_object = get_object_or_404(AnimeTitle, pk=anime_id)
    return render(request,"testingPage3.html",{'Anime':Anime_object})

def testing4(request, video_id):
    context = {
    'video':video_id,
    }
    return render(request, "testingPage4.html", context)

#################################    OFFICIALLY USEABLE PAGES    #################################


def deleteOldImages():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    imagesInUse =[]
    for i in AnimeTitle.objects.all():
        if i.profile:
            imagesInUse.append(i.profile.path)
        if i.extrapick_1:
            imagesInUse.append(i.extrapick_1.path)
        if i.extrapick_2:
            imagesInUse.append(i.extrapick_2.path)
        if i.extrapick_3:
            imagesInUse.append(i.extrapick_3.path)
        if i.extrapick_4:
            imagesInUse.append(i.extrapick_4.path)
        if i.extrapick_5:
            imagesInUse.append(i.extrapick_5.path)
        if i.extrapick_6:
            imagesInUse.append(i.extrapick_6.path)

    PATH_TO_MEDIA_IMAGES = "D:\\programming\\Tutorial_Django\\AnimeBUFF-project\\media\\images\\"
    allImages = [PATH_TO_MEDIA_IMAGES+i for i in os.listdir(BASE_DIR+"\media\images") if ".jpg" in i or ".png" in i or ".jpeg" in i or ".webp" in i ]
    imagesInUse = set(imagesInUse)
    allImages = set(allImages)
    print("imagesInUse" ,"LENGTH  =  " ,len(imagesInUse))
    print("allImages","LENGTH  =  ",len(allImages))
    DBdeletedImages = allImages.difference(imagesInUse)
    print("DBdeletedImages" , "LENGTH  =  ",len(DBdeletedImages))
    dele = open("deletedimages.txt",'w',encoding='utf8')
    dele.close()
    dele = open("deletedimages.txt",'a',encoding='utf8')
    for i in DBdeletedImages:
        dele.write(i+"\n")
    dele.close()
    for i in DBdeletedImages:
        os.remove(i)

def welcomePage(request):
    return render(request, "DatabaseEmpty.html")

def AnimeOST(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    anime_dir = AnimeFileLocation()
    listOfVids = []
    listOfVidsLink = []
    listOfVidsThumbnail = []
    count = 0
    numbers = []
    with open(BASE_DIR+"\\Ost_list.qwa", 'r' , encoding="utf-8") as target:
        for line in target:
            currentPlace = line[:-1]
            if ".mp4" in currentPlace or ".mkv" in currentPlace:
                name=currentPlace[:-4]
                listOfVids.append(name)
            elif ".webm" in currentPlace:
                name=currentPlace[:-5]
                listOfVids.append(name)
            listOfVidsLink.append("http://127.0.0.1:11111/[]Anime_OST/"+currentPlace)
            listOfVidsThumbnail.append("http://127.0.0.1:11111/[]Anime_OST/"+"thumbnail/"+currentPlace+".jpg")
            numbers.append(count)
            count+=1
    Ep_plus_Link = zip(listOfVids,listOfVidsLink,numbers,listOfVidsThumbnail)
    context = {
        'Ep_plus_Link':Ep_plus_Link,
        'count':count,
    }
    return render(request, "AnimeOST.html", context)


def animeTitle(request,anime_id):
    Anime_object = get_object_or_404(AnimeTitle, pk=anime_id)
    if Anime_object.noOfEPs() == "Dir Deleted":

        return HttpResponse("This anime Directory Doesnot exist in the Computer _ Enter correct path and try Again")

    epList=Anime_object.AnimeEpisodes()
    epListRange = []
    for i in range(0,len(epList)):
        if i == Anime_object.watchCurrEp:
            currentEpName = epList[i]
        epListRange.append(i)
    Ep_plus_Link = zip(epList,epListRange)
    #Anime_object_summary = Anime_object.summery
    #Anime_object_summary = Anime_object_summary.replace("\n","")
    context = {
    #'Anime_object_summary':Anime_object_summary,
    'Anime':Anime_object,
    'currentEpName':currentEpName,
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
    OSTstorage = os.path.join(AnimeFileLocation(),"[]Anime_OST")
    try:
        t1 = threading.Thread(target=collectOST)
        t1.start()
        if os.path.exists(OSTstorage):
            t2 = threading.Thread(target=generateOSTthumbnail)
            t2.start()
    except:
        print("THear is some problem in OST_LIST creation")

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

        courasel_1 = AnimeTitle.objects.filter(id=RandomAnimeList[0]) #  14
        courasel_2 = AnimeTitle.objects.filter(id=RandomAnimeList[1]) #  316
        courasel_3 = AnimeTitle.objects.filter(id=RandomAnimeList[2]) #  315
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
            try:
                recent_Anime.append(get_object_or_404(AnimeTitle, pk=i))
            except:
                try:
                    #recent_Anime.append(get_object_or_404(AnimeTitle, pk=recently_watched[recently_watched.index(i)+1]))
                    recent_Anime.append(AnimeTitle(id= 0 , title="This Anime Has Been Removed from your device"))
                except:
                    print("A recently watched anime was deleted replacing with previous anime",recently_watched[recently_watched.index(i)-2])
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
    #PC_IP = str(socket.gethostbyname(socket.getfqdn()))
    PC_IP = "localhost"
    Anime_object = get_object_or_404(AnimeTitle, pk=Anime_id)
    video_urls = Anime_object.AnimeEpisodesLink()
    video_url = video_urls[video_id]
    if video_id == 0:
        prev = -1
    if video_id > 0 :
        prev = video_id - 1
    if video_id == (int(Anime_object.noOfEPs())-1):
        next = -1
        VideoPostroll = "-1"  #   Postroll dosent exist  --> this is the last video
    if video_id < (int(Anime_object.noOfEPs())-1):
        next = video_id + 1  # finding the next video ID

        ##  finding out if next video Exists and Generating Url##
        #k = request.META['HTTP_REFERER']
        #k=k[::-1]
        #slashOut = 0
        #for i in k:
        #    if i == "/":
        #        if slashOut == 3:
        #            break
        #        slashOut = slashOut + 1
        #        k = k [1:]
        #k = k[::-1]    #  this will give the first part --> http://localhost:8123/video/
        VideoPostroll = "http://"+PC_IP+":8123"+"/video/"+str(Anime_id)+"/"+str(next)   # this will give url like   http://localhost:8123/video/20/134 ## "VideoPostroll = k+str(Anime_id)+"/"+str(next)"
        ##  Url generation ends
    video_NAME = Anime_object.AnimeEpisodes()[video_id]
    video_Public_Url = str(video_url)
    video_Public_Url = PC_IP+video_Public_Url[16:]
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
    else:
        recently_watched.remove(Anime_id)
        recently_watched.insert(0,Anime_id)
        test_list = [str(i) for i in recently_watched]
        convert_to_str = ' '.join(test_list)
        sN = open(BASE_DIR+"\\recentlyWatched.qaw",'w')
        sN.write(convert_to_str)
        sN.close()
    Anime_object.watchCurrEp = video_id
    Anime_object.save()
    print("######  ::  ",video_id)

    ##########################  TO Create SUBTITLES FOR THE VIDEO ##################################################
    PATH_TO_STATIC = "D:\programming\Tutorial_Django\AnimeBUFF-project\AnimeBUFF\static\SubtitlesForAnime.vtt"
    subtitle_present = False
    if 'SubtitlesForAnime.vtt' in os.listdir(PATH_TO_STATIC[:-21]):
        os.remove(PATH_TO_STATIC)
    if '.mkv' in video_url:
        subtitle_present = Subtitle(Anime_object, video_id)
        if subtitle_present == "Package not found":
            subtitle_present = False
            MSG = "MKV NIX TOOLS is not found... you will not be able to view subtitles..."
        else:
            MSG = ''
    else:
        MSG = ''

    ########################## END :::  TO Create SUBTITLES FOR THE VIDEO ##################################################
    k=open("autoplay.ini", 'r')
    autoplaySymbol = k.read()
    k.close()
    vlc_available = which("vlc") is not None

    #print("video_Public_Url +++++ ",video_Public_Url)

    context = {
    'video_id':video_id,
    'EP_name': video_NAME,
    'Anime_id': Anime_id,
    'video':video_url,
    'video_Public_Url':video_Public_Url,
    'prev' : prev,
    'next' : next,
    'subtitle_present':subtitle_present,
    'MSG':MSG,
    'VideoPostroll':VideoPostroll,
    'autoplaySymbol':autoplaySymbol,
    'vlc_available':vlc_available,
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
    ##print("AVOID FOLDER _____  ",Avoid_folder)
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
