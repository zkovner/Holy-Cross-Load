This is a script meant to visually depict resource flow to Holy Cross.

***Step 1:*** Copy/Paste the SQL file into a new query in the sqltrading server. Run the query and save the result as a csv for both Bronco and GV Hydro by un-commenting those lines. Make sure to update the OperatingDT range to the desired range.

***Step 2:*** Download or Copy/Paste the python script. Change the first section where it is labeled to do so. 

***Step 3:*** From webCalc, download a csv for the aggregates for each of [Actual Load, Solar, WAPA, and HCE_Purchases]. To do this, click on the filters and set range to monthly. In object name, put the items in the list (one at a time). Export the result as a csv. TIME ZONES MUST BE UTC (or GMT)

Run the python file labeled 'plot' with the paths updated. The script should output a plot.

NOTE: Everything is in UTC to work around the webCalc and Tagger issues with timezones. Make adjustments as needed. 

