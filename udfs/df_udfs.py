import pandas as pd

def addColumnByWindowFunction(df, new_column, group_by_list ,operation):
    if operation == 'row number':
        grouped_df = df.groupby(group_by_list).count().reset_index()
        grouped_df = grouped_df.loc[:, group_by_list]
        grouped_df['col_order'] = grouped_df.sort_values(group_by_list[-1], ascending=True).groupby(group_by_list[0]).cumcount() + 1
        df[new_column] = pd.merge(df, grouped_df, how='inner', on=group_by_list)['col_order']

    return df