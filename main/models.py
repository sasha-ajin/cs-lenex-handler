from django.db import models
from .utils import file_txt_handle

NATIONS = file_txt_handle("./docs/nations.txt")


class Club(models.Model):
    code = models.CharField(max_length=20)
    nation = models.CharField(max_length=10, choices=NATIONS)
    clubid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.clubid} ({self.nation})"


class Athlete(models.Model):
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    birthdate = models.DateField()
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=GENDERS)
    nation = models.CharField(max_length=15, choices=NATIONS)
    athleteid = models.CharField(max_length=100, unique=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} | {self.athleteid} ({self.nation})"


class Meet(models.Model):
    TIMING = (
        ('AUTOMATIC', 'AUTOMATIC'),
        ('MANUAL3', 'MANUAL3'),
        ('MANUAL1', 'MANUAL1')
    )
    ENTRYTYPE = (
        ('OPEN', 'OPEN'),
        ('INVITATION', 'INVITATION'),
    )
    STARTMETHOD = (
        ('1', '1'),
        ('2', '2'),
    )
    COURCES = (
        ('LCM', 'LCM'),
        ('SCM', 'SCM'),
        ('SCY', 'SCY'),
        ('SCY', 'SCY'),
        ('SCM16', 'SCM16'),
        ('SCM20', 'SCM20'),
        ('SCM33', 'SCM33'),
        ('SCY20', 'SCY20'),
        ('SCY27', 'SCY27'),
        ('SCY33', 'SCY33'),
        ('SCY36', 'SCY36'),
        ('OPEN', 'OPEN'),
    )
    clubs = models.ManyToManyField(Club)
    athletes = models.ManyToManyField(Athlete)
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    course = models.CharField(max_length=20, choices=COURCES)
    deadline = models.DateField()
    entrystartdate = models.DateField()
    entrytype = models.CharField(max_length=20, choices=ENTRYTYPE, default='null')
    reservecount = models.IntegerField(default=0)
    startmethod = models.CharField(max_length=20, choices=STARTMETHOD, default='null')
    timing = models.CharField(max_length=15, choices=TIMING, default='null')
    nation = models.CharField(max_length=15, choices=NATIONS, default='null')

    def __str__(self):
        return f"{self.name} in {self.city}({self.nation})"
