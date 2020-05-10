"""
Parameters and variables used by NEAT

You can modify the variables that have a default value if you want to mess around

Created by Shinrod at 08/05/2020
"""
# ------------------------------------------------ Node ----------------------------------------------------------------
# Kind
SENSOR = 0
HIDDEN = 1
OUTPUT = 2

# --------------------------------------------- Connection -------------------------------------------------------------
# Weight bounds
WEIGHT_UPPER_BOUND = 1      # Default : 1
WEIGHT_LOWER_BOUND = -1     # Default : -1

# Mutation
MUTATION_NEW_WEIGHT = 0.1       # Default : 0.1

# Slight weight mutation
"""
68 % of slight mutations will move the weight by less than {multiplier} of the weight range divided by 2

By default it means that 68 % of slight mutation will be +/- 0.15 * 2 / 2 = +/- 0.15
"""
SLIGHT_WEIGHT_MUTATION_STD_VAR_MULTIPLIER = 0.15   # Default : 0.15

"""
Take the full range : WEIGHT_UPPER_BOUND - WEIGHT_LOWER_BOUND
Divide it by 2 to get only 1 side of the normal distribution
Multiply it by the multiplier

And you get the std_var
"""
SLIGHT_WEIGHT_MUTATION_STD_VAR = (WEIGHT_UPPER_BOUND - WEIGHT_LOWER_BOUND) / 2 * SLIGHT_WEIGHT_MUTATION_STD_VAR_MULTIPLIER

# ----------------------------------------------- Genome ---------------------------------------------------------------
# Drawing : Colors
"""
Colors are in HSV where each value is between 0 and 1
"""
node_color = {SENSOR : '0.166 1 0.5',   # Default : '0.166 1 0.5'   (Yellow)
              HIDDEN : '0.660 1 0.5',   # Default : '0.660 1 0.5'   (Blue)
              OUTPUT : '0.528 1 0.5'}   # Default : '0.528 1 0.5'   (Cyan)

# Drawing : Rank
node_rank = {SENSOR : 'min',
             HIDDEN : None,
             OUTPUT : 'max'}

# Mutation
"""
Mutation chances are between 0 and 1
"""
MUTATION_CHANGE_ALL_WEIGHT = 0.80           # Default : 0.80
MUTATION_CHANCE_ADD_CONNECTION = 0.05       # Default : 0.05
MUTATION_CHANCE_ADD_NODE = 0                # Default : ?

