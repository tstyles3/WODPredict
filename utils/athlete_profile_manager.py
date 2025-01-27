import json
import os

class AthleteProfileManager:
    def __init__(self, file_name="/Users/tobiestyles/Documents/WODPredict/Working_Directory/data/athlete_profiles.json"):
        """
        Initialize the AthleteProfileManager with a JSON file.
        :param file_name: str, the name of the JSON file to store athlete profiles.
        """
        self.file_name = file_name
        self.profiles = self._load_profiles()

    def _load_profiles(self):
        """
        Load athlete profiles from the JSON file.
        :return: dict, profiles of athletes.
        """
        if os.path.exists(self.file_name) and os.path.getsize(self.file_name) > 0:
            try:
                with open(self.file_name, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print(f"Warning: {self.file_name} contains invalid JSON. Starting with an empty database.")
        return {}

    def _save_profiles(self):
        """
        Save the athlete profiles to the JSON file.
        """
        with open(self.file_name, "w") as file:
            json.dump(self.profiles, file, indent=4)

    def create_profile(self, athlete_id, name, age, gender, skill_level, height):
        """
        Create a new athlete profile.
        :param athlete_id: str, unique identifier for the athlete.
        :param name: str, athlete's name.
        :param age: int, athlete's age.
        :param gender: str, athlete's gender.
        :param skill_level: str, athlete's skill level (e.g., Beginner, Intermediate, Advanced).
        :param height: int, athlete's height in inches.
        """
        if athlete_id in self.profiles:
            print(f"A profile with ID '{athlete_id}' already exists.")
            return

        self.profiles[athlete_id] = {
            "name": name,
            "age": age,
            "gender": gender,
            "skill_level": skill_level,
            "height": height
        }
        self._save_profiles()
        print(f"Profile for {name} created successfully.")

    def view_profiles(self):
        """
        Display all athlete profiles.
        """
        if not self.profiles:
            print("No athlete profiles found.")
            return

        for athlete_id, details in self.profiles.items():
            print(f"ID: {athlete_id}")
            for key, value in details.items():
                print(f"  {key.capitalize()}: {value}")
            print()

    def update_profile(self, athlete_id, **kwargs):
        """
        Update an existing athlete profile.
        :param athlete_id: str, unique identifier for the athlete.
        :param kwargs: key-value pairs of fields to update.
        """
        if athlete_id not in self.profiles:
            print(f"No profile found with ID '{athlete_id}'.")
            return

        for key, value in kwargs.items():
            if key in self.profiles[athlete_id]:
                self.profiles[athlete_id][key] = value

        self._save_profiles()
        print(f"Profile for ID '{athlete_id}' updated successfully.")

    def delete_profile(self, athlete_id):
        """
        Delete an athlete profile.
        :param athlete_id: str, unique identifier for the athlete.
        """
        if athlete_id not in self.profiles:
            print(f"No profile found with ID '{athlete_id}'.")
            return

        del self.profiles[athlete_id]
        self._save_profiles()
        print(f"Profile for ID '{athlete_id}' deleted successfully.")

# Script Usage
if __name__ == "__main__":
    manager = AthleteProfileManager()

    while True:
        print("\nAthlete Profile Manager")
        print("1. Create Profile")
        print("2. View Profiles")
        print("3. Update Profile")
        print("4. Delete Profile")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            athlete_id = input("Enter athlete ID: ").strip()
            name = input("Enter athlete name: ").strip()
            age = int(input("Enter athlete age: ").strip())
            gender = input("Enter athlete gender: ").strip()
            skill_level = input("Enter athlete skill level (Beginner, Intermediate, Advanced): ").strip()
            height = input("Enter athlete height (inches): ").strip()
            manager.create_profile(athlete_id, name, age, gender, skill_level, height)
        elif choice == "2":
            manager.view_profiles()
        elif choice == "3":
            athlete_id = input("Enter athlete ID to update: ").strip()
            print("Enter the fields to update (leave blank to skip):")
            name = input("Name: ").strip()
            age = input("Age: ").strip()
            gender = input("Gender: ").strip()
            skill_level = input("Skill Level: ").strip()
            height = input("Height: ").strip()

            updates = {}
            if name:
                updates["name"] = name
            if age:
                updates["age"] = int(age)
            if gender:
                updates["gender"] = gender
            if skill_level:
                updates["skill_level"] = skill_level
            if height:
                updates["height"] = height

            manager.update_profile(athlete_id, **updates)
        elif choice == "4":
            athlete_id = input("Enter athlete ID to delete: ").strip()
            manager.delete_profile(athlete_id)
        elif choice == "5":
            print("Exiting Athlete Profile Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
