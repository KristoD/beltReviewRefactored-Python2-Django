from __future__ import unicode_literals

from django.db import models
from .. users.models import *

class BookManager(models.Manager):
    def book_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        if len(postData['title']) < 2:
            errors.append("Book title must be more than 2 characters!")
        if len(postData['review']) < 10:
            errors.append("Review must be more than 10 characters long!")
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            if 'author_select' in postData:
                author_select = postData['author_select']
            else:
                author_select = ""
            if postData['author'] == "":
                author = Author.objects.get(name = author_select)
                book = Book.objects.create(title = postData['title'], author_id = author.id, uploader_id = postData['id'])
                Review.objects.create(content = postData['review'], rating = postData['rating'], reviewer_id = postData['id'], book_id = book.id)
            else:
                if Author.objects.filter(name = postData['author']):
                    author = Author.objects.get(name = postData['author'])
                    book = Book.objects.create(title = postData['title'], author_id = author.id, uploader_id = postData['id'])
                    Review.objects.create(content = postData['review'], rating = postData['rating'], reviewer_id = postData['id'], book_id = book.id)
                elif len(postData['author']) > 1:
                    author = Author.objects.create(name = postData['author'])
                    book = Book.objects.create(title = postData['title'], author_id = author.id, uploader_id = postData['id'])
                    Review.objects.create(content = postData['review'], rating = postData['rating'], reviewer_id = postData['id'], book_id = book.id)
                else:
                    res['status'] = "bad"
                    errors.append("Must enter an author name")
                    res['data'] = errors
                    return res
            res['data'] = book
            return res

class ReviewManager(models.Manager):
    def review_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        if len(postData['review']) < 10:
            res['status'] = "bad"
            res['data'] = "Review must be at least 10 characters or longer!"
        else:
            review = Review.objects.create(content = postData['review'], rating = postData['rating'], reviewer_id = postData['reviewer'], book_id = postData['book'])
            res['data'] = review
        return res


class Author(models.Model):
    name = models.CharField(max_length = 255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length = 255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    author = models.ForeignKey(Author, related_name = "books")
    uploader = models.ForeignKey(User, related_name = "uploaded_books")

    objects = BookManager()

class Review(models.Model):
    content = models.TextField(default='')
    rating = models.SmallIntegerField(default=5)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    reviewer = models.ForeignKey(User, related_name = "reviews")
    book = models.ForeignKey(Book, related_name = "book_reviews")

    objects = ReviewManager()

