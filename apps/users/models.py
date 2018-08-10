from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9._-]+$')

class UserManager(models.Manager):
    def reg_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        if len(postData['name']) < 2 and not NAME_REGEX.match(postData['name']):
            errors.append("Name must be more than 2 characters and must only contain alphabetic characters")
        if len(postData['username']) < 2 and not USERNAME_REGEX.match(postData['username']):
            errors['username'] = "User name must be over 2 characters and must only contain alphabetic characters, numbers, or '_-.'"
        if not EMAIL_REGEX.match(postData['email']) or len(postData['email']) < 3:
            errors.append("Not a valid email format")
        if len(postData['password']) < 8:
            errors.append("Password must be longer than 8 characters!")
        if postData['password'] != postData['confirm_password']:
            errors.append("Passwords do not match!")
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt().encode())
            user = User.objects.create(name = postData['name'], username = postData['username'], email = postData['email'], password = hashed_pw)
            res['data'] = user
        return res

    def log_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        try:
            the_user = User.objects.get(email = postData['email'])
        except:
            res['status'] = "bad"
            res['data'] = "The email or password is incorrect"
            return res
        if bcrypt.checkpw(postData['password'].encode(), the_user.password.encode()):
            res['data'] = the_user
            return res
        else:
            res['status'] = "bad"
            res['data'] = "The email or password is incorrect"
            return res


class User(models.Model):
    name = models.CharField(max_length = 45)
    username = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()