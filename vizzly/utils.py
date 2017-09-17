import json
import pandas as pd


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


def json_to_sql(json_data):
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
