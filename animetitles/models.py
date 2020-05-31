from django.db import models
import os


GLOBAL_server_root_Address = "http://localhost:8887/"


# Create your models here.
class AnimeTitle(models.Model):
    title =  models.CharField(max_length=100)
    profile = models.ImageField(upload_to = "images/")
    summery =  models.TextField()
    trailer = models.CharField(max_length=170)
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

    def FileList(self):
        file_list = os.listdir(self.directory_address)
        print(file_list)
        return file_list

    def VidList(self):
        file_list = os.listdir(self.directory_address)
        vid_list = []
        for i in file_list:
            if ".mp4" in i or ".mkv" in i:
                vid_list.append(i)
        return vid_list


    def AnimeEpisodes(self):
        file_list = os.listdir(self.directory_address)
        vid_list = []
        for i in file_list:
            if ".mp4" in i or ".mkv" in i:
                vid_list.append(i)
        if "trailer.mp4" in vid_list:
            anime_episodes = vid_list.remove("trailer.mp4")
        else :
            anime_episodes = vid_list
        return anime_episodes

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
        if "trailer.mp4" in vid_list:
            anime_episodes = vid_list.remove("trailer.mp4")
        else :
            anime_episodes = vid_list

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
        return anime_episodes_link
