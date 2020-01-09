from django.forms import ModelForm, SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget

import datetime
from .models import Clients

cur_year = datetime.datetime.today().year

print (datetime.datetime.today())
year_range = tuple([i for i in range(cur_year - 70, cur_year - 18)])

class ClientForm(ModelForm):

    class Meta:
        model = Clients
        fields = '__all__'
        widgets = {
            'birthDay': SelectDateWidget(years=year_range, empty_label=("Choose Year", "Choose Month", "Choose Day"),),
        }