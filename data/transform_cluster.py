import pandas as pd
import numpy as np

df = pd.read_csv('cluster.csv')
df2 = pd.DataFrame()

for i in range(len(df)):
    row = df.iloc[i]
    new_row = row.copy()

    states_list = str(row.state).split(',')
    if '0' not in states_list:
        states_list.append('0')
        
    for state in states_list:
        new_row.state = int(state)+1
        df2 = df2.append(new_row, ignore_index = True)


df2.to_csv('cluster_transformed.csv', columns=['cluster','state','date_announced','date_last_onset','category','status'], index=False)

print('done')
