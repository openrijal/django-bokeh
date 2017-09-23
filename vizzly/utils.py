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

def date_binning(time_scale, date_param):
    ts = time_scale.upper()
    dt = "`{0}`".format(date_param)
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


def number_binning(bin_size, number_param):
    return "CONCAT( FLOOR(`{0}`/{1})*{1}, ' - ', CEIL(`{0}`/{1})*{1})".format(number_param, bin_size)


def json_to_sql_old(json_data):
    query_params = json.loads(json_data)
    time_scale = query_params.get('plot_parameters').get('time_scale')
    compare_parameter = query_params.get('plot_parameters').get('compare_parameter')
    aggregation_method = query_params.get('plot_parameters').get('aggregation_method')
    aggregation_parameter = query_params.get('plot_parameters').get('aggregation_parameter', "1")

    where_clause = "1"
    for ft in query_params.get('plot_parameters').get('filters'):
        where_clause += " AND `{0}`{1}'{2}'".format(ft.get('parameter'), ft.get('operator'), ft.get('value'))

    query = "SELECT {0} x, `{1}` z, {2}(`{3}`) y FROM ewt WHERE {4} GROUP BY {0}, `{1}`".format(
        ewt_date_convert(time_scale), compare_parameter, aggregation_method, aggregation_parameter, where_clause)

    return query


def json_to_sql(json_data):
    query_params = json.loads(json_data)
    x_axis = query_params.get('plot_parameters').get('x_axis', None)
    y_axis = query_params.get('plot_parameters').get('y_axis', None)

    # Create the filters array
    where_clause = "1"
    for ft in query_params.get('plot_parameters').get('filters'):
        where_clause += " AND `{0}`{1}'{2}'".format(ft.get('parameter'), ft.get('operator'), ft.get('value'))

    x_primary_param = x_axis.get('primary').get('parameter')
    x_primary_binning = x_axis.get('primary').get('binning_method')
    x_primary_binning_param = x_axis.get('primary').get('binning_param')
    x_categorical_param = x_axis.get('categorical').get('parameter')

    y_agg_method = y_axis.get('aggregation_method')
    y_agg_param = y_axis.get('aggregation_parameter', None)

    if y_agg_method.upper() == 'COUNT':
        agg_param = 'COUNT(1)'
    else:
        agg_param = '{0}(`{1}`)'.format(y_agg_method, y_agg_param)

    if x_primary_binning == 'date':
        x_primary =  date_binning(x_primary_binning_param, x_primary_param)
    elif x_primary_binning == 'number':
        x_primary = number_binning(x_primary_binning_param, x_primary_param)

    query = "SELECT {0} x, `{1}` z, {2} y FROM ewt WHERE {3} GROUP BY {0}, `{1}`".format(
        x_primary, x_categorical_param, agg_param, where_clause)

    print(query)
    return query


def get_plot_labels(json_data):
    query_params = json.loads(json_data)
    x_axis = query_params.get('plot_parameters').get('x_axis', None)
    y_axis = query_params.get('plot_parameters').get('y_axis', None)

    x_primary_param = x_axis.get('primary').get('parameter')
    x_primary_binning = x_axis.get('primary').get('binning_method')
    x_primary_binning_param = x_axis.get('primary').get('binning_param')
    x_categorical_param = x_axis.get('categorical').get('parameter')

    y_agg_method = y_axis.get('aggregation_method')
    y_agg_param = y_axis.get('aggregation_parameter', None)

    print('Aggregation method {0}'.format(y_agg_method))

    if y_agg_method == 'COUNT':
        aggr_str = 'Count'
    else:
        aggr_str = '{0} of {1}'.format(y_agg_method, y_agg_param)


    x_label = '{0}/{1} - {2}'.format(x_categorical_param, x_primary_binning_param, x_primary_param)
    y_label = aggr_str

    plot_title = '{0} vs {1}'.format(y_label, x_label)

    PlotLabels = collections.namedtuple("PlotLabels", "title x_label y_label")

    return PlotLabels(title=plot_title, x_label=x_label, y_label=y_label)


def get_layout(json_data):
    sql_data = json_to_sql(json_data)
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
