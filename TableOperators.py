import pandas as pd

def cjoin_table(table1, table2):  # Cross Join

    t1 = table_to_pd(table1)
    t2 = table_to_pd(table2)

    t1['key'] = 0
    t2['key'] = 0

    joined_table = t1.merge(t2, how='left', on='key', suffixes=('_' + table1.name, '_' + table2.name))
    joined_table.drop('key', 1, inplace=True)

    return joined_table


def njoin_table(table1, table2):  # Natural Join
    t1 = table_to_pd(table1)
    t2 = table_to_pd(table2)
    return pd.merge(t1, t2, how='inner')

def table_to_pd(table):
    '''
    Input table
    Output pd dataframe
    '''
    return pd.DataFrame(list(table.tuples.values()), columns = sorted(list(table.attributes_names)))


def union(table1, table2):
    t1 = table_to_pd(table1)
    t2 = table_to_pd(table2)
    return pd.concat([t1, t2], ignore_index=True).dropna().drop_duplicates()


def intersection(table1, table2):
    t1 = table_to_pd(table1)
    t2 = table_to_pd(table2)
    return pd.merge(t1, t2, how="inner", on=list(t1.columns))

def difference(table1, table2):
    t1 = table_to_pd(table1)

    inter = intersection(table1, table2)

    diff = t1.copy()

    for index, row in diff.iterrows():
        if (inter==row).all(1).any():
            diff.drop(index, inplace = True)

    return diff