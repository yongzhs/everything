import serial, time, xlsxwriter
from mcculw import ul
from mcculw.enums import InterfaceType
from mcculw.ul import ULError

ser0 = serial.Serial('COM6', 115200, timeout = 0) # UART0
ser1 = serial.Serial('COM3', 115200, timeout = 0) # PLC UART
cmd0 = 'accel_get_temp\n'
cmd1 = 'adc_sm 0 2400000 0x40 0\n'

board_num = 0 # for USB-TC
channel0, channel1, channel2, channel3 = 0, 1, 2 ,3
ul.ignore_instacal()
devices = ul.get_daq_device_inventory(InterfaceType.USB, 1)
print("Found device: " + devices[0].product_name)
ul.create_daq_device(board_num, devices[0])

t_start, t_stop, t_step, t_soak = -40, 85, 5, 10 # start, stop temp...
t_num = (t_stop - t_start)/t_step
wb = xlsxwriter.Workbook('results.xlsx')
sheet1 = wb.add_worksheet('results')

runs = 1000
for i in range(runs):
    # add chamber control

    time.sleep(10)
    ser0.write(cmd0.encode())
    ser1.write(cmd1.encode())
    time.sleep(0.5)
    s0 = ser0.read(100).decode('utf-8')
    acc_temp = int(s0.split()[3][17:])
    s1 = ser1.read(200).decode('utf-8')
    t1 = s1.find("test")
    t2 = s1.find("please")
    s1 = s1[t1 + 6: t2 -3]
    ain6 = int(s1[7:])

    ch0 = float("{:.2f}".format(ul.t_in(board_num, channel0, 0)))
    ch1 = float("{:.2f}".format(ul.t_in(board_num, channel1, 0)))
    ch2 = float("{:.2f}".format(ul.t_in(board_num, channel2, 0)))
    ch3 = float("{:.2f}".format(ul.t_in(board_num, channel3, 0)))
    print(acc_temp, ain6, ch0, ch1, ch2, ch3)
    
    # sheet1.write(i + 1, 0, t_start + t_step * i) # write temp setting in excel
    sheet1.write(i + 1, 1, ain6) # write adc reading
    sheet1.write(i + 1, 2, acc_temp)
    sheet1.write(i + 1, 3, ch0)
    sheet1.write(i + 1, 4, ch1)    
    sheet1.write(i + 1, 5, ch2)
    sheet1.write(i + 1, 6, ch3)    
wb.close()
ser0.close()
ser1.close()
ul.release_daq_device(board_num)