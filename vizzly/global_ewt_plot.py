from __future__ import unicode_literals

from bokeh.io import curdoc
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.ranges import FactorRange
from bokeh.models.widgets import TextInput
from bokeh.palettes import viridis
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

from .load_data import *
from .utils import *

# Create Input controls
eng = TextInput(title="ENG")
tran = TextInput(title="TRAN")
miles = TextInput(title="MILES")

controls = [eng, tran, miles]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = widgetbox(*controls, sizing_mode=sizing_mode)


def getdata():
    eng_val = eng.value.strip()
    tra_val = tran.value.strip()
    miles_val = miles.value.strip()


def update(json_data):
    sql_data = json_to_sql(json_data)
    data = get_dataframe(sql_data)

    columns = data.columns.tolist()
    columns.remove('x')

    x_axis_data = [(x, z) for x in data['x'] for z in columns]

    to_zip = [data[c].tolist() for c in columns]

    y_axis_data = sum(zip(*to_zip), ())

    source = ColumnDataSource(data=dict(x_axis_data=x_axis_data, y_axis_data=y_axis_data))

    p = figure(x_range=FactorRange(*x_axis_data), plot_width=1200, plot_height=600,
               title="Chart with Zip implementation")

    p.vbar(x='x_axis_data', top='y_axis_data', width=1, source=source, line_color="white",
           fill_color=factor_cmap('x_axis_data', palette=viridis(len(columns)), factors=columns, start=1,
                                  end=len(columns)))

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    return p



def get_plot(json_data):
    p=update(json_data)

    l = layout([
        [eng, tran, miles],
        [p],
    ], sizing_mode=sizing_mode)
    curdoc().add_root(l)
    return curdoc()
