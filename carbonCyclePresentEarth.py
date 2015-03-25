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

# Carbon sources = 28 Tmol/yr
D_M = 4.3       # degassing (3.1-5.5 Tmol/yr)
W_C = 11.7      # weathering (10-16 Tmol/yr)
D_C = 2.5       # degassing (2.0-4.0 Tmol/yr)
D_POC = 0.5     # degassing (0.4-0.6 Tmol/yr)
W_POC = 9.0     # weathering (8-16 Tmol/yr)

# Carbon sinks = 28 Tmol/yr
B_BC = 16.0     # burial (14-17 Tmol/yr)
A_OC = 2.0      # alteration (1.5-2.4 Tmol/yr)
B_CH4 = 0.0     # burial -- included in B_POC
B_AC = 0.0      # burial -- included in B_POC
B_POC = 10.0    # burial (5.4-27 Tmol/yr) -- includes B_AC and B_CH4