from django.shortcuts import render
from .models import SavedPlot
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def view_list_plots(request):
    user = request.user
    plots = SavedPlot.objects.filter(user=user)
    return render(request, 'saved_plots.html', {'plots': plots})


@login_required(login_url='/login/')
def view_saved_plots(request, slug):
    user = request.user
    plots = SavedPlot.objects.get(user=user, slug=slug)
    return render(request, 'view_plot.html', {'plots': plots})

