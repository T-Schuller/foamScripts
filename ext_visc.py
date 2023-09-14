#!/home/schuller/anaconda3/bin/python3
from matplotlib import pyplot as plt
import subprocess
import numpy as np
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

#print(os.curdir)
root = YOUR_FILEDIRECTORY
path = root + MATERIAL_PATH


# # source of7
# commands = 'source /opt/openfoam7/etc/bashrc && '

# # source of7libs
# commands += 'export LD_LIBRARY_PATH=$PETSC_DIR/$PETSC_ARCH/lib:$LD_LIBRARY_PATH && '

# # run allclean
# commands += 'bash ' + path + 'Allclean && '

# # run allrun
# commands += 'bash ' + path + 'Allrun'

# # start commands
# p = subprocess.Popen(commands, shell=True, executable='/bin/bash')
# # wait to finish
# p.communicate()
# print('Ext Finito!')



report = pd.read_csv(path + 'Report', sep='\s+', lineterminator='\n',header=None, on_bad_lines='skip')

#print('report data', report.head)

ext_rate=float(report.iloc[0, 6])

report = pd.read_csv(path + 'Report', sep='\t', lineterminator='\n',skiprows=(1), index_col=False, on_bad_lines='skip')

#print('report data', report.head)

rep_time=list(report.iloc[:, 0])
rep_ext_XX=list(report.iloc[:, 1])
rep_ext_YY=list(report.iloc[:, 4])

ext_visc=np.array([(rep_ext_XX[x]-rep_ext_YY[x])/ext_rate for x in range(0,len(rep_ext_XX))])
#print(ext_visc[0])
exp_report = pd.read_excel(YOUR_EXCEL_FILE,sheet_name=3,skiprows=(6))

#print('exp_report data', exp_report.head)

exp_time_3=list(exp_report['3s-1'])
exp_time_1=list(exp_report['1s-1'])
exp_time_0_3=list(exp_report['0,3s-1'])
exp_time_0_1=list(exp_report['0,1s-1'])


exp_visc_3=list(exp_report['3s-1 - exp'])
exp_visc_1=list(exp_report['1s-1 - exp'])
exp_visc_0_3=list(exp_report['0,3s-1 - exp'])
exp_visc_0_1=list(exp_report['0,1s-1 - exp'])


# num_time_3=list(exp_report['3s-1 - t_num'])
# num_time_1=list(exp_report['1s-1 - t_num'])
# num_time_0_3=list(exp_report['0,3s-1 - t_num'])
# num_time_0_1=list(exp_report['0,1s-1 - t_num'])

num_time_3=exp_time_3
num_time_1=exp_time_1
num_time_0_3=exp_time_0_3
num_time_0_1=exp_time_0_1

num_visc_3=list(exp_report['3s-1 - num'])
num_visc_1=list(exp_report['1s-1 - num'])
num_visc_0_3=list(exp_report['0,3s-1 - num'])
num_visc_0_1=list(exp_report['0,1s-1 - num'])

fig2, ax2 = plt.subplots()

plt.axis([0.004, 30, 100, 30000])



ax2.plot(exp_time_0_1, exp_visc_0_1,label=r'Experimental 0.1s-1', color='C0',marker='o',linestyle='', lw=1.,markevery=4)
ax2.plot(exp_time_0_3, exp_visc_0_3,label=r'Experimental 0.3s-1', color='C1',marker='o',linestyle='', lw=1.,markevery=4)
ax2.plot(exp_time_1, exp_visc_1,label=r'Experimental 1s-1', color='k',marker='o',linestyle='', lw=1.,markevery=4)
ax2.plot(exp_time_3, exp_visc_3,label=r'Experimental 3s-1', color='g',marker='o',linestyle='', lw=1.,markevery=4)


# if ext_rate==0.1:
#     file = open(root + "0_1_ext.txt", "a")
#     np.savetxt(file, ext_visc, newline=" ")
#     file.write('\n')
#     file.close()
#     data = np.loadtxt(root + "0_1_ext.txt")
#     ax2.plot(rep_time, data[-1,:],label=r'N. 0.1s-1 - 1st', color='C0',marker='',linestyle='solid', lw=3., alpha=1)
#     ax2.plot(rep_time, data[-2,:],label=r'N. 0.1s-1 - 2nd', color='C0',marker='',linestyle='dashed', lw=3., alpha=0.5)
#     ax2.plot(rep_time, data[-3,:],label=r'N. 0.1s-1 - 3rd', color='C0',marker='',linestyle='dashdot', lw=3., alpha=0.3)
#     ax2.plot(rep_time, data[-4,:],label=r'N. 0.1s-1 - 4th', color='C0',marker='',linestyle='dotted', lw=3., alpha=0.1)


