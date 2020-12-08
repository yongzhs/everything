import matplotlib.pyplot as plt
import numpy as np
y1 = [-1.8, 2.5, 6.8, 10.6, 14.4, 18.4, 22.3, 26.4, 30.1, 33.7, 37.9, 41.8, 45.6, 49.3, 53.6, 57.5, 61.3, 65, 69, 73, 76.8, 80.5, 84.8, 88.5] # board 1
z1 = [-3.3, 0.9, 5.2, 9, 12.7, 16.7, 20.8, 24.8, 28.5, 32.2, 36.2, 40.2, 44, 47.8, 52, 55.8, 59.8, 63.2, 67.4, 71.3, 75.1, 78.7, 83, 86.8]
x1 = [1820, 1855, 1896, 1932, 1968, 2007, 2045, 2083, 2126, 2153, 2193, 2231, 2268, 2303, 2344, 2380, 2416, 2450, 2487, 2522, 2554, 2584, 2618, 2644]
xv1 = [i * 2.625 /4095 for i in x1]

y2 = [-1.6, 2.6, 6.8, 10.8, 14.5, 18.3, 22.4, 26.4, 30.1, 33.3, 37.5, 41.4, 45.3, 49, 53.3, 57.1, 61, 64.6, 68.7, 72.7, 76.5, 80.2, 84.3, 88.2] # board 2
z2 = [-3, 1.2, 5.4, 9.3, 12.9, 17, 20.9, 24.9, 28.6, 31.9, 36, 39.9, 43.9, 47.7, 51.9, 55.8, 59.5, 63.3, 67.2, 71.2, 75, 78.8, 82.9, 86.7]
x2 = [1792, 1825, 1863, 1899, 1930, 1965, 2003, 2038, 2080, 2105, 2143, 2180, 2214, 2248, 2288, 2322, 2357, 2390, 2424, 2460, 2491, 2532, 2556, 2582]
xv2 = [i * 2.6433 /4095 for i in x2]

y3 = [-14.9, -11.3, -7.6, -3.6, 0.3, 4.1, 7.8, 11.8, 15.7, 19.7, 23.7, 27.8, 31.4, 35.4, 39.2, 41.9, 48.2, 50, 57.3, 64.8, 72.4, 76.4, 79.7, 83.9, 87.5] # board 3
z3 = [-16.4, -12.7, -8.9, -5.2, -1.3, 2.6, 6.3, 10.4, 14.4, 18.4, 22.4, 26.2, 29.9, 33.9, 37.7, 40.5, 47.4, 49, 56.4, 63.8, 71.4, 75.4, 78.6, 82.9, 86.5]
x3 = [1659, 1692, 1726, 1761, 1796, 1830, 1866, 1904, 1939, 1978, 2014, 2052, 2086, 2124, 2161, 2184, 2239, 2259, 2321, 2386, 2445, 2482, 2499, 2529, 2548]
xv3 = [i * 2.6504 /4095 for i in x3]

y4 = [-14.7, -10.9, -7, -3.1, 0.9, 4.7, 8.7, 12.7, 16.7, 20.8, 24.9, 28.9, 32.6, 36.8, 40.3, 42.4, 49.1, 51, 58.3, 65.6, 73.2, 77.6, 80.5, 84.9, 88.3] # board 4
z4 = [-16.2, -12.5, -8.5, -4.5, -0.7, 3.2, 7.4, 11.2, 15.2, 19.3, 23.3, 27.4, 31.1, 35.2, 38.6, 40.9, 47.7, 49.7, 56.9, 64.4, 71.8, 76.3, 79.1, 83.5, 86.9]
x4 = [1729, 1761, 1793, 1827, 1861, 1895, 1929, 1964, 1999, 2036, 2072, 2107, 2141, 2177, 2213, 2239, 2299, 2311, 2378, 2444, 2506, 2538, 2562, 2589, 2612]
xv4 = [i * 2.6414 /4095 for i in x4]

