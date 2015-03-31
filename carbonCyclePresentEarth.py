'''
Balanced Carbon cycle for present Earth from the textbook
Fundamentals of Geobiology (Knoll, Canfield, Konhauser).
'''

# burial = atmosphere/ocean -> oceanic crust
# degassing = crust/mantle -> atmosphere/ocean
# weathering = continental crust -> atmosphere/ocean
# subduction = oceanic crust -> mantle
# alteration = atmosphere/ocean -> oceanic crust
# accretion = oceanic -> continental crust
# erosion = continental crust -> oceaninc crust

# POC = particulate organic carbon
# CH4 = methane
# C = carbonate minerals
# BC = biogenic carbonates
# AC = authigenic carbonates
# OC = oceanig crust
# M = mantle

fluxes = {}
isotopes = {}

# Carbon sources
fluxes['D_M'] = (4.3, 3.1, 5.5)     # degassing
fluxes['W_C'] = (11.7, 10.0, 16.0)  # weathering
fluxes['D_C'] = (2.5, 2.0, 4.0)     # degassing
fluxes['D_POC'] = (0.5, 0.4, 0.6)   # degassing
fluxes['W_POC'] = (9.0, 8.0, 16.0)  # weathering

# Carbon sinks
fluxes['B_BC'] = (16.0, 14.0, 17.0) # burial
fluxes['A_OC'] = (2.0, 1.5, 2.4)    # alteration
fluxes['B_CH4'] = (0.0, 0.0, 0.0)   # burial -- included in B_POC
fluxes['B_AC'] = (0.0, 0.0, 0.0)    # burial -- included in B_POC
fluxes['B_POC'] = (10.0, 5.4, 27.0) # burial -- includes B_AC and B_CH4

# CO2 sinks
fluxes['W_CSIL'] = (7.1, 6.0, 10.0) # chemical weathering of silicate rocks on land (6-10 Tmol/yr)
fluxes['W_OSIL'] = (3.5, 3.3, 13.3) # chemical weathering of silicates in marine sediments (3.3-13.3 Tmol/yr)

# isotopic compositions
d_CA = 0.0      # carbonate minerals accumulating at seafloor
d_PA = -0.024   # sedimentary POC accumulating at seafloor
d_M = -0.005    # mantle CO2
d_CW = 0.002    # carbonate minerals subject to weathering and metamorphosis
d_PW = -0.026   # POC subject to weathering and metamorphosis

### === ### === ### === ### === ### === ### === ### === ### === ### === ### === ### === ### ===

def carbonDioxideBalance(x):
#    sinks = W_C + W_CSIL + W_OSIL + B_POC + B_AC + B_CH4
#    sources = D_M + D_C + D_POC + W_POC + B_BC
    sinks = x[8] + x[9] + x[10] + x[4] + x[1] + x[3]
    sources = x[6] + x[5] + x[7] + x[11] + x[2]
    return abs(sinks - sources)

def carbonBalance(x):
#    sinks = B_BC + B_POC + B_AC + B_CH4 + A_OC
#    sources = D_M + D_C + D_POC + W_POC + W_C
    sinks = x[2] + x[4] + x[1] + x[3] + x[0]
    sources = x[6] + x[5] + x[7] + x[11] + x[8]
    return abs(sinks - sources)

def isotopeBalance(x):
#    sinks = d_CA*(B_BC+A_OC) + d_PA*(B_POC+B_AC+B_CH4)
#    sources = d_M*D_M + d_CW*(D_C+W_C) + d_PW*(D_POC+W_POC)
    sinks = d_CA*(x[2]+x[0]) + d_PA*(x[4]+x[1]+x[3])
    sources = d_M*x[6] + d_CW*(x[5]+x[8]) + d_PW*(x[7]+x[11])
    return abs(sinks - sources)

def masterBalance(x):
    return carbonBalance(x) + carbonDioxideBalance(x) + isotopeBalance(x)

### === ### === ### === ### === ### === ### === ### === ### === ### === ### === ### === ### ===

import numpy as np
import scipy.optimize as o
import random as r

x0 = []
b = []

for i, key in enumerate(sorted(fluxes)):
    x0.append(fluxes[key][0])
    b.append((fluxes[key][1], fluxes[key][2]))

for i in range(len(x0)):
    x0[i] = r.uniform(b[i][0], b[i][1])

x0 = np.array(x0)
x,f,d = o.fmin_l_bfgs_b(carbonDioxideBalance, x0, approx_grad=1, bounds=b)

if(d['warnflag'] != 0):
    print "Optimization has not converged: " + str(d['warnflag'])
    if(d['warnflag'] == 2):
        print d['task']

print "Proposed solution:"
for i, key in enumerate(sorted(fluxes)):
    print "%s = %5.2f" % (key, x[i])
print
print "Total distance to perfect balance = %5.2f" % masterBalance(x)
print "- From carbon balance = %5.2f" % carbonBalance(x)
print "- From CO2 balance = %5.2f" % carbonDioxideBalance(x)
print "- From isotope composition = %5.2f" % isotopeBalance(x)