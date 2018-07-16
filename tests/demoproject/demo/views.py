from rest_framework.renderers import JSONRenderer

from unicef_djangolib.drf.exports import ExportModelView
from unicef_djangolib.drf.permissions import IsSuperUser
from unicef_djangolib.drf.renderers import FriendlyCSVRenderer
from unicef_djangolib.drf.views import QueryStringFilterAPIView

from demo.sample.models import DemoModel
from demo.sample.serializers import DemoModelSerializer


class DemoListAPIView(QueryStringFilterAPIView, ExportModelView):
    """Returns a list of DemoModel objects"""

    queryset = DemoModel.objects.all()
    serializer_class = DemoModelSerializer
    permission_classes = (IsSuperUser, )
    renderer_classes = (JSONRenderer, FriendlyCSVRenderer)

    filters = (
        ('name', 'name'),
    )
    search_terms = ('name__istartswith', )
