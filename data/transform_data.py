"""

MYM00048601   5.2970  100.2770    3.4    PENANG INTL                            48601 PENANG
MY000048620   4.2170  100.7000    8.0    SITIAWAN                       GSN     48620 PERAK
MYM00048647   3.1310  101.5490   27.4    SULTAN ABDUL AZIZ SHAH INTL            48647 SELANGOR
MYM00048650   2.7460  101.7100   21.0    KUALA LUMPUR INTL                      48650 SELANGOR
MYM00048665   2.2630  102.2520   10.7    MALACCA                                48665 MALACCA
MYM00048674   2.4500  103.8330   45.0    MERSING                                48674 JOHOR
MYM00048615   6.1670  102.2930    4.9    SULTAN ISMAIL PETRA                    48615 KELANTAN
MY000048657   3.6200  103.2200   16.0    KUANTAN                        GSN     48657 KUANTAN
MYM00096421   2.2620  111.9850   37.2    SIBU                                   96421 SARAWAK
MYM00096449   4.3220  113.9870   18.0    MIRI                                   96449 SARAWAK
MY000096413   1.4830  110.3330   27.0    KUCHING                        GSN     96413 SARAWAK
MY000096441   3.2000  113.0330    5.0    BINTULU                        GSN     96441 SARAWAK
MYM00096471   5.9370  116.0510    3.0    KOTA KINABALU INTL                     96471 SABAH
MYM00096481   4.3130  118.1220   17.4    TAWAU                                  96481 SABAH
MY000096491   5.9000  118.0670   13.0    SANDAKAN                       GSN     96491 SABAH
MY000096465   5.3000  115.2500   30.0    LABUAN                         GSN     96465 LABUAN
"""

import pandas as pd

states = [
    ('Malaysia',1),
    ('Johor',2),
    ('Kedah',3),
    ('Kelantan',4),
    ('Melaka',5),
    ('Negeri Sembilan',6),
    ('Pahang',7),
    ('Pulau Pinang',8),
    ('Perak',9),
    ('Perlis',10),
    ('Selangor',11),
    ('Terengganu',12),
    ('Sabah',13),
    ('Sarawak',14),
    ('W.P. Kuala Lumpur',15),
    ('W.P. Labuan',16),
    ('W.P. Putrajaya',17),
    ]

def transform_date(date_raw):
    date_raw = str(date_raw)
    return date_raw[:4] + '-' + date_raw[4:6] + '-' + date_raw[6:]

def fill_missing_date(df):
    df = df.sort_values(by = ['date'])
    date_ref = pd.date_range(start=df.iloc[0]['date'], end=df.iloc[-1]['date'])
    date_ref = pd.DataFrame(date_ref)
    date_ref.columns = ['date']
    df_temp = pd.merge(date_ref, df, how='left', on=['date'])
    df_temp = df_temp.fillna(method='ffill')
    return df_temp

def transform_data(df):
    df = df[['date_raw','var','val']]
    df = df[df['var']=='TAVG']
    df = df.drop('var', axis=1)

    date = df['date_raw']
    df['date'] = pd.to_datetime(date.apply(transform_date))
    df['temp'] = df['val']/10
    df = df[['date','temp']]
    df = df[df['date'] >= '2020-01-01']

    return df

df = pd.DataFrame()

