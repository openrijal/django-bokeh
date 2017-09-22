import json
import collections

from bokeh.models import ColumnDataSource, FactorRange, HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import viridis
from bokeh.plotting import figure

from .load_data import *


def columnsToDate(df, column_dic, date_format):
    for column in column_dic:
        df[column] = pd.to_datetime(df[column], format=date_format, errors='coerce')


def ewt_date_convert(time_scale):
    ts = time_scale.upper()
    dt = "`REPAIR-DT`"
    dt_obj = "STR_TO_DATE({0}, '%Y-%m-%d')".format(dt)

    if ts == "QUARTER":
        yr = "YEAR({0})".format(dt_obj)
        qt = "QUARTER({0})".format(dt_obj)
        dt = "CONCAT(CAST({0} AS CHAR(4)),'-', CAST({1} AS CHAR(4)))".format(yr, qt)

    elif ts == "MONTH":
        yr = "YEAR({0})".format(dt_obj)
        mt = "MONTH({0})".format(dt_obj)
        dt = "CONCAT(CAST({0} AS CHAR(4)),'-', CAST({1} AS CHAR(4)))".format(yr, mt)

    return dt


def json_to_sql(json_data, filters):
    query_params = json.loads(json_data)
    time_scale = query_params.get('plot_parameters').get('time_scale')
    compare_parameter = query_params.get('plot_parameters').get('compare_parameter')
    aggregation_method = query_params.get('plot_parameters').get('aggregation_method')
    aggregation_parameter = query_params.get('plot_parameters').get('aggregation_parameter', "1")

    where_clause = "1"

    for ft in filters:
        where_clause += " AND `{0}`{1}'{2}'".format(ft.get('parameter'), ft.get('operator'), ft.get('value'))

    query = "SELECT {0} x, `{1}` z, {2}(`{3}`) y FROM ewt WHERE {4} GROUP BY {0}, `{1}`".format(
        ewt_date_convert(time_scale), compare_parameter, aggregation_method, aggregation_parameter, where_clause)

    return query


def get_plot_labels(json_data):
    query_params = json.loads(json_data)
    time_adj_maps = {'DAY': 'Daily', 'MONTH': 'Monthly', 'QUARTER': 'Quarterly'}
    time_adj = time_adj_maps[query_params.get('plot_parameters').get('time_scale')]

    if query_params.get('plot_parameters').get('aggregation_method') == 'COUNT':
        aggr_str = 'Count'
    else:
        aggr_str = 'Sum of {0}'.format(query_params.get('plot_parameters').get('aggregation_parameter'))
    plot_title = '{0} {1} by {2}'.format(time_adj, aggr_str,
                                         query_params.get('plot_parameters').get('compare_parameter'))

    x_label = '{0}/{1}'.format(query_params.get('plot_parameters').get('compare_parameter'),
                               query_params.get('plot_parameters').get('time_scale').capitalize())
    y_label = aggr_str

    PlotLabels = collections.namedtuple("PlotLabels", "title x_label y_label")

    return PlotLabels(title=plot_title, x_label=x_label, y_label=y_label)


def get_layout(json_data, filters):
    sql_data = json_to_sql(json_data, filters)
    data = get_dataframe(sql_data)

    labels = get_plot_labels(json_data)

    columns = data.columns.tolist()
    columns.remove('x')

    x_axis_data = [(x, z) for x in data['x'] for z in columns]

    to_zip = [data[c].tolist() for c in columns]

    y_axis_data = sum(zip(*to_zip), ())

    source = ColumnDataSource(data=dict(x_axis_data=x_axis_data, y_axis_data=y_axis_data))

    hover = HoverTool(tooltips=[
        (','.join(labels.x_label.rsplit('-', 1)[::-1]), "@x_axis_data"),
        (labels.y_label, "@y_axis_data"),
    ])

    p = figure(x_range=FactorRange(*x_axis_data), plot_width=1200, plot_height=600,
               title=labels.title, tools=[hover, 'pan', 'box_zoom', 'wheel_zoom', 'save', 'reset'])

    p.vbar(x='x_axis_data', top='y_axis_data', width=1, source=source, line_color="white",
           fill_color=factor_cmap('x_axis_data', palette=viridis(len(columns)), factors=columns, start=1,
                                  end=len(columns)))

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.xaxis.axis_label = labels.x_label
    p.yaxis.axis_label = labels.y_label
    p.title.align = 'center'

    # eng = TextInput(title="ENG")
    # tran = TextInput(title="TRAN")
    # miles = TextInput(title="MILES")
    #
    # controls = [eng, tran, miles]
    #
    # sizing_mode = 'fixed'
    #
    # ly = layout([controls, [p]], sizing_mode=sizing_mode)

    # return ly
    return p
