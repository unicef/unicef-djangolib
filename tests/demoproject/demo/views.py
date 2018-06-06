from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer

from unicef_djangolib.drf.permissions import IsSuperUser

from demo.sample.models import DemoModel
from demo.sample.serializers import DemoModelSerializer


class DemoListAPIView(ListAPIView):
    """Returns a list of DemoModel objects"""

    queryset = DemoModel.objects.all()
    serializer_class = DemoModelSerializer
    permission_classes = (IsSuperUser, )
    renderer_classes = (JSONRenderer, )
