import pandas as pd
from datetime import date
from udfs import easter_calculator

class Holidays:
    def __init__(self, df:pd.DataFrame):
        self.df = df
        self.end_date = self.getEndDate()
        self.holidays_df = self.getHolidays()
        self.easters_df = self.getEaster()

    def getEndDate(self)->pd.Timestamp:
        return self.df['full_date'].max()

    def getHolidays(self)->pd.DataFrame:

        holidays_col_list = [
            'holiday_month',
            'holiday_day',
            'holiday_name',
            'date_from',
            'date_to']

        holidays_list = list()
        holidays_list.append([1, 1, 'Restoration Day of the Independent Czech State', date(1952, 1, 1), self.end_date])
        holidays_list.append([5, 1, 'Labour Day', date(1952, 1, 1), self.end_date])
        holidays_list.append([5, 8, 'Victory Day', date(1990, 5, 11), self.end_date])
        holidays_list.append([5, 9, 'Victory Day', date(1952, 1, 1), date(1990, 5, 10)])
        holidays_list.append([7, 5, 'Saints Cyril and Methodius Day', date(1990, 5, 10), self.end_date])
        holidays_list.append([7, 6, 'Jan Hus Day', date(1990, 5, 18), self.end_date])
        holidays_list.append([9, 28, 'Statehood Day', date(2000, 8, 9), self.end_date])
        holidays_list.append([10, 28, 'Independent Czechoslovak State Day', date(1988, 9, 21), self.end_date])
        holidays_list.append([11, 17, 'Struggle for Freedom and Democracy Day', date(2000, 8, 9), self.end_date])
        holidays_list.append([12, 24, 'Christmas Eve', date(1990, 5, 10), self.end_date])
        holidays_list.append([12, 25, 'Christmas Day', date(1990, 5, 10), self.end_date])
        holidays_list.append([12, 26, 'Second Day of Christmas', date(1990, 5, 10), self.end_date])

        return pd.DataFrame(data=holidays_list, columns=holidays_col_list)
    
    def getHolidaysToInsert(self)->list:
        holidays_to_insert = list()

        for i, df_row in self.df.iterrows():
            for j, hol_row in self.holidays_df.iterrows():
                # Ensure consistent types for date comparison

                date_from = pd.Timestamp(hol_row['date_from'])
                date_to = pd.Timestamp(hol_row['date_to'])

                if (df_row['m'] == hol_row['holiday_month']) \
                and (df_row['d'] == hol_row['holiday_day']) \
                and (df_row['full_date'] >= date_from) \
                and (df_row['full_date'] <= date_to):
                    holidays_to_insert.append((i, hol_row['holiday_name']))

        return holidays_to_insert
    
    def getEaster(self)->pd.DataFrame:

        easters_col_list = [
            'easter_day',
            'easter_name',
            'date_from',
            'date_to']

        easters_list = list()
        easters_list.append([4, 'Good Friday', date(2015, 12, 21), self.end_date])
        easters_list.append([0, 'Easter Monday', date(1952, 1, 1), self.end_date])

        return pd.DataFrame(data=easters_list, columns=easters_col_list)
    
    def getEastersToInsert(self)->list:
        easters = list()
        easters_to_insert = list()

        for y in self.df['y'].unique():
            easter_sunday = easter_calculator.getEasters(y)
            easter_monday = easter_sunday + pd.Timedelta(days=1)
            easter_friday = easter_sunday + pd.Timedelta(days=-2)

            easters.append([4, easter_friday])
            easters.append([0, easter_monday])

        df_easters_dates = pd.DataFrame(data=easters, columns=['easter_day', 'easter_date'])

        df_easters_dates = pd.merge(df_easters_dates, self.easters_df, on='easter_day', how='left')
        df_easters_dates = df_easters_dates.query('easter_date >= date_from and easter_date <= date_to')

        for i, df_row in self.df.iterrows():
            for j, east_row in df_easters_dates.iterrows():
                if df_row['full_date'].date() == east_row['easter_date']:
                    easters_to_insert.append((i, east_row['easter_name']))

        return easters_to_insert

    def insertHolidays(self)->pd.DataFrame:
        """
        Insert holidays to the calendar dataframe.
        """

        holidays_to_insert = self.getHolidaysToInsert() + self.getEastersToInsert()

        # create columns for holidays with default values
        self.df['is_holiday'] = 0
        self.df['holiday_name'] = ''

        # insert holidays to the dataframe
        for i in holidays_to_insert:
            self.df['is_holiday'].at[i[0]] = 1
            self.df['holiday_name'].at[i[0]] = i[1]

        return self.df