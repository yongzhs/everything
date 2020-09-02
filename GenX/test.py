import subprocess
from subprocess import PIPE

# out = subprocess.run('wsl ./net_mgr -d 10.0.0.2', shell = True, stdout = PIPE, stderr = PIPE)
# out = subprocess.run('pwd', shell = True, stdout = PIPE, stderr = PIPE)
# subprocess.run("cd /", shell = True, stdout = PIPE, stderr = PIPE)
# subprocess.run("cd RF_DVT/ColumbusHwDev.RF_DVT/SUN_RF_Validation_Scripts/", shell = True, cwd = 'C:\RF_DVT\ColumbusHwDev.RF_DVT\SUN_RF_Validation_Scripts', stdout = PIPE, stderr = PIPE)
# out = subprocess.run('pwd', shell = True, stdout = PIPE, stderr = PIPE)
out = subprocess.run("wsl ./net_mgr", shell = True, cwd = 'C:\RF_DVT\ColumbusHwDev.RF_DVT\SUN_RF_Validation_Scripts', stdout = PIPE, stderr = PIPE)

print(out.stdout)
