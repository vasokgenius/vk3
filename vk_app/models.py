from django.db import models



class User(models.Model):
    uid = models.BigIntegerField()
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)

    def __str__(self):
        return '{0} {1}'.format(self.name, self.surname)

class Group(models.Model):
    gid = models.BigIntegerField()
    name = 	models.CharField(max_length=255)
    is_closed = models.PositiveSmallIntegerField()
    gtype = models.CharField(max_length=255)
    photo = models.TextField()
    photo_medium = models.TextField()
    photo_big = models.TextField()

    def __str__(self):
        return '{0}'.format(self.name)