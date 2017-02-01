# coding: utf-8
from django.shortcuts import render
from datetime import datetime

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from stravalib.client import Client
from models import Profile
import forms


def index(request):
    #strava_functions.login_strava();
    #client = Client()
    #authorize_url = client.authorization_url(client_id=13966, redirect_uri='http://127.0.0.1:8000/everest_run/authorization/')
    # Have the user click the authorization URL, a 'code' param will be added to the redirect_uri
    # .....
    #url_strava = authorize_url.encode('ascii','ignore')
    url_strava = 'https://www.strava.com/oauth/authorize?client_id=13966&response_type=code&redirect_uri=http://maaxrun.pythonanywhere.com/everest_run/authorization/&scope=write&state=mystate&approval_prompt=force'
    print(type(url_strava))
    date = datetime.now()

    return render(request, 'index.html', locals())

def auth(request):
    client = Client()
    if request.method == "POST":
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            userName = form.cleaned_data["username"]
            userPass = form.cleaned_data["password"]
            userMail = form.cleaned_data["mail"]
            userToken = form.cleaned_data["token"]
            user = User.objects.create_user(userName, userMail, userPass)  # Nous créons un nouvel utilisateur
            user.save()
            profil = Profile(user=user, user_token=userToken)
            profil.save()
    else:
        form = forms.CreateUserForm()
        code = request.GET['code']
        access_token = client.exchange_code_for_token(client_id=13966, client_secret='a67b6efd42d941633fd631b35df2d22ae9b566c1', code=code)

    return render(request, 'auth.html', locals())


def connexion(request):
    error = False

    if request.method == "POST":
        form = forms.ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)

            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                print('connexion ok')
            else: # sinon une erreur sera affichée
                error = True
                print('erreur connexion')
    else:
        form = forms.ConnexionForm()

    return render(request, 'login.html', locals())


def profileView(request):
    username = None
    if request.user.is_authenticated():
        #username = request.user.username
        access_token = request.user.profile.user_token
        client = Client(access_token)
        athlete = client.get_athlete()
        id_runner =athlete.id

        elevation = 0
        best_speed = 0.0
            # Activities can have many streams, you can request desired stream types

        for activity in client.get_activities(after = "2016-01-01T00:00:00Z"):
            #print("{0.distance} {0.moving_time} {0.total_elevation_gain}".format(activity).encode('utf-8'))
            if activity.type == 'Run':
                elevation += float(activity.total_elevation_gain)
                if float(activity.distance)/activity.moving_time.total_seconds()>best_speed:
                    best_speed = float(activity.distance)/activity.moving_time.total_seconds()


        nb_everest = round(elevation/8848,2);
        nb_mtblanc = round(elevation/4809,2);
        best_speed = round(best_speed*3.6,2)
        best_allure = 1/(best_speed/60)
        partie_entiere = int(best_allure)
        partie_decimale = int((best_allure - partie_entiere)*60)
        if partie_decimale<10:
            is_inf10 =  1
        else: is_inf10 = 0
        #best_allure = partie_entiere + partie_decimale
    else:
        print('error')
    return render(request,'profile.html',locals())
