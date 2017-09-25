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
from .views import index, view_single, view_global_ewt, clear_session, save_session,view_dashboard, update_figure, json_play
from django.contrib.auth import views as auth_views
from core.views import view_list_plots, view_saved_plots

urlpatterns = [
    url(r'^~admin/', admin.site.urls),
    url(r'^$', index, name='home'),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^single/$', view_single, name='single'),
    url(r'^global/$', view_global_ewt, name='global'),
    url(r'^dashboard/$', view_dashboard, name='dashboard'),
    url(r'^json_play/$', json_play, name='json_play'),
    url(r'^update_figure/$', update_figure, name='update_figure'),
    url(r'^clear_session/$', clear_session, name='clear_session'),
    url(r'^save_session/$', save_session, name='save_session'),

    url(r'^list_plots/$', view_list_plots, name='list_plots'),
    url(r'^view_plot/(?P<slug>[^\.]+)', view_saved_plots, name='view_plot'),

    # url(r'^chart1/$', bar_colormapped, name='chart1'),
    # url(r'^chart2/$', bar_nested_colormapped, name='chart2'),
    # url(r'^chart3/$', bar_nested, name='chart3'),
    # url(r'^chart4/$', bar_stacked, name='chart4'),
    # url(r'^chart5/$', bar_mixed, name='chart5'),
    # url(r'^legend1/$', hide_glyph, name='legend1'),
    # url(r'^legend2/$', mute_glyph, name='legend2'),
    # url(r'^widget1/$', slider_widget, name='widget1'),
]
