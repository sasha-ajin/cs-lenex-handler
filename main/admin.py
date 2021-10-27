from django.contrib import admin
from .models import Club, Athlete, Meet, Enrollment,Record

admin.site.register(Club)
admin.site.register(Athlete)
admin.site.register(Meet)
admin.site.register(Enrollment)
admin.site.register(Record)

