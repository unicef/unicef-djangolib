from demo.sample.models import DemoModel
from unicef_djangolib.forms import AutoSizeTextForm


class DemoForm(AutoSizeTextForm):

    class Meta:
        model = DemoModel
        fields = '__all__'
