#
# This is a work in progress - I'd like to support more units
# but for now it should already be useful. If you have a figure
# "12.2e10 g C / year", and you'd like to convert it to mol/year, just do
#
# g_X_to_mol(12.2e10, "C")
#
# It works with molecules as well
#
# g_X_to_mol(3.4e4, "H2O")
#
#
# This requires a package called periodictable
# install it from https://pypi.python.org/pypi/periodictable
#
#
from periodictable import formula

#N_A = 6.0221412927e23

def g_X_to_mol(mass_in_g_X, species_X):
	g_per_mol = formula(species_X).mass
	return mass_in_g_X/g_per_mol