# Penang, Kedah, Perlis
df_w_penang = pd.read_csv('MYM00048601.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_penang = transform_data(df_w_penang)
df_w_penang = fill_missing_date(df_w_penang)

df_w_penang['state_id'] = 8
df_w_penang['state'] = 'Pulau Pinang'
df = df.append(df_w_penang)

df_w_penang['state_id'] = 3
df_w_penang['state'] = 'Kedah'
df = df.append(df_w_penang)

df_w_penang['state_id'] = 10
df_w_penang['state'] = 'Perlis'
df = df.append(df_w_penang)

# Perak
df_w_perak = pd.read_csv('MY000048620.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_perak = transform_data(df_w_perak)
df_w_perak = fill_missing_date(df_w_perak)

df_w_perak['state_id'] = 9
df_w_perak['state'] = 'Perak'
df = df.append(df_w_perak)

# Kuala Lumpur
df_w_kl = pd.read_csv('MYM00048647.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_kl = transform_data(df_w_kl)
df_w_kl = fill_missing_date(df_w_kl)

df_w_kl['state_id'] = 15
df_w_kl['state'] = 'W.P. Kuala Lumpur'
df = df.append(df_w_kl)

# Putrajaya
df_w_pj = pd.read_csv('MYM00048650.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_pj = transform_data(df_w_pj)
df_w_pj = fill_missing_date(df_w_pj)

df_w_pj['state_id'] = 17
df_w_pj['state'] = 'W.P. Putrajaya'
df = df.append(df_w_pj)

# Selangor
df_w_sgr = pd.merge(df_w_kl, df_w_pj, on=['date'])
df_w_sgr['temp'] = (df_w_sgr['temp_x']+df_w_sgr['temp_y'])/2
df_w_sgr = df_w_sgr[['date', 'temp']]

df_w_sgr['state_id'] = 11
df_w_sgr['state'] = 'Selangor'
df = df.append(df_w_sgr)

# Melaka
df_w_melaka = pd.read_csv('MYM00048665.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_melaka = transform_data(df_w_melaka)
df_w_melaka = fill_missing_date(df_w_melaka)

df_w_melaka['state_id'] = 5
df_w_melaka['state'] = 'Melaka'
df = df.append(df_w_melaka)

# Johor
df_w_johor = pd.read_csv('MYM00048674.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_johor = transform_data(df_w_johor)
df_w_johor = fill_missing_date(df_w_johor)

df_w_johor['state_id'] = 2
df_w_johor['state'] = 'Johor'
df = df.append(df_w_johor)

# Kelantan
df_w_kelantan = pd.read_csv('MYM00048615.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_kelantan = transform_data(df_w_kelantan)
df_w_kelantan = fill_missing_date(df_w_kelantan)

df_w_kelantan['state_id'] = 4
df_w_kelantan['state'] = 'Kelantan'
df = df.append(df_w_kelantan)

# Pahang
df_w_pahang = pd.read_csv('MY000048657.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_pahang = transform_data(df_w_pahang)
df_w_pahang = fill_missing_date(df_w_pahang)

df_w_pahang['state_id'] = 7
df_w_pahang['state'] = 'Pahang'
df = df.append(df_w_pahang)

# Terengganu
df_w_terengganu = pd.merge(df_w_kelantan, df_w_pahang, on=['date'])
df_w_terengganu['temp'] = (df_w_terengganu['temp_x']+df_w_terengganu['temp_y'])/2
df_w_terengganu = df_w_terengganu[['date', 'temp']]

df_w_terengganu['state_id'] = 12
df_w_terengganu['state'] = 'Terengganu'
df = df.append(df_w_terengganu)

# Sarawak
df_w_sibu = pd.read_csv('MYM00096421.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_sibu = transform_data(df_w_sibu)
df_w_sibu = fill_missing_date(df_w_sibu)

df_w_miri = pd.read_csv('MYM00096449.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_miri = transform_data(df_w_miri)
df_w_miri = fill_missing_date(df_w_miri)

df_w_kuching = pd.read_csv('MY000096413.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_kuching = transform_data(df_w_kuching)
df_w_kuching = fill_missing_date(df_w_kuching)

df_w_bintulu = pd.read_csv('MY000096441.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_bintulu = transform_data(df_w_bintulu)
df_w_bintulu = fill_missing_date(df_w_bintulu)

df_w_sarawak_1 = pd.merge(df_w_sibu, df_w_miri, on=['date'])
df_w_sarawak_1['temp'] = (df_w_sarawak_1['temp_x']+df_w_sarawak_1['temp_y'])
df_w_sarawak_1 = df_w_sarawak_1[['date', 'temp']]

df_w_sarawak_2 = pd.merge(df_w_kuching, df_w_bintulu, on=['date'])
df_w_sarawak_2['temp'] = (df_w_sarawak_2['temp_x']+df_w_sarawak_2['temp_y'])
df_w_sarawak_2 = df_w_sarawak_2[['date', 'temp']]

df_w_sarawak = pd.merge(df_w_sarawak_1, df_w_sarawak_2, on=['date'])
df_w_sarawak['temp'] = (df_w_sarawak['temp_x']+df_w_sarawak['temp_y'])/4
df_w_sarawak = df_w_sarawak[['date', 'temp']]

df_w_sarawak['state_id'] = 14
df_w_sarawak['state'] = 'Sarawak'
df = df.append(df_w_sarawak)

# Sabah
df_w_kk = pd.read_csv('MYM00096471.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_kk = transform_data(df_w_kk)
df_w_kk = fill_missing_date(df_w_kk)

df_w_tawau = pd.read_csv('MYM00096481.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_tawau = transform_data(df_w_tawau)
df_w_tawau = fill_missing_date(df_w_tawau)

df_w_sandakan = pd.read_csv('MY000096491.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_sandakan = transform_data(df_w_sandakan)
df_w_sandakan = fill_missing_date(df_w_sandakan)

df_w_sabah_1 = pd.merge(df_w_kk, df_w_tawau, on=['date'])
df_w_sabah_1['temp'] = (df_w_sabah_1['temp_x']+df_w_sabah_1['temp_y'])
df_w_sabah_1 = df_w_sabah_1[['date', 'temp']]

df_w_sabah = pd.merge(df_w_sabah_1, df_w_sandakan, on=['date'])
df_w_sabah['temp'] = (df_w_sabah['temp_x']+df_w_sabah['temp_y'])/3
df_w_sabah = df_w_sabah[['date', 'temp']]

df_w_sabah['state_id'] = 13
df_w_sabah['state'] = 'Sabah'
df = df.append(df_w_sabah)

# Labuan
df_w_labuan = pd.read_csv('MY000096465.csv', names=['station','date_raw','var','val','0','1','2'], index_col=False, low_memory=False)
df_w_labuan = transform_data(df_w_labuan)
df_w_labuan = fill_missing_date(df_w_labuan)

df_w_labuan['state_id'] = 16
df_w_labuan['state'] = 'W.P. Labuan'
df = df.append(df_w_labuan)

df = df.sort_values(by = ['date','state_id'])
df =  df.reset_index(drop=True)
df.index += 1

df.to_csv('temperature.csv')
