#!/home/schuller/anaconda3/bin/python3
import subprocess
from matplotlib import pyplot as plt
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

#print(os.curdir)

dir_path = YOUR_FILEDIRECTORY


# # source of7
# commands = 'source /opt/openfoam7/etc/bashrc && '

# # source of7libs
# commands += 'export LD_LIBRARY_PATH=$PETSC_DIR/$PETSC_ARCH/lib:$LD_LIBRARY_PATH && '

# # run allclean
# commands += 'bash ' + dir_path + 'multimode_Giesekus_shear_PLA/' + 'Allclean && '

# # run allrun
# commands += 'bash ' + dir_path + 'multimode_Giesekus_shear_PLA/' + 'Allrun'

# # start commands
# p = subprocess.Popen(commands, shell=True, executable='/bin/bash')
# # wait to finish
# p.communicate()
# print('Shear Finito!')


report = pd.read_csv(dir_path + YOUR_ECXEL_FILE, sep='\t', lineterminator='\n',skiprows=(1), index_col=False, on_bad_lines='skip')

#print('report data', report.head)

rep_time=list(report.iloc[:, 0])
rep_shear_XX=list(report.iloc[:, 2])

shear_visc=[rep_shear_XX[x]/rep_time[x] for x in range(0,len(rep_shear_XX))]

exp_report = pd.read_excel(dir_path + OTHER_ECXEL_FILE,sheet_name=4,skiprows=(1))

#print('exp_report data', exp_report.head)

saos_time=list(exp_report['Angular frequency'])

saos_visc=list(exp_report['saos'])

exp_time=list(exp_report['shear rate'])

exp_visc=list(exp_report['shear'])

fig2, ax2 = plt.subplots(figsize = (6,3.5))

plt.axis([0.1, 1000, 10, 1000])




ax2.plot(exp_time, exp_visc,label=r'Steady Shear',marker='o',linestyle='dashed', lw=1. ,color ='C1')
ax2.plot(saos_time, saos_visc,label=r'SAOS',marker='s',linestyle='dotted', lw=1. ,color ='k')
ax2.plot(rep_time, shear_visc,label=r'Numerical',marker='^',linestyle='solid', lw=1. ,color ='C0')

plt.xscale('log')
plt.yscale('log')

ax2.set_xlabel(r'Shear Rate $(\dot{\gamma}) [s^{-1}]$')
ax2.set_ylabel(r'Viscosity $(\eta) [Pa.s]$')

ax2.legend()




#plt.show()
plt.savefig('shear_visc_new_petcf.pdf')
