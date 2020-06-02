import pandas as pd
import xlsxwriter
import matplotlib.pyplot as plt
# https://stackoverflow.com/questions/17071871/how-to-select-rows-from-a-dataframe-based-on-column-values

data = pd.read_excel (r'C:\Users\yshao\Google Drive\Programming\python\576067_rev5.xlsx')
data = data.loc[data['TestResult'] == 'Pass']
testid = [30010,	30110,	30170,	30210,	30220,	30060,	30270,	30290]
wb = xlsxwriter.Workbook('FVT.xlsx')
sheet1 = wb.add_worksheet('Results')
for i in range(len(testid)):
    sheet1.write(0, i + 1, testid[i])
    data1 = data.loc[data['TestID'] == testid[i]]
    data1 = data1.drop_duplicates(subset = "Barcode")
    t = data1.loc[:, 'Measurement'].values.tolist()
    if i == 0:
        tbarcode = data1.loc[:, 'Barcode'].values.tolist()
        for k in range(len(tbarcode)):
            sheet1.write(k + 1, 0, tbarcode[k])
    for j in range(len(t)):
        sheet1.write(j + 1 , i + 1, t[j])
    num_bins = 1
    plt.figure(i)
    plt.hist(t, bins=30)
    plt.xlabel(testid[i])
    plt.ylabel('Density')
wb.close()