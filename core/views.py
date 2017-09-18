from django.shortcuts import render
from .models import SavedPlot
from django.contrib.auth.decorators import login_required

from vizzly.utils import get_layout
from bokeh.embed import components


@login_required(login_url='/login/')
def view_list_plots(request):
    user = request.user
    plots = SavedPlot.objects.filter(user=user)
    return render(request, 'saved_plots.html', {'plots': plots})


@login_required(login_url='/login/')
def view_saved_plots(request, slug):
    user = request.user
    plots = SavedPlot.objects.get(user=user, slug=slug).plots.split('<;;>')
    plot_list = list()

    for pl in plots:
        ly = get_layout(pl)
        plot_list.append(ly)

    script, divs = components(tuple(plot_list))

    return render(request, 'view_plot.html', {'divs': divs, 'script': script})

