import pandas as pd
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import numpy as np
from udfs import date_udfs, validation_udfs, df_udfs, holidays_udfs

def createCalendar(start_year:int, for_years:int)->pd.DataFrame:
    """Create calendar for given years.

    Args:
        start_year (int): year when the calendar starts
        for_years (int): number of years to create the calendar for

    Returns:
        DataFrame: calendar dataframe with columns:
            - date_key (int): date in format
            - full_date (datetime): full date
            - y (int): year
            - m (int): month
            - d (int): day
            - day_suffix (str): suffix of the day
            - year_month (str): year with month in format YYYY-MM
            - wkd (int): day of week (0 = Monday, 6 = Sunday)
            - wkd_name (str): weekday name
            - month_name (str): month name
            - q (int): quarter (1-4)
            - year_quarter (str): year with quarter in format YYYY-Q1-4
            - day_year (int): day order in year
            - w (int): week number in year
            - iso_w (int): week number in year according to ISO
            - week_month (int): week number in month
            - is_weekend (int): identify weekend
            - is_weekday (int): identify weekday
            - previous_weekday (datetime): previous weekday
            - next_weekday (datetime): next weekday
            - is_holiday (int): identify holiday
            - holiday_name (str): holiday name
            - is_workday (int): identify workday
            - workday_id (int): workday id
            - workday_date (datetime): workday date
            - workday_number (int): workday number
            - pwd (datetime): previous workday
            - nwd (datetime): next workday
            - first_workday_in_month (datetime): first workday in month
            - last_workday_in_month (datetime): last workday in month
            - first_day_year (datetime): first day in year
            - first_day_quarter (datetime): first day in quarter
            - first_day_month (datetime): first day in month
            - first_day_week (datetime): first day in week
            - last_day_year (datetime): last day in year
            - last_day_quarter (datetime): last day in quarter
            - last_day_month (datetime): last day in month
            - last_day_week (datetime): last day in week
            - previous_day (datetime): previous day
            - next_day (datetime): next day
            - previous_year_month (str): previous year with month
            - next_year_month (str): next year with month
            - previous_quarter (int): previous quarter
            - next_quarter (int): next quarter
            - previous_year (int): previous year
            - next_year (int): next year
            - is_today (int): identify today
            - is_report_day (int): identify report day
            - is_current_week (int): identify current week
            - is_current_month (int): identify current month
            - is_current_quarter (int): identify current quarter
            - is_current_year (int): identify current year
            - created (datetime): created date
    """
    start_date = datetime(start_year, 1, 1)
    end_date = (start_date + relativedelta(years=for_years) - pd.Timedelta(days=1)).date()

    # create base dataframe
    df = pd.DataFrame({
        'date_key': pd.date_range(start=start_date, end=end_date, freq='D').strftime('%Y%m%d').astype(int),
        'full_date': pd.date_range(start=start_date, end=end_date, freq='D')
    })

    # year, month and day as int
    df['y'] = pd.DatetimeIndex(df['full_date']).year
    df['m'] = pd.DatetimeIndex(df['full_date']).month
    df['d'] = pd.DatetimeIndex(df['full_date']).day

    # day suffix ('st', 'nd', 'rd', 'th')
    df['day_suffix'] = df.apply(lambda x: date_udfs.suffixConditions(x['d']), axis=1)

    # year with month in format YYYY-MM
    df['year_month'] = df.apply(lambda x: date_udfs.getYearMonth(x['full_date'], 0), axis=1)

    # day of week (0 = Monday, 6 = Sunday)
    df['wkd'] = df['full_date'].dt.day_of_week

    # weekday name
    df['wkd_name'] = df['full_date'].dt.day_name()

    # month name
    df['month_name'] = df['full_date'].dt.month_name()

    # quarter (1-4)
    df['q'] = df['full_date'].dt.quarter

    # year with quarter in format YYYY-Q1-4
    df['year_quarter'] = df['y'].astype(str) + '-Q' +  df['q'].astype(str)

    # day order in year
    df['day_year'] = df['full_date'].dt.day_of_year

    # week number in year
    df['w'] = df.apply(lambda x: date_udfs.getWeek(x['full_date']), axis=1)
    df['iso_w'] = df['full_date'].dt.isocalendar().week

    # week number in month
    df = df_udfs.addColumnByWindowFunction(df, 'week_month', ['year_month', 'w'], 'row number')

    # identify weekend and weekday
    df['is_weekend'] = df.apply(lambda x: date_udfs.isWeekend(x['wkd']), axis=1)
    df['is_weekday'] = df.apply(lambda x: date_udfs.isWeekday(x['wkd']), axis=1)

    # previous and next day
    df['previous_weekday'] = df.apply(lambda x: date_udfs.getPreviousWeekDay(x, x['wkd']), axis=1)
    df['next_weekday'] = df.apply(lambda x: date_udfs.getNextWeekDay(x, x['wkd']), axis=1)

    # create holidays
    holidays = holidays_udfs.Holidays(df)
    df = holidays.insertHolidays()

    df['is_workday'] =  df.apply(lambda x: 1 if x['is_weekend'] == 0 and x['is_holiday'] == 0 else 0, axis=1)


    df_workdays = df.loc[df['is_workday']==1, ['full_date', 'year_month']].reset_index()

    df_workdays['day_order'] = df_workdays.sort_values(['full_date'], ascending=True).groupby(['year_month']).cumcount() + 1

    df_workdays['workday_id'] = df_workdays.reset_index().index + 1

    df_workdays['pwd_id'] = df_workdays['workday_id'] - 1
    df_workdays['pwd_date'] = pd.merge(df_workdays, df_workdays, how='left', left_on=['pwd_id'], right_on=['workday_id'], suffixes=[None, '_prev'])['full_date_prev']

    df_workdays['nwd_id'] = df_workdays['workday_id'] + 1
    df_workdays['nwd_date'] = pd.merge(df_workdays, df_workdays, how='left', left_on=['nwd_id'], right_on=['workday_id'], suffixes=[None, '_next'])['full_date_next']

    df['workday_id'] = pd.merge(df, df_workdays, how='left', on=['full_date'])['workday_id']


    # create dataframe by months
    df_workdays_months = df_workdays.groupby(['year_month']).agg({
        'workday_id':['min', 'max'],
        'full_date': ['min', 'max']}).reset_index()
    df_workdays_months.columns = ['year_month', 'id_min', 'id_max', 'date_min', 'date_max']


    for index, row in df.iterrows():
        current_month = row['year_month']
        current_date = row['full_date']

        if pd.isnull(row['workday_id']):
            min_wd_day = df_workdays_months.loc[df_workdays_months['year_month'] == current_month, 'date_min'].item()
            max_wd_day = df_workdays_months.loc[df_workdays_months['year_month'] == current_month, 'date_max'].item()

            if current_date < min_wd_day:
                df.loc[index, 'workday_id'] = df_workdays_months.loc[df_workdays_months['year_month'] == current_month, 'id_min'].item()
            elif current_date > max_wd_day:
                df.loc[index, 'workday_id'] = df_workdays_months.loc[df_workdays_months['year_month'] == current_month, 'id_max'].item()
            else:
                # vezmi předcházející workday_id v daném měsíci
                need_assign = True

                previous_date = current_date + pd.Timedelta(days=-1)
                while need_assign:
                    if (previous_date in df_workdays['full_date'].values):
                        df.loc[index, 'workday_id'] = df_workdays.loc[df_workdays['full_date']==previous_date,'workday_id'].item()
                        need_assign = False
                    else:
                        previous_date = previous_date + pd.Timedelta(days=-1)
        else:
            pass

    df['workday_id'] = df['workday_id'].astype(int)

    df['workday_date'] = pd.merge(df, df_workdays, how='left', on=['workday_id'], suffixes=[None, '_new'])['full_date_new']
    df['workday_number'] = pd.merge(df, df_workdays, how='left', on=['workday_id'])['day_order']

    df['pwd'] = pd.merge(df, df_workdays, how='left', on=['workday_id'])['pwd_date']
    df['pwd'] = df['pwd'].fillna(date_udfs.getMissingWd(df, 'pwd'))

    df['nwd'] = pd.merge(df, df_workdays, how='left', on=['workday_id'])['nwd_date']
    df['nwd'] = df['nwd'].fillna(date_udfs.getMissingWd(df, 'nwd'))

    # first and last workday in month
    df['first_workday_in_month'] = pd.merge(df, df_workdays_months, how='inner', on=['year_month'], suffixes=[None, '_new'])['date_min']
    df['last_workday_in_month'] = pd.merge(df, df_workdays_months, how='inner', on=['year_month'], suffixes=[None, '_new'])['date_max']

    # first and last day in year, quarter, month and week
    df = date_udfs.getColumnBy(df, 'first_day_year', 'y', 'first')
    df = date_udfs.getColumnBy(df, 'first_day_quarter', 'year_quarter', 'first')
    df = date_udfs.getColumnBy(df, 'first_day_month', 'year_month', 'first')
    df = date_udfs.getColumnBy(df, 'first_day_week', ['y', 'w'], 'first')

    df = date_udfs.getColumnBy(df, 'last_day_year', 'y', 'last')
    df = date_udfs.getColumnBy(df, 'last_day_quarter', 'year_quarter', 'last')
    df = date_udfs.getColumnBy(df, 'last_day_month', 'year_month', 'last')
    df = date_udfs.getColumnBy(df, 'last_day_week', ['y', 'w'], 'last')
    
    # previous and next year, quarter, month and day
    df['previous_day'] = df['full_date'] + pd.DateOffset(-1)
    df['next_day'] = df['full_date'] + pd.DateOffset(1)

    df['previous_year_month'] = df.apply(lambda x: date_udfs.getYearMonth(x['full_date'], -1), axis=1)
    df['next_year_month'] = df.apply(lambda x: date_udfs.getYearMonth(x['full_date'], +1), axis=1)

    df['previous_quarter'] = (df['full_date'] + pd.DateOffset(months=-3)).dt.quarter
    df['next_quarter'] = (df['full_date'] + pd.DateOffset(months=3)).dt.quarter

    df['previous_year'] = pd.DatetimeIndex(df['full_date'] + pd.DateOffset(months=-12)).year
    df['next_year'] = pd.DatetimeIndex(df['full_date'] + pd.DateOffset(months=12)).year

    # current period flags
    if end_date < datetime.now().date():
        df['is_today'] = 0
        df['is_report_day'] = 0
        df['is_current_week'] = 0
        df['is_current_month'] = 0
        df['is_current_quarter'] = 0
        df['is_current_year'] = 0
    else:
        df['is_today'] = df.apply(lambda x: date_udfs.getCurrentPeriod(x['full_date'], 'today'), axis=1)

        pwd = df.loc[df['is_today']==1, 'pwd'].item()
        df['is_report_day'] = df.apply(lambda x : 1 if x['workday_date'] == pwd else 0, axis=1)

        df['is_current_week'] = df.apply(lambda x: date_udfs.getCurrentPeriod(x['full_date'], 'week'), axis=1)
        df['is_current_month'] = df.apply(lambda x: date_udfs.getCurrentPeriod(x['full_date'], 'month'), axis=1)
        df['is_current_quarter'] = df.apply(lambda x: date_udfs.getCurrentPeriod(x['full_date'], 'quarter'), axis=1)
        df['is_current_year'] = df.apply(lambda x: date_udfs.getCurrentPeriod(x['full_date'], 'year'), axis=1)

    # created date
    df['created'] = datetime.now()

    return df
    
if __name__ == '__main__':

    # validate year input
    while True:
        start_year = int(input('Enter start year: '))

        if validation_udfs.validStartYear(start_year) == False:
            print('Invalid start year. Please enter year between 1970 and 2100.')
            exit()
        else:
            break

    # validate number of years input
    while True:
        for_years = int(input('Enter number of years: '))

        if validation_udfs.validForYears(for_years) == False:
            print('Invalid number of years. Please enter a positive integer.')
            exit()
        else:
            break

    df = createCalendar(start_year, for_years)

    df.to_csv('calendar.csv', index=False)