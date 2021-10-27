from django.shortcuts import render, redirect
from .forms import UploadFileForm
from django import views
from django.contrib import messages
from .services import file_xml_handle, error_reader


class Main(views.View):
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            res = file_xml_handle(request.FILES['file'])
            if res['errors']:
                statement, errors = error_reader(errors_dict=res['error_msg'])
                messages.info(request, "Was error in file handling")
                messages.info(request, f"Problem is in '{statement}' value: {','.join(f'{error.lower()}' for error in errors)}")
            else:
                print(res['created'])
                if res['created']:
                    messages.info(request, f"{res['meet_created']} meet(-s) created")
                    messages.info(request, f"{res['club_created']} club(-s) created")
                    messages.info(request, f"{res['athlete_created']} athlete(-s) created")
                    messages.info(request, f"{res['enrollment_created']} enrollment(-s) created")
                    messages.info(request, f"{res['record_created']} record(-s) created")
                if res['updated']:
                    messages.info(request, f"{res['meet_updated']} meet(-s) updated")
                    messages.info(request, f"{res['club_updated']} club(-s) updated")
                    messages.info(request, f"{res['athlete_updated']} athlete(-s) updated")
                    messages.info(request, f"{res['record_updated']} record(-s) updated")
                if not res['created'] and not res['updated']:
                    messages.info(request, f"Nothing was created and updated")
                messages.info(request, f"There was no errors")
        else:
            messages.info(request, 'File is not valid, probably problem is in extension')
        return redirect('/')

    def get(self, request):
        form = UploadFileForm()
        return render(request, 'main.html', {'form': form})
