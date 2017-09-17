"""vizzly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import index, view_single, view_global_ewt, clear_session
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^~admin/', admin.site.urls),
    url(r'^$', index, name='home'),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^single/$', view_single, name='single'),
    url(r'^global/$', view_global_ewt, name='global'),
    url(r'^clear_session/$', clear_session, name='clear_session'),
    # url(r'^chart1/$', bar_colormapped, name='chart1'),
    # url(r'^chart2/$', bar_nested_colormapped, name='chart2'),
    # url(r'^chart3/$', bar_nested, name='chart3'),
    # url(r'^chart4/$', bar_stacked, name='chart4'),
    # url(r'^chart5/$', bar_mixed, name='chart5'),
    # url(r'^legend1/$', hide_glyph, name='legend1'),
    # url(r'^legend2/$', mute_glyph, name='legend2'),
    # url(r'^widget1/$', slider_widget, name='widget1'),
]
