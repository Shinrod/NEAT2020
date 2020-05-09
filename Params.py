"""
Parameters of NEAT

Created by Shinrod at 08/05/2020
"""

# --- Node ---
# Kind
SENSOR = 0
HIDDEN = 1
OUTPUT = 2

# --- Connection ---
# Weight bounds
WEIGHT_UPPER_BOUND = 1
WEIGHT_LOWER_BOUND = -1

# History
history_count = 0

# --- Neural Network ---
# Drawing : graphviz.py stuff
node_color = {SENSOR : '0.166 1 0.5',   # Yellow
              HIDDEN : '0.66 1 0.5',    # Blue
              OUTPUT :'0.528 1 0.5'}    # Cyan
node_rank = {SENSOR : 'min',
             HIDDEN : None,
             OUTPUT : 'max'}
