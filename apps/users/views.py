from django.shortcuts import render, redirect
from .models import *
from .. books.models import *
from django.contrib import messages

def index(request):
    return render(request, "users/index.html")

def process(request, action):
    if request.method == "POST":
        if action == "register":
            reg_user = User.objects.reg_validator(request.POST)
            if reg_user['status'] == "bad":
                for error in reg_user['data']:
                    messages.error(request, error)
                    return redirect('/')
            else:
                request.session['user_id'] = reg_user['data'].id
                return redirect('/books')

        elif action == "login":
            log_user = User.objects.log_validator(request.POST)
            if log_user['status'] == "bad":
                messages.error(request, log_user['data'])
                return redirect('/')
            else:
                request.session['user_id'] = log_user['data'].id
                return redirect('/books')

        else:
            return redirect('/')
    else:
        return redirect('/')

def show(request, id):
    context = {
        "user" : User.objects.get(id=id),
        "total_reviews" : Review.objects.filter(reviewer_id = id).count(),
        "reviews" : Review.objects.filter(reviewer_id = id)
    }
    return render(request, 'users/show.html', context)

def logout(request):
    del request.session['user_id']
    return redirect('/')