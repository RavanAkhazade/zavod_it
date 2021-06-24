from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User, News
from .forms import CreateNews


def index(request):
    all_news = News.objects.all()
    return render(request, "test_exercise/index.html", {
        "all_news": all_news,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "test_exercise/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "test_exercise/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "test_exercise/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "test_exercise/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "test_exercise/register.html")


def statistics(request):
    all_news = News.objects.all().order_by('-views')
    return render(request, "test_exercise/statistics.html", {
        "all_news": all_news,
    })


def add_news(request):
    form = CreateNews(request.POST or None)
    if form.is_valid():
        News.objects.create(author=request.user, title=form.cleaned_data['title'], text=form.cleaned_data['text'], tags=form.cleaned_data['tags'])
        message = "Success!"
        return render(request, "test_exercise/add_news.html", {
            "form": CreateNews(),
            "message": message
        })
    return render(request, "test_exercise/add_news.html", {
        "form": CreateNews(),
    })


def news(request, id):
    news_instance = News.objects.get(id=id)
    news_instance.views += 1  # попытался сделать просмотры уникальными для каждого юзера создав отдельную модель, которая наследует в одном поле user а в другом news
    news_instance.save()  # но в таком случае очень проблемно сортировать посты по просмотрам ( не помогло даже создать отдельный template tag для этих целей)

    return render(request, "test_exercise/news.html", {
        "news": news_instance,
    })
