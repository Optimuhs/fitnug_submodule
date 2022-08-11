####################################################################################################################
#################################     PARAMETERS FOR FITNUGS EXTENSION    ##########################################
####################################################################################################################


workout_command_name = "workout"
workout_command_description = "tell us when you exercised to earn points"
workout_leaderboard_command_name = "leaderboard"
workout_leaderboard_command_description = "see who's been doing the most workouts"

activities = ["weightlifting", "running", "hiit shiiiit",
              "biking", "hiking", "climbing & bouldering", "swimming", "sex", "other"]

intensity_multipliers = {"easy": 0.5, "moderate": 1, "hard": 1.5, "deadly": 1.5}
intensity_points = {"easy": 1, "moderate": 2, "hard": 3, "deadly": 4}
intensity_levels = ["easy", "moderate", "hard", "deadly"]

timespan_values = {"day": (24 * 60 * 60),
                   "week": (7 * 24 * 60 * 60),
                   "month": (30 * 24 * 60 * 60),
                   "year": (365 * 24 * 60 * 60),
                   "all": (10 * 365 * 24 * 60 * 60)}
leaderboard_timespans = ["day", "week", "month", "year", "all"]
