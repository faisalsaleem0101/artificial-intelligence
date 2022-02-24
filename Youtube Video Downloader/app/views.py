
from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import urllib.request as url_request
from pytube import YouTube
from pathlib import Path
import os


def index(request):
    return render(request, "index.html")


def storeLink(request):
    context = {
        "video_resolutions" : [],
        "videos" : [],
        "indexes" : [],
        "message" : "",
        "type" : "",
        "link" : ""
    }

    if request.method == "POST":
        url = request.POST["link"]

        if(len(url) > 0):
            try:
                youtube = YouTube(url)
                links = youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

                context["videos"] = links
                context["link"] = url

                context["type"] = "success"
                context["message"] = "Success"  
            except:
                context["type"] = "danger"
                context["message"] = "Something went wrong"
        else:
            context["type"] = "danger"
            context["message"] = "Link is required"    
    else:
        context["type"] = "danger"
        context["message"] = "Get Method not allowed"

    return render(request, "result.html", context=context)


def downloadLink(request):
    
    path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))

    
    
    if request.method == "GET":
        try:
            url = str(request.GET["link"]).strip()
            res = str(request.GET["res"])

            youtube = YouTube(url)
            links = youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            video = None
            for video in links:
                if video.resolution == res:
                    video = video
                    break
            
            if video != None:
                video.download(path_to_download_folder)

            return HttpResponse("Video downloaded successfully!")    
        except:
            return HttpResponse("Something went wrong")    
    else:
        return HttpResponse("Something went wrong")    
    
    