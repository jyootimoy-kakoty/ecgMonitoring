"""ecgMonitoring URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    #Index
    url(r'^$', views.Index, name='Index'),
    #Data Entry
    url(r'^hospitalDataEntry$', views.hospitalDataEntry, name='hospitalDataEntry'),
    url(r'^patientDataEntry$', views.patientDataEntry, name='patientDataEntry'),
    url(r'^sensorDataEntry$', views.sensorDataEntry, name='sensorDataEntry'),
    url(r'^ecgDataEntry$', views.ecgDataEntry, name='ecgDataEntry'),
    #Details
    url(r'^(?P<hID>H[A-Z]+[0-9]+)/$', views.hospitalDetails , name='hospitalDetails'),
    url(r'^(?P<pID>P[A-Z]+[0-9]+)/$', views.patientDetails , name='patientDetails'),
    url(r'^(?P<pID>P[A-Z]+[0-9]+)/conciseTable/$', views.conciseTable , name='conciseTable'),
    #POST Request for Data Entry
    url(r'^RPIPush$', views.RPIPush , name='RPIPush'),
]