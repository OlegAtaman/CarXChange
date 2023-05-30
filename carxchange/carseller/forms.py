from django.forms import ModelForm
from .models import Car


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ['title', 'price', 'runtime', 'color', 'wheel',
                  'fuel', 'accidents', 'brand', 'transmission',
                  'description', 'picture']