from django.shortcuts import render
from .models import SavedPlot
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def view_list_plots(request):
    user = request.user
    plots = SavedPlot.objects.filter(user=user).order_by('-created_on')
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username

    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'plots': plots}
    return render(request, 'saved_plots.html', context)


@login_required(login_url='/login/')
def view_saved_plots(request, slug):
    user = request.user
    plots = SavedPlot.objects.get(user=user, slug=slug).plots

    return render(request, 'view_plot.html', {'divs': plots, 'script': '', 'username': request.user.username})
