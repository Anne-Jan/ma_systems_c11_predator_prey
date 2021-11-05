# Main variables
num_runs = 5                           # Number of runs the program will do in an experiment (to average results)

# Board variables
board_vars = {
'board_size': 100,                      # Size of board
'num_hunters': 20,                      # Starting number of hunters
'num_prey': 100,                        # Starting number of prey
'max_iterations': 5000                  # Maximal number of iterations before ending simulation
}

# Hunter variables
hunter_vars = {
'hunter_vision_range': 10,              # Detect prey within this range
'hunter_communication_range': 0,       # Communicate with hunters within this range (0 = no commmunication)
'hunter_stalking_range': 8,             # Range at which hunters stalk prey if other hunters are coming to help
'hunter_hunger_threshold': 50,          # While above this threshold, hunters do not hunt and have chance to reproduce
'hunter_energy_consumption': 0.75,         # Amount of energy consumed when moving
'hunter_energy_reduc': 0.05,            # Lower rate of energy consumption when waiting for helping hunters (gets multiplied by basic energy consumption)
'hunter_reproduce_rate': 0.01,           # Chance of hunter reproducing (when not hunting) (number between 0 and 1)
'hunter_max_age': 400,                  # Age at which hunters die
'hunter_born_max_age': 400,             # Hunters at start of simulation spawn with age between 0 and 'prey_born_max_age'
'hunter_coop_energy': 90                # Number to which satedness is set after succesful cooperative hunt (between 100 and 0)
}

# Prey variables
prey_vars = {
'prey_vision_range': 5,                 # Detect and flee from hunters within this range
'prey_reproduce_rate': 0.004,            # Chance of prey reproducing (when they see no hunters) (number between 0 and 1)
'prey_move_handicap': 0.1,             # Chance of prey skipping move to give hunter small advantage(number between 0 and 1)
'prey_max_age': 325,                    # Age at which prey die
'prey_born_max_age': 325                 # Prey at start of simulation spawn with age between 0 and 'prey_born_max_age'
}
