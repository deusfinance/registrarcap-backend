from django.conf.urls import url

from charts.views import GetConfigView, GetTimeView, ResolveSymbolView, SearchSymbolView, GetBarsView

urlpatterns = [
    url('time', GetTimeView.as_view()),
    url('config', GetConfigView.as_view()),
    url('symbols', ResolveSymbolView.as_view()),
    url('search', SearchSymbolView.as_view()),
    url('history', GetBarsView.as_view()),
]

