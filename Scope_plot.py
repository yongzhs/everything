import visa
import matplotlib.pyplot as plt
import time

rm = visa.ResourceManager()
rm.list_resources()
s = rm.open_resource('TCPIP0::172.17.213.103::inst0::INSTR')
print(s.query('*IDN?'))
duration = 300
v1 = [0 for i in range(duration)]
v2 = [0 for i in range(duration)]
for i in range(duration):
    s.write('CURSor:SOUrce CH1')
    time.sleep(0.5)
    v1[i] = float(s.query('CURSor:VBArs:HPOS1?').split(' ', 1)[-1])
    print(v1[i])

    s.write('CURSor:SOUrce CH2')
    time.sleep(0.5)
    v2[i] = float(s.query('CURSor:VBArs:HPOS1?').split(' ', 1)[-1])
    print(v2[i])

plt.plot(v2)
plt.plot(v1)

plt.ylabel('Voltage (V)')
plt.xlabel('Time (s)')