#     ax2.plot(exp_time_0_1, exp_visc_0_1,label=r'Experimental 0.1s-1', color='C0',marker='o',linestyle='', lw=1., alpha=1)
    
# elif ext_rate==0.3:
#     file = open(root + "0_3_ext.txt", "a")
#     data = np.loadtxt(root + "0_3_ext.txt")
#     if np.array_equal(ext_visc,data[-1,:])==False:
#         np.savetxt(file, ext_visc, newline=" ")
#         file.write('\n')
#     file.close()
#     data = np.loadtxt(root + "0_3_ext.txt")
#     ax2.plot(rep_time, data[-1,:],label=r'N. 0.3s-1 - 1st', color='C1',marker='',linestyle='solid', lw=3., alpha=1)
#     ax2.plot(rep_time, data[-2,:],label=r'N. 0.3s-1 - 2nd', color='C1',marker='',linestyle='dashed', lw=3., alpha=0.5)
#     ax2.plot(rep_time, data[-3,:],label=r'N. 0.3s-1 - 3rd', color='C1',marker='',linestyle='dashdot', lw=3., alpha=0.3)
#     ax2.plot(rep_time, data[-4,:],label=r'N. 0.3s-1 - 4th', color='C1',marker='',linestyle='dotted', lw=3., alpha=0.1)


#     ax2.plot(exp_time_0_3, exp_visc_0_3,label=r'Experimental 0.3s-1', color='C1',marker='o',linestyle='', lw=1., alpha=1)

# elif ext_rate==1:
#     file = open(root + "1_ext.txt", "a")
#     np.savetxt(file, ext_visc, newline=" ")
#     file.write('\n')
#     file.close()
#     data = np.loadtxt(root + "1_ext.txt")
#     ax2.plot(rep_time, data[-1,:],label=r'N. 1s-1 - 1st', color='k',marker='',linestyle='solid', lw=3., alpha=1)
#     ax2.plot(rep_time, data[-2,:],label=r'N. 1s-1 - 2nd', color='k',marker='',linestyle='solid', lw=3., alpha=0.7)
#     ax2.plot(rep_time, data[-3,:],label=r'N. 1s-1 - 3rd', color='k',marker='',linestyle='solid', lw=3., alpha=0.4)
#     ax2.plot(rep_time, data[-4,:],label=r'N. 1s-1 - 4th', color='k',marker='',linestyle='solid', lw=3., alpha=0.2)


#     ax2.plot(exp_time_1, exp_visc_1,label=r'Experimental 1s-1', color='k',marker='o',linestyle='', lw=1., alpha=1)
    
# elif ext_rate==3:
#     file = open(root + "3_ext.txt", "a")
#     np.savetxt(file, ext_visc, newline=" ")
#     file.write('\n')
#     file.close()
#     data = np.loadtxt(root + "3_ext.txt")
#     ax2.plot(rep_time, data[-1,:],label=r'N. 3s-1 - 1st', color='g',marker='',linestyle='solid', lw=3., alpha=1)
#     ax2.plot(rep_time, data[-2,:],label=r'N. 3s-1 - 2nd', color='g',marker='',linestyle='dashed', lw=3., alpha=0.5)
#     ax2.plot(rep_time, data[-3,:],label=r'N. 3s-1 - 3rd', color='g',marker='',linestyle='dashdot', lw=3., alpha=0.3)
#     ax2.plot(rep_time, data[-4,:],label=r'N. 3s-1 - 4th', color='g',marker='',linestyle='dotted', lw=3., alpha=0.1)


#     ax2.plot(exp_time_3, exp_visc_3,label=r'Experimental 3s-1', color='g',marker='o',linestyle='', lw=1., alpha=1)
    
ax2.plot(num_time_0_1, num_visc_0_1,label=r'Numerical 0.1s-1', color='C0',marker='',lw=1.)
ax2.plot(num_time_0_3, num_visc_0_3,label=r'Numerical 0.3s-1', color='C1',marker='',lw=1.)
ax2.plot(num_time_1, num_visc_1,label=r'Numerical 1s-1', color='k',marker='',lw=1.)
ax2.plot(num_time_3, num_visc_3,label=r'Numerical 3s-1', color='g',marker='',lw=1.)

plt.xscale('log')
plt.yscale('log')

ax2.set_xlabel(r'Time $t_{e} [s]$')
ax2.set_ylabel(r'Extensional Viscosity $(\eta_{E}) [Pa.s]$')

ax2.legend()




plt.show()

#plt.savefig('ext_visc_petcf.pdf')
