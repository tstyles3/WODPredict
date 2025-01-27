from parsers.workout_parser import WorkoutParser

def test_parser():
    parser = WorkoutParser()
    workout_text = """
Annie plus
(Time)
50-40-30-20-10
Double unders
25-20-15-10-5
Burpees
Into,
50-40-30-20-10
Sit-ups
25-20-15-10-5
Push jerk(155/105)
    """
    parsed_data = parser.parse(workout_text)
    # print(parsed_data)

    total_reps = parser._calculate_total_reps(parsed_data)
    print("Total Reps by Category:", total_reps)

    # logger = parser.store_total_reps_in_database(total_reps)

# Ensure the function runs when the script is executed
if __name__ == "__main__":
    test_parser()
