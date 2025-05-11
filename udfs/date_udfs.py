from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def suffixConditions(day):
    if day in [1, 21, 31]:
        suffix = 'st'
    elif day in (2, 22):
        suffix = 'nd'
    elif day in (3, 23):
        suffix = 'rd'
    else:
        suffix = 'th'

    return suffix

def isWeekday(day):
    if day in [0, 1, 2, 3, 4]:
        is_weekday = 1
    else:
        is_weekday = 0

    return is_weekday

def isWeekend(day):
    if day in [5, 6]:
        is_weekend = 1
    else:
        is_weekend = 0

    return is_weekend

def getWeek(date):
    y = int(date.strftime("%Y"))
    first_iso_week = datetime(y, 1, 1).isocalendar()[1]

    # pro poslední týden v roce je iso week = 1
    if int(date.strftime("%m")) == 12 and date.isocalendar()[1] == 1:
        set_correct_week = True
        previous_day = date + timedelta(days=-1)
        while set_correct_week:
            if first_iso_week > 50:
                week_num = previous_day.isocalendar()[1] + 2
            else:
                week_num = previous_day.isocalendar()[1] + 1
            if week_num < 50:
                previous_day = previous_day + timedelta(days=-1)
            else:
                set_correct_week = False
            
    # pro první týden v roce je iso week > 50
    elif first_iso_week > 50:
        if date.isocalendar()[1] > 50 and int(date.strftime("%m")) == 1:
            week_num = 1
        else:
            week_num = date.isocalendar()[1] + 1

    # pokud první týden je iso week = 0
    elif first_iso_week == 0:
        week_num = date.isocalendar()[1] + 1

    else:
        week_num = date.isocalendar()[1]
        
    return week_num

def getPreviousWeekDay(df, day):
    if day == 0:
        previous_weekday = df['full_date'] + pd.DateOffset(-3)
    elif day == 6:
        previous_weekday = df['full_date'] + pd.DateOffset(-2)
    else:
        previous_weekday = df['full_date'] + pd.DateOffset(-1)

    return previous_weekday

def getNextWeekDay(df, day):
    if day == 4:
        next_weekday = df['full_date'] + pd.DateOffset(3)
    elif day == 5:
        next_weekday = df['full_date'] + pd.DateOffset(2)
    else:
        next_weekday = df['full_date'] + pd.DateOffset(1)

    return next_weekday

def getColumnBy(df, new_column, group_by_field, operation):
    if operation == 'first':
        operation = 'np.min'
    elif operation == 'last':
        operation = 'np.max'

    grouped_df = df.groupby(group_by_field)['full_date'].apply(eval(operation)).reset_index()
    df[new_column] = pd.merge(df, grouped_df, how='inner', on=group_by_field, suffixes=['', '_r'])['full_date_r']

    return df

def getYearMonth(date, months_add):

    date_add = date + pd.DateOffset(months = months_add)
    year_month = f'{date_add.year}-{date_add.month:0>2}'

    return year_month

def getCurrentPeriod(date, period):

    current_date = date.now()

    if period == 'today':
        return 1 if current_date.date() == date.date() else 0
    if period == 'week':
        return 1 if getWeek(current_date) == getWeek(date) and current_date.year == date.year else 0
    if period == 'month':
        return 1 if current_date.month == date.month and current_date.year == date.year else 0
    if period == 'quarter':
        return 1 if current_date.quarter == date.quarter and current_date.year == date.year else 0
    if period == 'year':
        return 1 if current_date.year == date.year else 0
    
def getMissingWd(df, missing_value):

    if missing_value == 'pwd':
        dy = df['full_date'].min()
        wd = dy + timedelta(days=-1)
    if missing_value == 'nwd':
        dy = df['full_date'].max()
        wd = dy + timedelta(days=2) # exclude 01.01.

    set_match = True

    while set_match:
        if (wd.weekday() in [5, 6]) and (missing_value=='pwd'):
            wd = dy + timedelta(days=-1)
        elif (wd.weekday() in [5, 6]) and (missing_value=='nwd'):
            wd = dy + timedelta(days=1)
        else:
            set_match = False

    return wd