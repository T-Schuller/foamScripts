#!/home/schuller/miniconda3/bin/python3
from matplotlib import pyplot as plt
import numpy as np

'''
How to run streamline script

1. Open simulation
2. Slice in Z
3. Make 1 streamline between as close to the reentrant corner as possible
4. Apply CellDatatoPointData filter and create spreadsheet window
5. Export CSV with name streamlines_MATERIAL_SPEED.csv
6. Open script streamliner.py
7. Search for the ideal section to do the fitting
8. Use the given point as center to get speed and tension tensor.
9. Input tauxy, tauxx and tauyy
10. Input tau11, tau12 and magnitude of velocity at point to excel
'''

root = YOUR_ROOT

# LOAD CSV ##################################################################
#  CSV data input (streamline info from ParaView)
data = np.genfromtxt(root+CSV_FILE_STREAMLINES, delimiter=',', names=True)
streamline_ids = np.unique(data['SeedIds']).astype(int)

# separation between abscissa and ordinate (x's and y's)
x = data['Points0']
y = data['Points1']

# ordering of vectors based on the abscissae
# (the paraview vector comes all disorganized)
# These are the indices that will be used to reorder the vectors.
sorted_inds = np.argsort(x)
# print(x)
# Sorting the vectors based on the indices calculated above
x = x[sorted_inds]
y = y[sorted_inds]
#############################################################################


# plot for visual inspection of the curve section to be fitted
fig1, ax1 = plt.subplots()
fig1.suptitle('Streamline')
ax1.plot(x,y,marker='x')
plt.axis('equal')
plt.show()

lim_esquerdo_user = float(input("Left limit (*1e-2)= "))*1e-2
lim_direito_user = float(input("Right limit (*1e-2)= "))*1e-2
abcissa_ponto_a_calcular_Rc = float(input("X of point to determine Rc (*1e-2)= "))*1e-2

# Test values for a template curve
# lim_esquerdo_user = 3.2427*1e-2
# lim_direito_user = 3.261*1e-2
# abcissa_ponto_a_calcular_Rc = 3.2461*1e-2

# definition of the closest datapoints to the defined limits
lim_e = np.argmin(np.abs(x - lim_esquerdo_user))
lim_d = np.argmin(np.abs(x - lim_direito_user))

# After visual inspection, this stretch was chosen for fitting a polynomial
slice = np.s_[lim_e:lim_d]

# np.polifit used to determine the coefficients of the polynomial
# that best approximates the selected stretch. 3rd order.
fit_parameters = np.polyfit(x[slice], y[slice], 3)

# First derivative values of the polynomial
fit_parameters_der = fit_parameters[:-1]*np.asarray([3, 2, 1])
# Second derivative values of the polynomial
fit_parameters_der2 = fit_parameters_der[:-1]*np.asarray([2, 1])

# creation of a function that helps to define a polynomial function.
# It facilitates the application of "natural operations" on polynomials.
fit = np.poly1d(fit_parameters)
fit_der = np.poly1d(fit_parameters_der)
fit_der2 = np.poly1d(fit_parameters_der2)

# Creation of an evenly spaced array
xfit = np.linspace(x[slice][0],x[slice][-1])
# Finding the closest point in the array that matches the selected Rc point
i_xfit_pto_rc = np.argmin(np.abs(xfit - abcissa_ponto_a_calcular_Rc))

# equation, first and second derivatives of the polynomial for the array
yfit = fit(xfit)
dydx = fit_der(xfit)
d2ydx2 = fit_der2(xfit)

# function that determines the radius of the circular arc that best 
# approximates the curve at that point.
rc = np.abs(pow(1+pow(dydx,2),3/2)/(d2ydx2))


# Calculated point closest to the Rc abscissa
rc_do_ponto_que_quero = rc[i_xfit_pto_rc]
print('Curvature radius = %.3e' % rc_do_ponto_que_quero)

# Creation of the tangent and normal vectors to the circular arc
m_vec = -1*np.asarray([dydx[i_xfit_pto_rc], -1])*np.sign(d2ydx2[i_xfit_pto_rc])
m_vec = m_vec/np.sqrt(m_vec[0]**2 + m_vec[1]**2)

