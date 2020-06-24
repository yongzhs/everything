import serial
import time
import visa
import xlsxwriter

address = 'GPIB0::23::INSTR'
num = 100

rm = visa.ResourceManager()
rm.list_resources()

try:
    dmm = rm.open_resource(address)
    print("Connected to " + dmm.query('*IDN?'))
except:
    print("Connection error!")
    
ser = serial.Serial('COM3', 115200, timeout=0)

wb = xlsxwriter.Workbook('voltage.xlsx')
sheet1 = wb.add_worksheet('voltage')
for i in range(num):
    ser.write([0x3C, 0xA8, 1, 9, 0, 0, 0x4E, 0x3E]) # PHY reset
    time.sleep(0.5)
    ser.write([0x3C, 0xA8, 1, 10, 0, 4, 0, 0,  0, 0, 0x49, 0x3E]) # PHY start
    time.sleep(0.5)
    ser.write([0x3C, 0xA8, 1, 5, 0, 0x1C, 4, 0,  0, 0, 8, 5, 1, 0, 0, 0,   0, 0, 0, 0xC5, 0xD, 0, 8, 0,  0, 0, 7, 0, 0, 0, 0, 0,    0, 0, 0x43, 0x3E]) # Rx mode
    time.sleep(0.1)
    v = float(dmm.query('MEAS?'))
    print(v)
    sheet1.write(i, 0, v)

wb.close()
ser.close()