z5 = [-16, -11.7, -8.3, -4.5, -0.6, 3.2, 7.2, 11.7, 14.9, 19.3, 23, 27, 30.8, 34.7, 38.6, 42.4, 46.3, 50.3, 54.3, 58, 62, 65.9, 69.8, 73.7, 77.6, 81.5, 85.3, 89.3] # board 5
x5 = [1794, 1820, 1852, 1888, 1923, 1957, 1999, 2033, 2066, 2110, 2137, 2176, 2215, 2254, 2291, 2327, 2364, 2402, 2440, 2476, 2512, 2547, 2580, 2613, 2645, 2675, 2701, 2724]
xv5 = [i * 2.649 /4095 for i in x5]

z6 = [-17.9, -13.6, -10.4, -6.5, -2.4, 1.3, 5.3, 9.8, 13, 17.5, 21.3, 25.3, 28.9, 32.9, 38.4, 40.8, 44.8, 48.7, 52.7, 56.6, 60.6, 64.5, 68.5, 72.4, 76.3, 80.3, 84.2, 88.3] # board 6
x6 = [1710, 1740, 1770, 1806, 1840, 1874, 1911, 1952, 1983, 2020, 2058, 2092, 2130, 2167, 2203, 2240, 2277, 2313, 2348, 2384, 2418, 2452, 2483, 2512, 2540, 2567, 2588, 2606]
xv6 = [i * 2.647 /4095 for i in x6]

z7 = [-18.6, -14, -11, -6.8, -3.1, 0.6, 4.8, 9.7, 12.4, 17.2, 20.8, 24.8, 28.4, 32.3, 36.3, 40.3, 44.1, 48.2, 52.2, 56, 60, 64, 67, 72, 75.9, 79.8, 83.6, 88.2] # board 7
x7 = [1724, 1757, 1785, 1821, 1855, 1888, 1935, 1965, 1996, 2035, 2077, 2106, 2145, 2184, 2222, 2260, 2298, 2335, 2373, 2413, 2451, 2490, 2529, 2566, 2603, 2641, 2678, 2710]
xv7 = [i * 2.629 /4095 for i in x7]

z8 = [-19.7, -15, -12, -7.9, -4.1, -0.3, 3.7, 8.7, 11.4, 16.2, 19.7, 23.7, 27.3, 31.2, 35.3, 39.2, 43.2, 47.1, 51.2, 55.1, 59.1, 63.1, 67, 71, 74.9, 78.9, 82.8, 87.5] # board 8
x8 = [1657, 1688, 1717, 1751, 1783, 1815, 1861, 1891, 1922, 1963, 1989, 2026, 2063, 2099, 2135, 2171, 2207, 2243, 2278, 2312, 2347, 2380, 2413, 2444, 2474, 2504, 2529, 2552]
xv8 = [i * 2.631 /4095 for i in x8]

x = x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8
z = z1 + z2 + z3 + z4 + z5 + z6 + z7 + z8
xv = xv1 + xv2 + xv3 + xv4 + xv5 + xv6 + xv7 + xv8

# fig = plt.figure(1)
# ax = fig.gca()
# ax.set_xticks(np.arange(1600, 2800, 100))
# ax.set_yticks(np.arange(-30, 90, 10))
# plt.plot(x1, z1, 'b+')
# plt.plot(x2, z2, 'g*')
# plt.plot(x3, z3, 'ro')
# plt.plot(x4, z4, 'c*')
# plt.plot(x5, z5, 'mv')
# plt.plot(x6, z6, 'y^')
# plt.plot(x7, z7, 'k<')
# plt.plot(x8, z8, 'c>')

# a = np.polyfit(x, z, 1)
# x0 = np.linspace(1600, 2700)
# plt.plot(x0, [(a[0] * x + a[1]) for x in x0])
# plt.grid(), plt.show()

fig = plt.figure(1)
ax = fig.gca()
ax.set_xticks(np.arange(1, 1.8, 0.1))
ax.set_yticks(np.arange(-30, 90, 10))
plt.plot(xv1, z1, 'b+')
plt.plot(xv2, z2, 'g*')
plt.plot(xv3, z3, 'ro')
plt.plot(xv4, z4, 'c*')
plt.plot(xv5, z5, 'mv')
plt.plot(xv6, z6, 'y^')
plt.plot(xv7, z7, 'k<')
plt.plot(xv8, z8, 'c>')

a = np.polyfit(xv, z, 1)
x0 = np.linspace(1, 1.8)
plt.plot(x0, [(a[0] * x + a[1]) for x in x0])
plt.grid(), plt.show()