m_vec_tang = np.asarray([1,dydx[i_xfit_pto_rc]])*np.sign(d2ydx2[i_xfit_pto_rc])
m_vec_tang = m_vec_tang/np.sqrt(m_vec_tang[0]**2 + m_vec_tang[1]**2)

# Definition of the vector that points to the Rc point coordinates
vec_pos = np.asarray([xfit[i_xfit_pto_rc], yfit[i_xfit_pto_rc]])

# Definition of the arc centerpoint
centro_circ = vec_pos + rc_do_ponto_que_quero*m_vec


x2 = np.asarray([1,dydx[i_xfit_pto_rc]])
x2 = x2/np.sqrt(x2[0]**2 + x2[1]**2)
y2 = -1*np.asarray([dydx[i_xfit_pto_rc], -1])
y2 = y2/np.sqrt(y2[0]**2 + y2[1]**2)

# creating coordinate points of a circumference
t = np.linspace(-np.pi,np.pi,1000)
xexpl = rc[i_xfit_pto_rc]*np.cos(t) + centro_circ[0]
yexpl = rc[i_xfit_pto_rc]*np.sin(t) + centro_circ[1]


### PLOTTING ##################################################################

fig2, ax2 = plt.subplots()
fig2.suptitle('Plotting the streamline, the circumference and the radius at Rc measurement location', fontsize=14)
# Plotting the streamline, the circumference and the radius at Rc measurement location
ax2.plot(x,y,marker='x')
ax2.plot(xexpl, yexpl, label=r"$R_c$ = %.3e" % rc[i_xfit_pto_rc])
ax2.plot([xfit[i_xfit_pto_rc], centro_circ[0]], [yfit[i_xfit_pto_rc],centro_circ[1]], c='C1',marker ='o')
ax2.legend()
ax2.axis('equal')
ax2.set_xlim(xfit[0],xfit[-1])
plt.show()

fig3, ax3 = plt.subplots()
fig3.suptitle('Plotting the sliced streamline, Rc location and the fitted curve', fontsize=14)
# Plotting the sliced streamline, Rc location and the fitted curve
ax3.plot(x[slice],y[slice],marker='x')
ax3.plot(xfit,yfit,c='g')
ax3.plot(xfit[i_xfit_pto_rc],yfit[i_xfit_pto_rc], c='C1',marker ='o')
plt.axis('equal')
plt.show()

fig4, ax4 = plt.subplots()
fig4.suptitle('Plotting the fitted curve and normal and tangent vectors', fontsize=14)
# Plotting the fitted curve and normal and tangent vectors
scaling_factor = 0.3*np.sqrt(pow(xfit[-1]-xfit[0],2)+pow(yfit[-1]-yfit[0],2))
ax4.plot([xfit[i_xfit_pto_rc], xfit[i_xfit_pto_rc]+scaling_factor*x2[0]], [yfit[i_xfit_pto_rc],yfit[i_xfit_pto_rc]+scaling_factor*x2[1]])
ax4.plot([xfit[i_xfit_pto_rc], xfit[i_xfit_pto_rc]+scaling_factor*y2[0]], [yfit[i_xfit_pto_rc],yfit[i_xfit_pto_rc]+scaling_factor*y2[1]])
ax4.plot(xfit,yfit)
ax4.axis('equal')
plt.show()

##############################################################################

# Rc coords output to probe in ParaView
print('Rc point coordinates = ',vec_pos)
print('X_2 vector = ',x2)
print('Y_2 vector = ',y2)

# Creation of rotation matrix for the tension tensor
tr_matrix = np.vstack((x2,y2))

# Input of tension values at Rc coords and
# Creation of cartesian tension tensor
taus_cart = np.matrix(np.ones((2,2)))*float(input("Tau_xy= "))
taus_cart[0,0] = float(input("Tau_xx= "))
taus_cart[1,1] = float(input("Tau_yy= "))


# Rotation of the tension tensor using the rotation matrix
taus_tp = np.matmul(np.matmul(tr_matrix,taus_cart),tr_matrix.T)


# Output of original matrix and invariants
print('Cartesian tensor matrix = \n', taus_cart)
print(np.trace(taus_cart))
print(np.linalg.det(taus_cart))
# Output of rotated matrix and invariants
# Invariants must match
print('Transformed tensor matrix = \n', taus_tp)
print(np.trace(taus_tp))
print(np.linalg.det(taus_tp))
