import pandas as pd
import numpy as np

def columnsToDate(df, column_dic, date_format):
    for column in column_dic:
        df[column] = pd.to_datetime(df[column], format=date_format, errors='coerce')