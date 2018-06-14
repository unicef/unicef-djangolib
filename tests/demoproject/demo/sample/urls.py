from django.conf.urls import url

from demo.views import DemoListAPIView

from .api import DemoCreateView, DemoUpdateView

app_name = "sample"

urlpatterns = (
    url(r'^create/$', view=DemoCreateView.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', view=DemoUpdateView.as_view(), name='update'),
    url(r'^list', view=DemoListAPIView.as_view(), name='list'),
)
