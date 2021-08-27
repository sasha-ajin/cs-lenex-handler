from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .utils import file_xml_handle
from django import views
from django.contrib import messages
from .models import Athlete, Meet, Club


class Main(views.View):
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        meets_quantity, clubs_quantity, athletes_quantity = int(), int(), int()
        if form.is_valid():
            file_list = file_xml_handle(request.FILES['file'])
            for meet in file_list:
                meet_obj = Meet.objects.create(name=meet['name'], course=meet['course'], deadline=meet['deadline'],
                                               entrystartdate=meet['entrystartdate'], entrytype=meet['entrytype'],
                                               reservecount=int(meet['reservecount']), startmethod=meet['startmethod'],
                                               timing=meet['timing'], nation=meet['nation'])
                meets_quantity += 1
                for club in meet['clubs']:
                    meet_obj.clubs.add(Club.objects.create(code=club['code'], nation=club['nation'],
                                                           clubid=club['clubid'], name=club['nation']))
                    clubs_quantity += 1
                    for athlete in club['athletes']:
                        meet_obj.athletes.add(
                            Athlete.objects.create(birthdate=athlete['birthdate'], firstname=athlete['firstname'],
                                                   lastname=athlete['lastname'], gender=athlete['gender'],
                                                   nation=athlete['nation'], 
                                                   athleteid=athlete['athleteid'],
                                                   club=Club.objects.get(clubid=club['clubid'])))
                        athletes_quantity += 1
                        # print(athlete)
            messages.info(request, f"{meets_quantity} meet(-s) created")
            messages.info(request, f"{clubs_quantity} club(-s) created")
            messages.info(request, f"{athletes_quantity} athlete(-s) created")
        else:
            messages.info(request, 'You have problems with file extension')
        return redirect('/')

    def get(self, request):
        form = UploadFileForm()
        return render(request, 'main.html', {'form': form})
