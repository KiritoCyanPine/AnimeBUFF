from django.db import models
import os
import re


# GLOBAL_server_root_Address = "http://192.168.137.1:8887/"
# GLOBAL_server_root_Address = "http://localhost:8887/"
GLOBAL_server_root_Address = "http://127.0.0.1:11111/"
# GLOBAL_server_root_Address = "http://127.0.0.1:8887/"


# Create your models here.
class AnimeTitle(models.Model):
    title =  models.CharField(max_length=100)
    profile = models.ImageField(upload_to = "images/")
    otherNames = models.CharField(max_length=200)
    genres = models.CharField(max_length=200)
    summery =  models.TextField()
    trailer = models.CharField(max_length=170 , blank = True)
    # put blank=True within the brackets
    extrapick_1 = models.ImageField(upload_to = "images/",
                    blank = True)
    extrapick_2 = models.ImageField(upload_to = "images/",
                    blank = True)
    extrapick_3 = models.ImageField(upload_to = "images/",
                    blank = True)
    extrapick_4 = models.ImageField(upload_to = "images/",
                    blank = True)
    extrapick_5 = models.ImageField(upload_to = "images/",
                    blank = True)
    extrapick_6 = models.ImageField(upload_to = "images/",
                    blank = True)

    directory_address =  models.CharField(max_length=175)

    def __str__(self):
        return self.title

    def shortSummery(self):
        if len(self.summery) > 330 :
            return self.summery[0:327]+"..."
        else:
            return self.summery

    def OTHER_NAMES(self):
        if len(self.otherNames) > 100 :
            return self.otherNames[0:97]+"..."
        return self.otherNames

    def FileList(self):
        file_list = os.listdir(self.directory_address)
        file_list.sort(key=natural_keys)
        print(file_list)
        return file_list

    def VidList(self):
        file_list = os.listdir(self.directory_address)
        vid_list = []
        for i in file_list:
            if ".mp4" in i or ".mkv" in i:
                vid_list.append(i)
        vid_list.sort(key=natural_keys)
        return vid_list

    def TrailerVideo(self):
        if self.trailer == "":
            Trailer = False
        else:
            if "watch?v=" in self.trailer:
                Trailer = self.trailer.replace("watch?v=","embed/")
        print(Trailer)
        return Trailer

    def AnimeEpisodes(self):
        file_list = os.listdir(self.directory_address)
        vid_list = []
        for i in file_list:
            if ".mp4" in i or ".mkv" in i:
                vid_list.append(i[:-4])
        if "trailer.mp4" in vid_list:
            anime_episodes = vid_list.remove("trailer.mp4")
        else :
            anime_episodes = vid_list
        anime_episodes.sort(key=natural_keys)
        return anime_episodes

    def noOfEPs(self):
        try:
            file_list = os.listdir(self.directory_address)
            vid_list = []
            for i in file_list:
                if ".mp4" in i or ".mkv" in i:
                    vid_list.append(i)
            if "trailer.mp4" in vid_list:
                anime_episodes = vid_list.remove("trailer.mp4")
            else :
                anime_episodes = vid_list
            number = str(len(anime_episodes))
            return number
        except:
            return "Dir Deleted"

    def DirLink(self):
        diradd = self.directory_address
        p=""
        q=""
        for i in diradd:
            p=i+p
        for i in p:
            if "\\" == i:
                break
            q = i+q
        directory_link = q.replace(" ","%20")
        directory_link = directory_link+"/"
        return directory_link

    def AnimeEpisodesLink(self):
        file_list = os.listdir(self.directory_address)
        vid_list = []
        for i in file_list:
            if ".mp4" in i or ".mkv" in i:
                vid_list.append(i)
        vid_list.sort(key=natural_keys)
        if "trailer.mp4" in vid_list:
            anime_episodes = vid_list.remove("trailer.mp4")
        else :
            anime_episodes = vid_list
        anime_episodes.sort(key=natural_keys)

        diradd = self.directory_address
        p=""
        q=""
        for i in diradd:
            p=i+p
        for i in p:
            if "\\" == i:
                break
            q = i+q
        directory_link = q.replace(" ","%20")
        directory_link = directory_link+"/"

        anime_episodes_link = []
        global GLOBAL_server_root_Address
        for i in anime_episodes:
            anime_episodes_link.append(GLOBAL_server_root_Address+directory_link+i.replace(" ","%20"))
        anime_episodes_link.sort(key=natural_keys)
        print(anime_episodes_link)
        return anime_episodes_link


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)',text) ]

'''    my_list =os.listdir()
    my_list.sort(key=natural_keys)
    print(my_list) '''
