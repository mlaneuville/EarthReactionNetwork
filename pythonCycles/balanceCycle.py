import json, argparse
from pprint import pprint

parser = argparse.ArgumentParser(description="Balances and prints a given chemical cycle.")
parser.add_argument("-c", "--cycle", help="Name of the datafile to load.", required=True)
args = vars(parser.parse_args())

print "Loading "+args["cycle"]+" data..."
with open(args["cycle"]) as data_file:
    data = json.load(data_file)

### === ### === ### === ### === ### === ### === ### === ### === ### === ### === ### === ### ===

def carbonDioxideBalance(x):
    #    sinks = W_C + W_CSIL + W_OSIL + B_POC + B_AC + B_CH4
    #    sources = D_M + D_C + D_POC + W_POC + B_BC
    sinks = x[8] + x[9] + x[10] + x[4] + x[1] + x[3]
    sources = x[6] + x[5] + x[7] + x[11] + x[2]
    return (sinks - sources)**2

def carbonBalance(x):
    #    sinks = B_BC + B_POC + B_AC + B_CH4 + A_OC
    #    sources = D_M + D_C + D_POC + W_POC + W_C
    sinks = x[2] + x[4] + x[1] + x[3] + x[0]
    sources = x[6] + x[5] + x[7] + x[11] + x[8]
    return (sinks - sources)**2

def isotopeBalance(x):
    #    sinks = d_CA*(B_BC+A_OC) + d_PA*(B_POC+B_AC+B_CH4)
    #    sources = d_M*D_M + d_CW*(D_C+W_C) + d_PW*(D_POC+W_POC)
    sinks = d_CA*(x[2]+x[0]) + d_PA*(x[4]+x[1]+x[3])
    sources = d_M*x[6] + d_CW*(x[5]+x[8]) + d_PW*(x[7]+x[11])
    return (sinks - sources)**2

def masterBalance(x):
    return carbonBalance(x) + carbonDioxideBalance(x) + isotopeBalance(x)

### === ### === ### === ### === ### === ### === ### === ### === ### === ### === ### === ### ===

import numpy as np
import scipy.optimize as o
import random as r

x0 = []
b = []

cycle = "CarbonCycle"
for key in sorted(data[cycle+"Fluxes"]):
    max = data[cycle+"Fluxes"][key]["maxVal"]
    min = data[cycle+"Fluxes"][key]["minVal"]
    b.append((min,max))
    x0.append(r.uniform(min, max))

d_CA = data[cycle+"Isotopes"]["d_CA"]
d_PA = data[cycle+"Isotopes"]["d_PA"]
d_M = data[cycle+"Isotopes"]["d_M"]
d_CW = data[cycle+"Isotopes"]["d_CW"]
d_PW = data[cycle+"Isotopes"]["d_PW"]

x0 = np.array(x0)
x,f,d = o.fmin_l_bfgs_b(masterBalance, x0, approx_grad=1, bounds=b)

if(d['warnflag'] == 0):
    print "Optimization has converged!"
if(d['warnflag'] == 1):
    print "Optimization has not converged: too many iterations or function evaluations."
if(d['warnflag'] == 2):
    print "Optimization has not converged:"
    print d['task']

print
print "Proposed solution:"
for i, key in enumerate(sorted(data[cycle+"Fluxes"])):
    print "%s = %5.2f" % (key, x[i])
print
print "Total distance to perfect balance = %5.2f" % masterBalance(x)
print "- From carbon balance = %5.2f" % carbonBalance(x)
print "- From CO2 balance = %5.2f" % carbonDioxideBalance(x)
print "- From isotope composition = %5.2f" % isotopeBalance(x)