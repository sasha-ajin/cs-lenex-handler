from django.db import models
from docs.nations_tuple import nations

NATIONS = nations


class Club(models.Model):
    TYPES = (
        ('CLUB', 'CLUB'),
        ('NATIONALTEAM', 'NATIONALTEAM'),
        ('REGIONALTEAM', 'REGIONALTEAM'),
        ('UNATTACHED', 'UNATTACHED'),
    )
    code = models.CharField(max_length=20, blank=True)
    nation = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=25, choices=TYPES, default='UNATTACHED')

    def athletes_list(self):
        return Enrollment.objects.filter(club=self).values('athlete')

    def __str__(self):
        return f"{self.name}({self.nation})"


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
    clubs = models.ManyToManyField(Club, through='Enrollment')

    def records(self):
        return Record.objects.filter(enrollment__athlete=self)

    def __str__(self):
        return f"{self.firstname} {self.lastname}({self.nation})"


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
    clubs = models.ManyToManyField(Club, through='Enrollment')
    athletes = models.ManyToManyField(Athlete, through='Enrollment')
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    course = models.CharField(max_length=20, choices=COURCES, blank=True)
    deadline = models.DateField()
    entrystartdate = models.DateField()
    entrytype = models.CharField(max_length=20, choices=ENTRYTYPE)
    reservecount = models.IntegerField(default=0, blank=True)
    startmethod = models.CharField(max_length=20, choices=STARTMETHOD, blank=True)
    timing = models.CharField(max_length=15, choices=TIMING, blank=True)
    nation = models.CharField(max_length=15, choices=NATIONS, default='null')

    def __str__(self):
        return f"{self.name} in {self.city}({self.nation})"


class Enrollment(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True)
    meet = models.ForeignKey(Meet, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['athlete', 'club', 'meet']

    def foreign_athlete(self):
        if self.athlete.nation != self.meet.nation:
            return True
        return False

    def __str__(self):
        return f"athlete {self.athlete} in club {self.club} for {self.meet}"


class Record(models.Model):
    STROKE = (
        ('APNEA', 'APNEA'),
        ('BACK', 'BACK'),
        ('BIFINS', 'BIFINS'),
        ('BREAST', 'BREAST'),
        ('FLY', 'FLY'),
        ('FREE', 'FREE'),
        ('IMMERSION', 'IMMERSION'),
        ('MEDLEY', 'MEDLEY'),
        ('SURFACE', 'SURFACE'),
        ('UNKNOWN', 'UNKNOWN'),
    )
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    order = models.IntegerField()
    place = models.IntegerField()
    agemin = models.IntegerField()
    agemax = models.IntegerField()
    distance = models.IntegerField()
    stroke = models.CharField(max_length=10, choices=STROKE)
    event_gender = models.CharField(choices=GENDERS, max_length=30)
    event_number = models.IntegerField()
    event_order = models.IntegerField()


    def __str__(self):
        return f"{self.enrollment.athlete.firstname} {self.enrollment.athlete.lastname} on place {self.place}"
