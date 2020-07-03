"""AnimeBUFF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import animetitles.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('animetitle/<int:anime_id>/', animetitles.views.animeTitle, name="animeTitle"),
    path('video/<int:Anime_id>/<int:video_id>', animetitles.views.video, name="video"),
    path('animetitle/',animetitles.views.main , name="main"),
    path('', animetitles.views.start, name="start"),
    path('search/', animetitles.views.search, name="search"),
    path('searchByGenre/', animetitles.views.searchGenre, name="searchGenre"),
    path('animetitle/randomise/', animetitles.views.randomise, name="randomise"),
    path('animetitle/notify/', animetitles.views.notify, name="notify"),
    path('welcomePage/', animetitles.views.welcomePage),

###################################################    TESTING PAGES URLS ##############################
    path('testing/', animetitles.views.testing, name="testing"),
    path('testing2/', animetitles.views.testing2, name="testing2"),
    path('testing3/<int:anime_id>/', animetitles.views.testing3, name="testing3"),
    path('testing4/<path:video_id>', animetitles.views.testing4, name="testing4"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
