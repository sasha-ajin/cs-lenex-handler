from django.shortcuts import render, redirect
from .forms import UploadFileForm
from django import views
from django.contrib import messages
from .services import file_xml_handle
from .classes_schemas import cc


class Main(views.View):
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            res = file_xml_handle(request.FILES['file'])
            if res['errors']:
                messages.info(request, f"Was error in creating")
            else:
                messages.info(request, f"{res['meets_quantity']} meet(-s) created")
                messages.info(request, f"{res['clubs_quantity']} club(-s) created")
                messages.info(request, f"{res['athletes_quantity']} athlete(-s) created")
                messages.info(request, f"There was no errors")
        else:
            messages.info(request, 'You have problems with file extension')
        return redirect('/')

    def get(self, request):
        cc()
        form = UploadFileForm()
        return render(request, 'main.html', {'form': form})
