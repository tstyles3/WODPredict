import re
import json
import os
from datetime import datetime


class WorkoutParser:
    def __init__(self, movements_file="/Users/tobiestyles/Documents/WODPredict/Working_Directory/parsers/crossfit_movements.json"):
        """
        Initialize the WorkoutParser and load known movements and their synonyms from a JSON file.
        :param movements_file: str, path to the JSON file containing movements.
        """
        self.synonym_map = self._load_movements(movements_file)

    def _load_movements(self, movements_file):
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

        return synonym_map

    def parse(self, text):
        """
        Main function to parse a workout description.
        :param text: str, raw workout text.
        :return: dict, structured workout data.
        """
        cleaned_text = self._preprocess(text)
        movements = self._extract_movements(cleaned_text)
        rep_scheme = self._extract_rep_scheme(cleaned_text)
        weights = self._extract_weights(cleaned_text)
        time_cap = self._extract_time_cap(cleaned_text)
        extras = self._extract_extras(cleaned_text)

        return {
            "movements": movements,
            "rep_scheme": rep_scheme,
            "weights": weights,
            "time_cap": time_cap,
            "extras": extras,
        }

    def _preprocess(self, text):
        """
        Cleans and normalizes the input text.
        :param text: str
        :return: str
        """
        return text.strip().lower()

    def _extract_movements(self, text):
        """
        Extracts movements from the text using the synonym map, prioritizing exact matches.
        Falls back to partial matches if no exact matches are found for a line.
        :param text: str
        :return: list of canonical movements in order of appearance.
        """
        movements = []  # List to preserve order
        sorted_synonyms = sorted(self.synonym_map.items(), key=lambda x: len(x[0]), reverse=True)  # Match longer synonyms first
        lines = text.splitlines()  # Split the text into lines

        for line in lines[1:]:  # Skip the first line
            line_lower = line.lower()  # Normalize to lowercase for case-insensitive matching
            exact_matched = False  # Flag to track exact match in the current line

            # Check for exact matches first
            for synonym, canonical in sorted_synonyms:
                # Match exact phrases using word boundaries
                pattern = rf"\b{re.escape(synonym)}\b"
                if re.search(pattern, line_lower):
                    if canonical not in movements:  # Avoid duplicates
                        movements.append(canonical)
                    line_lower = re.sub(pattern, " " * len(synonym), line_lower)  # Remove exact match
                    exact_matched = True  # Mark as an exact match
                    break  # Skip to the next line after finding an exact match

            # If no exact match, allow partial matches
            if not exact_matched:
                for synonym, canonical in sorted_synonyms:
                    if synonym in line_lower:
                        if canonical not in movements:  # Avoid duplicates
                            movements.append(canonical)
                        line_lower = line_lower.replace(synonym, " " * len(synonym))  # Remove partial match
                        break  # Move to the next line after finding a partial match

        return movements
    
    def _extract_rep_scheme(self, text):
        """
        Extracts rep schemes, including ladders (e.g., '21-18-15-12-9'), 
        rounds formats (e.g., '5 RFT'), and movement-specific reps.
        :param text: str
        :return: dict with "global_scheme" and "movement_reps".
        """
        global_scheme = []
        movement_reps = []

        global_scheme_patterns = [
            r"(\d+(-\d+)+)",          # Patterns like '21-18-15'
            r"(\d+\s?RFT)",           # Patterns like '5 RFT'
            r"(AMRAP\s?\d+\s?(min|minutes)?)",  # Patterns like 'AMRAP 15 min'
            r"(EMOM\s?\d+\s?(min|minutes)?)"   # Patterns like 'EMOM 20 min'
        ]

        # Track ladder and associated movements
        current_ladder_reps = 0
        is_ladder_active = False
        active_movements = []

        for line in text.splitlines():
            line_lower = line.strip().lower()
            exact_matched = False  # Track if an exact match occurred

            # Check for global scheme patterns
            for pattern in global_scheme_patterns:
                match = re.search(pattern, line_lower, re.IGNORECASE)
                if match:
                    global_scheme.append(match.group(1))

            # Detect ladders and calculate total reps
            ladder_match = re.match(r"(\d+(-\d+)+)", line_lower)
            if ladder_match:
                ladder = list(map(int, ladder_match.group(1).split('-')))
                current_ladder_reps = sum(ladder)
                is_ladder_active = True
                active_movements = []  # Track movements processed for this ladder
                continue

            # Detect movements and assign ladder reps if active
            if is_ladder_active:
                # Check for exact matches first
                sorted_synonyms = sorted(self.synonym_map.items(), key=lambda x: len(x[0]), reverse=True)  # Longest synonyms first
                for synonym, canonical in sorted_synonyms:
                    # Match exact phrases using word boundaries
                    pattern = rf"\b{re.escape(synonym)}\b"
                    if re.search(pattern, line_lower):
                        if canonical not in active_movements:  # Avoid duplicates
                            movement_reps.append((canonical, current_ladder_reps))
                            active_movements.append(canonical)
                        line_lower = re.sub(pattern, " " * len(synonym), line_lower)  # Remove exact match
                        exact_matched = True  # Mark as an exact match
                        break  # Skip to the next synonym after finding an exact match

                # If no exact match, allow partial matches
                if not exact_matched:
                    for synonym, canonical in sorted_synonyms:
                        if synonym in line_lower:
                            if canonical not in active_movements:  # Avoid duplicates
                                movement_reps.append((canonical, current_ladder_reps))
                                active_movements.append(canonical)
                            line_lower = line_lower.replace(synonym, " " * len(synonym))  # Remove partial match
                            break  # Move to the next line after finding a partial match

                # Reset ladder status if movements are processed
                # if active_movements:
                #     is_ladder_active = False
                #     current_ladder_reps = 0
                #     active_movements = []

            # Detect explicit movement-specific reps
            explicit_rep_match = re.match(r"(\d+)\s+(.+)", line)
            if explicit_rep_match:
                reps = int(explicit_rep_match.group(1))
                description = explicit_rep_match.group(2).strip().lower()
                movement_reps.append((description, reps))

        return {
            "global_scheme": global_scheme,
            "movement_reps": movement_reps
        }


    def _extract_weights(self, text):
        """
        Extracts weights (e.g., '(115/85)', '135 lbs'), excluding specific values like '24/20' and '30/24'.
        :param text: str
        :return: list of weights.
        """
        # Match weights using regex
        weights = re.findall(r"\((\d+/\d+|\d+\s?(lbs|kg))\)", text)

        # Exclude specific weights
        excluded_weights = {"24/20", "30/24"}
        filtered_weights = [weight for weight in weights if weight[0] not in excluded_weights]

        # Return the filtered list of weights
        return [weight[0] for weight in filtered_weights]

    def _extract_time_cap(self, text):
        """
        Extracts the time cap (e.g., '15 min time cap').
        :param text: str
        :return: str or None.
        """
        match = re.search(r"(\d+\s?(min|minute|second)\s?time cap)", text)
        return match.group(1) if match else None

    def _extract_extras(self, text):
        """
        Extracts additional instructions (e.g., '30 double unders between sets').
        :param text: str
        :return: list of extras.
        """
        return re.findall(r"\*\s?(\d+)\s?(.*?)\s?between\s?sets", text)

    def _calculate_total_reps(self, parsed_data):
        """
        Calculate the total reps for each movement, including scenarios like ladders and RFT.
        :param parsed_data: dict, output of the `parse` method.
        :return: dict mapping movements to total reps.
        """
        total_reps = {movement: 0 for movement in self.synonym_map.keys()}  # Initialize all movements with 0 reps
        movement_reps = parsed_data["rep_scheme"]["movement_reps"]
        global_scheme = parsed_data["rep_scheme"]["global_scheme"] 

        # Detect rounds in the global scheme (e.g., '5 RFT')
        rounds_multiplier = 1
        for scheme in global_scheme:
            match = re.match(r"(\d+)\s*(rft|rounds)", scheme, re.IGNORECASE)
            if match:
                rounds_multiplier = int(match.group(1))
                break

        # Process movement-specific reps
        sorted_synonyms = sorted(self.synonym_map.items(), key=lambda x: len(x[0]), reverse=True)  # Longest synonyms first
        for movement_description, reps in movement_reps:
            for synonym, canonical_movement in sorted_synonyms:
            
                pattern = rf"\b{re.escape(synonym)}\b"
                if re.search(pattern, movement_description):
                    total_reps[canonical_movement] += reps * rounds_multiplier
                movement_description = re.sub(pattern, " " * len(synonym), movement_description)  # Remove exact match

        # Filter out movements with 0 reps for clarity
        total_reps = {movement: reps for movement, reps in total_reps.items() if reps > 0}

        return total_reps

    # def store_total_reps_in_database(self, total_reps, database_file="/Users/tobiestyles/Documents/WODPredict/Working_Directory/data/athlete_database.json"):
    #     """
    #     Store the total reps in a database for machine learning model training.
    #     :param total_reps: dict, output of `_calculate_total_reps`.
    #     :param database_file: str, file path to store the database.
    #     """
    #     # Prepare the new entry
    #     new_entry = {
    #         "date": datetime.now().strftime("%Y-%m-%d"),  # Add current date
    #         "totals": total_reps,                         # Include total reps data
    #         "results": int(input("Input your time in seconds: "))
    #     }

    #     # Initialize the database
    #     database = []

    #     # Check if the file exists
    #     if os.path.exists(database_file):
    #         try:
    #             # Open and load the existing database
    #             with open(database_file, "r") as file:
    #                 if os.path.getsize(database_file) > 0:  # Ensure the file is not empty
    #                     database = json.load(file)
    #         except json.JSONDecodeError:
    #             print(f"Warning: {database_file} is corrupted or contains invalid JSON. Initializing a new database.")

    #     # Append the new entry
    #     database.append(new_entry)

    #     # Save the updated database back to the file
    #     with open(database_file, "w") as file:
    #         json.dump(database, file, indent=4)

    #     print(f"Workout totals successfully added to {database_file}.")


