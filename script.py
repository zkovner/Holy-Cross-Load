import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ===================================
# CHANGE THE PATH AND FILE NAMES BELOW
# ===================================

TaggerPath = r'Files\marchTest.csv'
SolarPath = r'Files\HCEPortfolio_20260312_0957.csv'
ActualLoadPath = r'Files\HCEPortfolio_20260312_1038.csv'
startDate = '2026-03-01' #change this to the start date of the period you want to analyze
endDate = '2026-03-11' #change this to the end date of

# ====================================
# LEAVE THE CODE BELOW UNCHANGED
# ====================================
dfTagger = pd.read_csv(TaggerPath)
dfCalc = pd.read_csv(SolarPath, skiprows=11,  skip_blank_lines=True)
dfActual = pd.read_csv(ActualLoadPath, skiprows=11,  skip_blank_lines=True)

dfTagger.columns = ['Date', 'HE (UTC)', 'TotalMW']
dfTagger['Date'] = pd.to_datetime(dfTagger['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
dfCalc['Date'] = pd.to_datetime(dfCalc['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
he_cols = ['Date'] + [c for c in dfCalc.columns if c.startswith('HE')]
dfCalc = dfCalc[he_cols]
dfCalc.columns = ['Date'] + [f'{i}' for i in range(1, len(dfCalc.columns))]
dfActual = dfActual[he_cols]
dfActual = dfActual[(dfActual['Date'].str.strip() != '') & (dfActual['Date'].notna())]
dfActual.columns = ['Date'] + [f'{i}' for i in range(1, len(dfActual.columns))]
dfActual = dfActual.set_index('Date')
dfActual.columns = dfActual.columns.astype(int)
dfCalc = dfCalc[(dfCalc['Date'].str.strip() != '') & (dfCalc['Date'].notna())]
dfCalc = dfCalc.set_index('Date')
dfTagger = dfTagger.pivot(index='Date', columns='HE (UTC)', values='TotalMW')
dfCalc.columns = dfCalc.columns.astype(int)

dfCalc = dfCalc.loc[startDate:endDate]
dfTagger = dfTagger.loc[startDate:endDate]  
dfActual = dfActual.loc[startDate:endDate]

# ==============================
# FINAL SOLUTION AND EXPORT
# ==============================
MW_Delivered = dfCalc.add(dfTagger)
Diff = (MW_Delivered.subtract(dfActual)).round(0)
Diff.columns = [f'HE {col}' for col in Diff.columns]
Diff.to_excel('HCE_MW_Diff.xlsx')
print("Excel File Created Successfully")

