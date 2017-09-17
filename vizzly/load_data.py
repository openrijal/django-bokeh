from sqlalchemy import create_engine
import pandas as pd

from .settings import DB_NAME, DB_USER, DB_PASS

# Connection to database
engine = create_engine('mysql+pymysql://{}:{}@localhost/{}'.format(DB_USER, DB_PASS, DB_NAME))


def load_sqdf_labeled():
    return pd.read_sql_table("sqdf_labeled", engine)


def load_vin_labeled(vin):
    connection = engine.connect()
    res = pd.read_sql(('SELECT * FROM sqdf_labeled_6 WHERE VIN8 = %(vin)s'), connection, params={"vin": vin}, )
    connection.close()
    return res


def load_part_labeled(parts_vin):
    connection = engine.connect()
    format_strings = ','.join(['%s'] * len(parts_vin))
    res = pd.read_sql(('SELECT * FROM sqdf_labeled_6 WHERE PART_NUMBER IN (%s)' % format_strings), connection,
                      params=tuple(parts_vin))
    connection.close()
    return res


def load_dtc_labeled(dtcs_vin):
    connection = engine.connect()
    format_strings = ','.join(['%s'] * len(dtcs_vin))
    res = pd.read_sql(('SELECT * FROM sqdf_labeled_6 WHERE DTC_FULL IN (%s)' % format_strings), connection,
                      params=tuple(dtcs_vin))
    connection.close()
    return res


def load_dtc_labeled_dtc(dtc):
    connection = engine.connect()
    res = pd.read_sql('SELECT * FROM sqdf_labeled_6 WHERE DTC_FULL = %(dtc)s', connection, params={"dtc": dtc})
    connection.close()
    return res


def load_part_info(parts_vin):
    connection = engine.connect()
    format_strings = ','.join(['%s'] * len(parts_vin))
    res = pd.read_sql(('SELECT * FROM xref WHERE PART_NUMBER IN (%s)' % format_strings), connection,
                      params=tuple(parts_vin))
    connection.close()
    return res


def load_ewt(vin):
    connection = engine.connect()
    res = pd.read_sql(('SELECT * FROM ewt WHERE VIN8 = %(vin)s'), connection, params={"vin": vin}, )
    connection.close()
    return res


def load_qna(vin, part):
    connection = engine.connect()
    res = pd.read_sql(('SELECT * FROM qna WHERE VINLAST8 = %(vin)s AND PART_NUMBER = %(part)s'), connection,
                      params={"vin": vin, "part": part}, )
    connection.close()
    return res


def load_single_dtc(vin):
    connection = engine.connect()
    res = pd.read_sql(('SELECT * FROM sqdf WHERE VIN8 = %(vin)s LIMIT 1'), connection,
                      params={"vin": vin}, )
    connection.close()
    return res


def load_pras(vin, part):
    connection = engine.connect()
    res = pd.read_sql(('SELECT `ROOT CAUSE CATEGORY` FROM pras WHERE `VIN LAST 8` = %(vin)s AND `PART NO` = %(part)s'),
                      connection,
                      params={"vin": vin, "part": part}, )
    connection.close()
    return res


def load_ewt_part(part):
    connection = engine.connect()
    res = pd.read_sql(('SELECT * FROM ewt WHERE PART_NUMBER = %(part)s'), connection, params={"part": part}, )
    connection.close()
    return res


def load_sqdf_dtc(dtc, start='2000-01-01 00:00:00', end='2100-01-01 00:00:00'):
    connection = engine.connect()
    res = pd.read_sql((
        'SELECT EVENT_OCCURRED,ODO_MILES FROM sqdf WHERE DTC = %(dtc)s AND EVENT_OCCURRED_2 BETWEEN %(start)s AND %(end)s'),
        connection,
        params={"dtc": dtc, "start": start, "end": end})
    connection.close()
    return res


def load_sqdf_dtc_all(start='2000-01-01 00:00:00', end='2100-01-01 00:00:00'):
    connection = engine.connect()
    res = pd.read_sql(
        ('SELECT EVENT_OCCURRED,ODO_MILES FROM sqdf WHERE EVENT_OCCURRED_2 BETWEEN %(start)s AND %(end)s'), connection,
        params={"start": start, "end": end})
    connection.close()
    return res


def plot1_example():
    connection = engine.connect()
    raw_sql = '''
        select DATE_FORMAT(STR_TO_DATE(`REPAIR-DT`, '%%Y-%%m-%%d'), '%%Y-%%m-01') "Month",`RPR-DLR` "Dealer", count(1) "Claims" from ewt group by DATE_FORMAT(STR_TO_DATE(`REPAIR-DT`, '%%Y-%%m-%%d'), '%%Y-%%m-01'), `RPR-DLR` ORDER BY STR_TO_DATE(`REPAIR-DT`, '%%Y-%%m-%%d') asc;
    '''
    res = pd.read_sql(raw_sql, connection)
    connection.close()
    return res

def get_dataframe(raw_sql):
    connection = engine.connect()
    res = pd.read_sql(raw_sql.replace('%', '%%'), connection)
    connection.close()
    return res.pivot_table(values='y', index='x', columns='z').fillna(0).reset_index()
