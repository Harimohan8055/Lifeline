from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import os



# Create your models here.

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('fest/', filename)

def get_file_path_event(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('event/', filename)

class State(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class User(AbstractUser):
    is_individual = models.BooleanField(default=False)
    is_institution = models.BooleanField(default=False)
    is_confirm = models.BooleanField(default=False)


class IndividualProfile(models.Model):
    TYPE=(
        ('0','Student'),
        ('1','Professional'),
        ('2','Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    location = models.CharField(max_length=15)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=50, choices=TYPE)
    age= models.IntegerField()

    def __str__(self):
        return self.user.username


class InstitutionProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institutionname = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    location = models.CharField(max_length=15)
    regno = models.IntegerField()
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class FestClubModel(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class EventModel(models.Model):
    ATYPE=(
        (0,'Student'),
        (1,'Professional'),
        (2,'Other'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    venue = models.CharField(max_length=100)
    address = models.TextField(max_length=200)
    time = models.TimeField(max_length=15)
    start_date = models.DateField(max_length=15)
    end_date = models.DateField(max_length=15)
    seats = models.IntegerField()
    fee = models.IntegerField(null=True,blank=True)
    prize = models.IntegerField(null=True,blank=True)
    paylink = models.CharField(null=True,max_length=100,blank=True)
    fest = models.ForeignKey(FestClubModel, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    attendee_type = models.IntegerField(choices=ATYPE)
    event_type = models.IntegerField()

    def __str__(self):
        return self.title

class FestImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fest = models.ForeignKey(FestClubModel, on_delete=models.CASCADE)
    name = models.ImageField(upload_to=get_file_path ,max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class EventImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    name = models.ImageField(upload_to=get_file_path_event ,max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class ApplyEventModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, editable=False)
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE,blank=True, editable=False)
    is_confirm = models.BooleanField(default=False,blank=True, editable=False)

    def __str__(self):
        return self.name


class SeatsEventModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, editable=False)
    event = models.OneToOneField(EventModel, on_delete=models.CASCADE,blank=True, editable=False)
    total_seats = models.IntegerField(blank=True, editable=False)
    available_seats=models.IntegerField(blank=True, editable=False)

    def __str__(self):
        return str(self.total_seats)
