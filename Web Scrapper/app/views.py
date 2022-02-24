
from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import urllib.request as url_request


def index(request):
    return render(request, "index.html")


def storeLink(request):
    context = {
        "data" : '',
        "message" : "",
        "type" : ""
    }

    if request.method == "POST":
        url = request.POST["link"]

        if(len(url) > 0):
            try:
                res = url_request.Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
                page_html = url_request.urlopen(res).read()
                page_sout = BeautifulSoup(page_html, "html.parser")

                context["data"] = page_sout.prettify()
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