from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import PhotoForm
from .models import Photo


def index(request):
    template = loader.get_template('animal_app/index.html')
    context = {'form': PhotoForm()}
    return HttpResponse(template.render(context, request))


def predict(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = Photo(image=form.cleaned_data['image'])
            
            predicted, percentage = photo.predict()
            
            template = loader.get_template('animal_app/result.html')
            context = {
                'photo_name': photo.image.name,
                'photo_data': photo.image_src(),
                'predicted': predicted,
                'percentage': percentage,
            }
            return HttpResponse(template.render(context, request))
        else:
            raise ValueError('Formが不正です')
    return redirect('animal_app:index')