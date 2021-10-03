# Main variables
num_runs = 50                           # Number of runs on which to base results

# Board variables
board_vars = {
'board_size': 100,                      # Size of board
'num_hunters': 10,                      # Starting number of hunters
'num_prey': 100,                        # Starting number of prey
'max_iterations': 1000                  # Maximal number of iterations before ending simulation
}

# Hunter variables
hunter_vars = {
'hunter_vision_range': 20,              # Detect prey within this range
'hunter_communication_range': 40,       # Communicate with hunters within this range
'hunter_stalking_range': 8,             # Range at which hunters stalk prey if other hunters are coming to help
'hunter_hunger_threshold': 80,          # While above this threshold, hunters do not hunt and have chance to reproduce
'hunter_energy_consumption': 3,         # Amount of energy consumed when moving
'hunter_energy_reduc': 0.25,            # Lower rate of energy consumption when waiting for helping hunters (gets multiplied by basic energy consumption)
'hunter_reproduce_rate': 0.1            # Chance of hunter reproducing (when not hunting) (number between 0 and 1)
}

# Prey variables
prey_vars = {
'prey_vision_range': 5,                 # Detect and flee from hunters within this range
'prey_reproduce_rate': 0.0025,          # Chance of prey reproducing (when they see no hunters) (number between 0 and 1)
'prey_move_handicap': 0.15              # Chance of prey skipping move to give hunter small advantage(number between 0 and 1)
}