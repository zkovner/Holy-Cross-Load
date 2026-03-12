import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ===================================
# CHANGE THE PATH AND FILE NAMES BELOW
#CHANGE THE START AMD END DATES BELOW
# ===================================

SolarPath = r'Files\HCEPortfolio_20260312_1413.csv'
ActualLoadPath = r'Files\HCEPortfolio_20260312_1038.csv'
BroncoPath = r'Files\BroncoTest.csv'
HydroPath= r'Files\GVHydroTest.csv'
WAPAPath = r'Files\HCEPortfolio_20260312_1353.csv'
PurchasePath = r'Files\HCEPortfolio_20260312_1352.csv'


startDate = '2026-03-02' #change this to the start date of the period you want to analyze
endDate = '2026-03-11' #change this to the end date of

# ================================================================================
# LEAVE THE CODE BELOW UNCHANGED
# ================================================================================
def crop_csv(filepath: str, top_left_value: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, header=None, encoding='utf-8-sig', 
                     sep=',', names=range(500), on_bad_lines='skip')
    
    for row_idx in range(len(df)):
        for col_idx in range(len(df.columns)):
            cell = str(df.iloc[row_idx, col_idx]).strip().replace('\xa0', '')
            if cell == top_left_value.strip():
                df = df.iloc[row_idx:, col_idx:].reset_index(drop=True)
                df = df[[4] + [i for i in range(8, 32)]]
                df.columns = ['Date'] + [f'HE {i}' for i in range(1,25)]
                df = df.set_index('Date')
                df = df.loc[startDate:endDate]
                return df
    raise ValueError(f"'{top_left_value}' not found in {filepath}")

def pivotFromSQL(csv):
    df = pd.read_csv(csv)
    df.columns = ['Date', 'HE', 'MW']
    df= df.pivot(index='Date', columns='HE', values='MW')
    df.columns.name = None
    df.columns = [f'HE {col}' for col in df.columns]
    df = df.loc[startDate:endDate]
    return df

# ==================================
# CREATE DATAFRAMES
# ==================================
dfSolar =  crop_csv(SolarPath, startDate).apply(pd.to_numeric)
dfActual = crop_csv(ActualLoadPath, startDate).apply(pd.to_numeric)
dfPurchases = crop_csv(PurchasePath, startDate).apply(pd.to_numeric)
dfBronco = pivotFromSQL(BroncoPath).apply(pd.to_numeric)
dfHydro = pivotFromSQL(HydroPath).apply(pd.to_numeric)
dfWAPA = crop_csv(WAPAPath, startDate).apply(pd.to_numeric)


# ==============================
# FINAL SOLUTION AND EXPORT
# ==============================

# Stack all 5 dfs — each becomes a layer
names  = ['Solar', 'GV', 'WAPA',  'Bronco','TEA' ]
colors = ['#F4D03F', "#0087E0", '#1ABC9C', "#E77E73", "#7773AF"]
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Georgia']

combined = pd.concat([dfSolar, dfPurchases, dfBronco, dfHydro, dfWAPA], keys=names)

# Flatten rows x columns into a single time axis
# Each row is a date, each column is an hour — melt into (date, hour) pairs
def flatten(df, name):
    d = df.copy()
    d.index.name = 'Date'
    d = d.reset_index().melt(id_vars='Date', var_name='Hour', value_name=name)
    d['Hour_num'] = d['Hour'].str.extract(r'(\d+)').astype(int)
    d['Timestamp'] = pd.to_datetime(d['Date']) + pd.to_timedelta(d['Hour_num'] - 1, unit='h')- pd.to_timedelta(7, unit='h')
    return d.set_index('Timestamp')[name].sort_index()

series = [flatten(df, name) for df, name in zip([dfSolar, dfHydro,  dfWAPA, dfBronco, dfPurchases ], names)]
plot_df = pd.concat(series, axis=1).fillna(0)  # fill missing hours with 0

fig, ax = plt.subplots(figsize=(15, 6))

ax.stackplot(plot_df.index, 
             [plot_df[name] for name in names], 
             labels=names, colors=colors, alpha=0.9)

actual_series = flatten(dfActual, 'Actual Load')
ax.plot(actual_series.index, actual_series.values, color='red', linewidth=2.5, label='Actual Load')

# Date tick every day
import matplotlib.dates as mdates
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45, ha='right', fontsize=9)

ax.set_xlabel('Date')
ax.set_ylabel('MW')
ax.set_title('Hourly Stack by Resource')
ax.legend(loc='upper left', fontsize=9)

plt.tight_layout()
plt.show()
