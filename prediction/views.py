from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from urllib3 import HTTPResponse
from prediction.models import userDetails
from prediction.utils import kmeanPrediction
import pandas as pd

# Create your views here.
@csrf_exempt
def render_home(request):
    if request.session.get("username"):
        return render(request, "index.html",{
            "username" : request.session.get("username")
            })
    else:
        return HttpResponseRedirect("/")

@csrf_exempt
def render_login(request):
    return render(request, "logIn.html")

@csrf_exempt
def render_createAccount(request):
    return render(request, "createAccount.html")

@csrf_exempt
def loginUser(request):
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        logProps = userDetails.objects.filter(
            username = username,
            password = password
        )
        request.session["username"] = username
        if logProps:
            return JsonResponse({
                "status": True,
                "username" : request.POST["username"]
            })
        else:
            return JsonResponse({
                "status": False,
            })
@csrf_exempt
def createAccount(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        userProps =  userDetails(
            username = username,
            password = password,
            email = email
        )
        userProps.save()
        return HttpResponseRedirect("/")
@csrf_exempt
def render_results(request):
    dataset  =  request.FILES["dataset"]
    filename = dataset.name
    df =  pd.read_excel(dataset)
    km = kmeanPrediction(df)
    km.cleanData()
    purchase_img_graph = km.plot_purchases()
    purchase_data = km.create_RFM_Quantiles()
    clusters_graph, results = km.plot_clusters()  
    return render(request, "results.html", {
        "purchase_img_graph" : purchase_img_graph,
        "purchase_data"  : purchase_data,
        "clusters_graph" : clusters_graph,
        "results"  : results,
        "filename": filename,
        "username" : request.session.get("username")

    })
