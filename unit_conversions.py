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
import argparse

parser = argparse.ArgumentParser(description="Enter either g/year or mol/year for conversion.")
parser.add_argument("-g", help="Value in g/year.", type=float)
parser.add_argument("-m", help="Value in mol/year", type=float)
parser.add_argument("-s", help="Species to consider.", required=True)


args = vars(parser.parse_args())

if args["g"]:
    value = args["g"]
    unit = "g/year"
if args["m"]:
    value = args["m"]
    unit = "mol/year"

print "Input: %5.3e %s %s" % (value, unit, args["s"])

#N_A = 6.0221412927e23

def g_X_to_mol(mass_in_g_X, species_X):
	g_per_mol = formula(species_X).mass
	return mass_in_g_X/g_per_mol

def mol_X_to_g(mol_X, species_X):
    g_per_mol = formula(species_X).mass
    return mol_X*g_per_mol

if args["g"]:
    print "Output: %5.3e mol/year %s" % (g_X_to_mol(args["g"], args["s"]), args["s"])

if args["m"]:
    print "Output: %5.3e g/year %s" % (mol_X_to_g(args["m"], args["s"]), args["s"])