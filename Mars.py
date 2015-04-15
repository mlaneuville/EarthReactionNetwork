
# coding: utf-8

# # Mars' atmosphere disequilibrium
# 
# The main reason for Mars' atmosphere disequilibrium is the co-existence of CO and O2.    
# In equilibrium, all CO should be oxidized by O2 following 2CO + O2 => 2CO2.    
# 
# As we observe CO today, there must be a source for it. What is its driver?     
# Production of CO occurs through photodissociation of CO2.

# In[96]:

RM = 3390e3 # radius [m]
S = 4*3.1459*RM**2 # surface [m2]
NA = 6.022e23 # Avogadro's number
r = 2.0e12 # dissociation rate [cm-2 s-1]
reactionRate = 1e4*r # reaction rate [m-2 s-1]
year = 365*24*3600 # seconds in a year


# In[97]:

import numpy as np

def chemPot(T, Pi, dH0, dG0):
    R = 8.314
    T0 = 298.
    P0 = 101325.
    a = R*T*np.log(Pi/P0)
    b = (T/T0)*(dG0 - dH0)
    c = dH0
    return a + b + c


# In[98]:

P = 636 # Pa
T = 218 # K

uCO2 = chemPot(T, 0.9597*P, -393.51e3, -394.4e3)
uCO = chemPot(T, 0.000557*P, -110.53e3, -137.23e3)
uO2 = chemPot(T, 0.001460*P, 0., 0.)

print "uCO2 = %5.3f kJ/mol" % (uCO2/1e3)
print "uCO = %5.3f kJ/mol" % (uCO/1e3)
print "uO2 = %5.3f kJ/mol" % (uO2/1e3)


# In[94]:

F = reactionRate*S/NA # mol/s

# 2CO2 -> O2 + 2CO
dG = 2*uCO + uO2 - 2*uCO2

# equivalent power
P = dG*F


# In[95]:

print "F = %5.3e mol/year" % (F*year)
print "dG = %5.3f kJ/mol" % (dG/1e3)
print "P = %5.3f TW" % (P/1e12)


# Krissansen-Totton et al. (2015) show that Mars' atmosphere possesses a disequilibrium of 136 J/mol.    
# To maintain it, we show that a power of 2.3 TW is required.
# 
# Solar flux on Mars is about 590 W/m2. So the average integrated can be computed as follows:

# In[123]:

S0 = 588 # W/m2
d0 = 227936637000. # m

urange = np.linspace(0, np.pi/2, 100)
du = urange[1]-urange[0]
I = 0

for u in urange:
    b = u + RM*np.sin(u)/(d0-r*np.cos(u))
    I += 2*np.pi*r*np.sin(u)*S0*np.cos(b)*du
    
print "I = %5.3f TW" % (I/1e12)
