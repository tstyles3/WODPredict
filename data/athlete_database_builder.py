import json
import os
from datetime import datetime
from parsers.workout_parser import WorkoutParser


class AthleteDatabase:
    def __init__(self, profiles_file="/Users/tobiestyles/Documents/WODPredict/Working_Directory/data/athlete_profiles.json", database_file="/Users/tobiestyles/Documents/WODPredict/Working_Directory/data/athlete_database.json"):
        """
        Initialize the AthleteDatabase with athlete profiles and a workout database.
        :param profiles_file: str, the JSON file containing athlete profiles.
        :param database_file: str, the JSON file to store workout data.
        """
        self.profiles_file = profiles_file
        self.database_file = database_file
        self.profiles = self._load_profiles()
        self.database = self._load_database()

    def _load_profiles(self):
        """
        Load athlete profiles from the profiles JSON file.
        :return: dict, the profiles of athletes.
        """
        if os.path.exists(self.profiles_file) and os.path.getsize(self.profiles_file) > 0:
            with open(self.profiles_file, "r") as file:
                return json.load(file)
        raise FileNotFoundError(f"Athlete profiles file '{self.profiles_file}' not found!")

    def _load_database(self):
        """
        Load the athlete workout database from the JSON file.
        :return: dict, the database as a dictionary.
        """
        if os.path.exists(self.database_file) and os.path.getsize(self.database_file) > 0:
            try:
                with open(self.database_file, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print(f"Warning: {self.database_file} contains invalid JSON. Starting with an empty database.")
        return {}

    def _save_database(self):
        """
        Save the athlete workout database to the JSON file.
        """
        with open(self.database_file, "w") as file:
            json.dump(self.database, file, indent=4)

    def add_workout_for_athlete(self, athlete_name, workout_date, workout_type, total_reps, additional_features=None, result=None):
        """
        Add a workout result for an athlete. Uses profiles to verify athlete existence.
        :param athlete_name: str, name of the athlete.
        :param workout_date: str, date of the workout (format: YYYY-MM-DD).
        :param workout_type: str, type of the workout (e.g., AMRAP, RFT).
        :param total_reps: dict, total reps for each movement.
        :param additional_features: dict, other features (e.g., weights, rounds, etc.).
        :param result: int, total time to complete the workout.
        """
        # Ensure athlete exists in profiles
        if athlete_name not in self.profiles:
            print(f"Error: Athlete '{athlete_name}' does not exist in profiles!")
            return

        # Ensure additional features is a dict
        if additional_features is None:
            additional_features = {}

        # Initialize athlete's workout data if not already in the database
        if athlete_name not in self.database:
            self.database[athlete_name] = []

        # Create the workout record
        workout_record = {
            "date": workout_date,
            "type": workout_type,
            "total_reps": total_reps,
            **additional_features,
            "result": result
        }

        # Add the workout record
        self.database[athlete_name].append(workout_record)
        self._save_database()
        print(f"Workout for {athlete_name} on {workout_date} added successfully.")

    def view_athlete_workouts(self, athlete_name):
        """
        Display all workout records for a specific athlete.
        :param athlete_name: str, name of the athlete.
        """
        if athlete_name not in self.database:
            print(f"No records found for athlete: {athlete_name}")
            return

        print(f"Workout records for {athlete_name}:")
        for record in self.database[athlete_name]:
            print(f"Date: {record['date']}")
            print(f"Type: {record['type']}")
            print("Total Reps:")
            for movement, reps in record["total_reps"].items():
                print(f"  {movement}: {reps}")
            for key, value in record.items():
                if key not in ["date", "type", "total_reps"]:
                    print(f"{key.capitalize()}: {value}")
            print("-" * 40)

    def view_all_athletes(self):
        """
        Display a list of all athletes with their workout records.
        """
        print("Athlete Profiles with Workout Records:")
        for athlete, profile in self.profiles.items():
            print(f"  - {profile['name']} (Skill Level: {profile['skill_level']}, Age: {profile['age']})")
            if athlete in self.database:
                print(f"    Total Workouts Logged: {len(self.database[athlete])}")
            else:
                print("    No workouts logged yet.")

    def _load_movements(self, movements_file="/Users/tobiestyles/Documents/WODPredict/Working_Directory/parsers/crossfit_movements.json"):
        """
        Load known movements from a JSON file into a synonym map.
        :param movements_file: str, path to the JSON file.
        :return: dict mapping synonyms to canonical movement names.
        """
        if not os.path.exists(movements_file):
            raise FileNotFoundError(f"Movements file '{movements_file}' not found.")

        with open(movements_file, "r") as file:
            movements_data = json.load(file)

        synonym_map = {}
        for category, movements in movements_data.items():
            for movement, synonyms in movements.items():
                synonym_map[movement.lower()] = movement.lower()
                for synonym in synonyms:
                    synonym_map[synonym.lower()] = movement.lower()

        return movements_data


# Example Usage
if __name__ == "__main__":
    # Initialize the athlete database
    db = AthleteDatabase()
    movements_data = db._load_movements()
    movement_types = list(movements_data.keys())
    weightlifting = movement_types[0]
    all_movements = []
    for movement_type, movements in movements_data.items():
        for movement in movements.keys():
            all_movements.append(movement.lower())
    weightlifting_movements = list(movements_data[weightlifting].keys())
    # Convert weightlifting movements to lowercase for case-insensitive matching
    weightlifting_movements_lower = [movement.lower() for movement in weightlifting_movements]
    # print("synonym map: ", all_movements)

    # Example of total reps from the calculate_total_reps function
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
    # total_reps = {'snatch': 45, 'burpees': 45, 'running': 1200}
    print("Total Reps by Category:", total_reps)
    # example_total_reps = {
    #     "push-ups": 100,
    #     "kb swing": 50,
    #     "double unders": 120
    # }

    # Initialize the dictionary
    additional_features = {"weights": {}}

    # Loop through total_reps and add weights for matching movements
    for movement in total_reps.keys():
        if movement.lower() in weightlifting_movements_lower:
            print(f"Adding weight for movement: {movement}")
            weight = input(f"Enter weight for {movement}: ")  # Ask for input weight
            additional_features["weights"][movement] = int(weight)

    # Example of additional features
    # example_additional_features = {
    #     "rounds": 5,
    #     "weights": {
    #         "Clean": "135lbs",
    #         "Deadlift": "225lbs"
    #     },
    #     "duration": "20 minutes"
    # }
            
    # result = (int(input('final Minutes: '))*60)+int(input('final Seconds: '))
    result = 0

    # Add a workout record for an athlete
    db.add_workout_for_athlete(
        athlete_name="Tobie",
        workout_date=str(datetime.today().date()),
        # workout_date=('2024-12-17'),
        workout_type="Time",
        total_reps=total_reps,
        additional_features=additional_features,
        result = result
    )

    # View all workouts for a specific athlete
    # db.view_athlete_workouts("Tobie")

    # View all athletes with profiles
    # db.view_all_athletes()
