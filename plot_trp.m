# this script reads and plot data from a TRP antenna test results in txt file, script works in Octave
pin = 19.3; # user input, conducted output power
m = 11;                                      # [15:15:165]
step_theta = 180 / (m + 1);
n = 24;                                      # [0:15:345]
step_phi = 360 / n;                           # data in example is 11 * 24
AAA = fopen('b1_902.4MHz.txt', 'rt');
data = textscan(AAA, '%f %f %f %f %f', 'HeaderLines', 4);
eirp = zeros(m, n);
trp = 0;
for i = 1 : m
    for j = 1 : n
      eirp(i, j) = data{1, 5}((j - 1) * m + i);
      trp = trp + sind(i * step_theta) * 10 ^ (eirp(i, j) / 10);
    end
end
trp = 10 * log10(trp * pi / 2 / (m + 1) /n)
peak_eirp = max(max(eirp))
gain = peak_eirp - pin
directivity = peak_eirp - trp
efficiency = 100 * 10 ^ ((trp - pin) / 10)

x = zeros(m + 2, n + 1);
y = zeros(m + 2, n + 1);
z = zeros(m + 2, n + 1);
r = zeros(m + 2, n + 1);
for i = 1 : m
    for j = 1 : n
        x(i + 1, j) = eirp(i, j) * sind(i * step_theta) * cosd((j - 1) * step_phi);
        y(i + 1, j) = eirp(i, j) * sind(i * step_theta) * sind((j - 1) * step_phi);
        z(i + 1, j) = eirp(i, j) * cosd(i * step_theta);
    end
end
x(:, n + 1) = x(:, 1); # copy phi = 0 to phi = 360
y(:, n + 1) = y(:, 1);
z(:, n + 1) = z(:, 1);
x(1, :) = mean(x(2, :)); # theta = 0 is the average of theta = 15 points because it is not given.
y(1, :) = mean(y(2, :));
z(1, :) = mean(z(2, :));
x(m + 2, :) = mean(x(m + 1, :)); # theta = 360 is the mean of theta = 345 points because it is not given. 
y(m + 2, :) = mean(y(m + 1, :));
z(m + 2, :) = mean(z(m + 1, :));
r = sqrt(x.^2 + y.^2 + z.^2); # r is amplitude

##figure(1) # default view
##surf(x, y, z, r)
##shading(gca,'interp');
##xlabel('x-axis');
##ylabel('y-axis');
##zlabel('z-axis');
##colormap('jet');
##colorbar;
##axis equal;
##
##
##figure(2) # x z view
##surf(x, y, z, r);
##view(0, 0);
##shading(gca,'interp');
##xlabel('x-axis');
##zlabel('z-axis');
##title('X-Z View');
##colormap('jet');
##colorbar;
##axis equal;
##
##figure(3) # y z view
##surf(x, y, z, r);
##view(90, 0);
##shading(gca,'interp');
##ylabel('y-axis');
##zlabel('z-axis');
##title('Y-Z View');
##colormap('jet');
##colorbar;
##axis equal;
##
##figure(4) # x y view, view from top to bottom
##surf(x, y, z, r);
##view(0, 90);
##shading(gca,'interp');
##xlabel('x-axis');
##ylabel('y-axis');
##title('X-Y View');
##colormap('jet');
##colorbar;
##axis equal;

##figure(5) # reverse x z view
##surf(x, y, z, r);
##view(180, 0);
##shading(gca,'interp');
##xlabel('x-axis');
##zlabel('z-axis');
##title('Reverse X-Z View');
##colormap('jet');
##colorbar;
##axis equal;
##
##figure(6) # reverse y z view
##surf(x, y, z, r);
##view(270, 0);
##shading(gca,'interp');
##ylabel('y-axis');
##zlabel('z-axis');
##title('Reverse Y-Z View');
##colormap('jet');
##colorbar;
##axis equal;

##figure(7) # reverse x y view, view from bottom
##surf(x, y, z, r);
##view(180, 270);
##shading(gca,'interp');
##xlabel('x-axis');
##ylabel('y-axis');
##title('Reverse X-Y View');
##colormap('jet');
##colorbar;
##axis equal;

##azimuth plot, theta = 90
##figure(8)
##eirp_azi = eirp((m + 1)/2, :);
##eirp_azi(1, n + 1) = eirp_azi(1, 1);
##polar(linspace(0, 2 * pi, n + 1), eirp_azi)
##title('Azimuth plane \theta = 90')

## elevation plot, phi = 0, 180
##figure(9)
##eirp_elev = zeros(1, n + 1);
##for i = 1:6
##  eirp_elev(i) = eirp(7 - i, 1); # 1:6
##  eirp_elev(i + 7) = eirp(i, 13); # 8:13
##end
##for j = 1:5
##  eirp_elev(j + 13) = eirp(j + 6, 13); # 14: 18
##  eirp_elev(j + 19) = eirp(12 - j, 1); # 20: 24
##end
##eirp_elev(7) = (eirp_elev(6) + eirp(8))/2; #7
##eirp_elev(19)  = (eirp_elev(18) + eirp_elev(20))/2;
##eirp_elev(n + 1) = eirp(6, 1);# 25
##polar(linspace(0, 2 * pi, n + 1), eirp_elev)
##title('Elevation plane \phi = 0, 180')