# this script pulls data in "Measurement" column, from an excel per testid; it remove duplicate data that has the same barcode
import pandas as pd
import xlsxwriter
import matplotlib.pyplot as plt
import statistics
# https://stackoverflow.com/questions/17071871/how-to-select-rows-from-a-dataframe-based-on-column-values

data = pd.read_excel (r'C:\Users\yshao\Music\yongzhs\everything\t.xlsx')
data = data.loc[data['TestResult'] == 'Pass']
testid = [30010, 30110,	30170,	30210,	30220,	30060,	30270,	30290]
wb = xlsxwriter.Workbook('FVT.xlsx')
sheet1 = wb.add_worksheet('Results')
sheet2 = wb.add_worksheet('Statistics')
sheet2.write(1, 0, 'TestID')
sheet2.write(2, 0, 'Average')
sheet2.write(3, 0, 'SD')
sheet2.write(4, 0, 'Max')
sheet2.write(5, 0, 'Min')
sheet2.write(6, 0, 'LSL')
sheet2.write(7, 0, 'USL')
sheet2.write(8, 0, 'Cpl')
sheet2.write(9, 0, 'Cpu')
sheet2.write(10, 0, 'Cpk')
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
        
    if testid[i] != 30110: # case 30110 is hex value and does not have upper and lower limit so skip statistics
        avg = statistics.mean(t)
        std = statistics.stdev(t)
        maxt = max(t)
        mint = min(t)
        tl = data1.loc[:, 'LowerLimit'].values.tolist()[0]
        tu = data1.loc[:, 'UpperLimit'].values.tolist()[0]
        cpl = (avg - tl) / 3 / std
        cpm = (tu - avg) / 3 / std
        sheet2.write(1, i + 1, testid[i])
        sheet2.write(2, i + 1, avg)
        sheet2.write(3, i + 1, std)
        sheet2.write(4, i + 1, maxt)
        sheet2.write(5, i + 1, mint)
        sheet2.write(6, i + 1, tl)
        sheet2.write(7, i + 1, tu)
        sheet2.write(8, i + 1, cpl)
        sheet2.write(9, i + 1, cpm)
        sheet2.write(10, i + 1, min([cpl, cpm]))
    num_bins = 1
    plt.figure(i)
    plt.hist(t, bins=30)
    plt.xlabel(testid[i])
    plt.ylabel('Density')

wb.close()