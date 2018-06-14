from unicef_djangolib.forms import AutoSizeTextForm

from demo.sample.models import DemoModel


class DemoForm(AutoSizeTextForm):

    class Meta:
        model = DemoModel
        fields = '__all__'
