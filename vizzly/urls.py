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
from .views import index, view_single, view_global_ewt, clear_session, save_session, update_plot, get_iframe
from django.contrib.auth import views as auth_views
from core.views import view_list_plots, view_saved_plots

urlpatterns = [
    url(r'^~admin/', admin.site.urls),
    url(r'^$', index, name='home'),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^single/$', view_single, name='single'),
    url(r'^global/$', view_global_ewt, name='global'),
    url(r'^clear_session/$', clear_session, name='clear_session'),
    url(r'^save_session/$', save_session, name='save_session'),

    url(r'^list_plots/$', view_list_plots, name='list_plots'),
    url(r'^view_plot/(?P<slug>[^\.]+)', view_saved_plots, name='view_plot'),
    url(r'^update_plot', update_plot, name='update_plot'),
    url(r'^get_iframe', get_iframe, name='get_iframe'),

]
