from django.shortcuts import render, redirect
from .models import *
from .. users.models import *

def index(request):
    context = {
        "user" : User.objects.get(id = request.session['user_id']),
        "reviews" : Review.objects.all().order_by("-id")[:3],
        "books" : Book.objects.all()
    }
    return render(request, 'books/index.html', context)

def new_book(request):
    context = {
        "authors" : Author.objects.all()
    }
    return render(request, 'books/new.html', context)

def process(request, action):
    if request.method == "POST":
        if action == "book":
            new_book = Book.objects.book_validator(request.POST)
            if new_book['status'] == "bad":
                for error in new_book['data']:
                    messages.error(request, error)
                    return redirect('/books/new')
            else:
                book_id = new_book['data'].id
                return redirect("/books/show/" + str(book_id))
        elif action == "review":
            new_review = Review.objects.review_validator(request.POST)
            if new_review['status'] == "bad":
                messages.error(request, new_review['data'])
                return redirect('/books/show/' + str(new_review['data'].book_id))
            else:
                return redirect('/books/show/' + str(new_review['data'].book_id))
        else:
            return redirect('/books')
    else:
        return redirect('/books')

def destroy(request, id):
    review = Review.objects.get(id=id)
    book_id = review.book.id
    review.delete()
    return redirect('/books/show/' + str(book_id))

def show(request, id):
    context = {
        "book" : Book.objects.get(id=id),
        "reviews" : Review.objects.filter(book_id = id)
    }
    return render(request, 'books/show.html', context)