import json

movements_file="/Users/tobiestyles/Documents/WODPredict/Working_Directory/parsers/crossfit_movements.json"

with open(movements_file, "r") as file:
    movements_data = json.load(file)
# print(movements_data)

# Initialize lists
all_movements = []
weighted_movements = []

# Identify weightlifting categories (these are likely weighted)
weighted_categories = {"Weightlifting Movements", "Odd Object Movements"}

# Extract movements
for category, movements_dict in movements_data.items():
    for movement, synonyms in movements_dict.items():
        all_movements.append(movement)
        # Add to weighted_movements if in weighted categories
        if category in weighted_categories:
            weighted_movements.append(movement)

# Sort movements alphabetically
all_movements = sorted(set(all_movements))  # Remove duplicates and sort
weighted_movements = sorted(set(weighted_movements))

# Results
print("All Movements:", all_movements)
print("Weighted Movements:", weighted_movements)

# # Save to JSON if needed
# output_data = {
#     "movements": all_movements,
#     "weighted_movements": weighted_movements
# }

# with open("movement_database_for_app.json", "w") as file:
#     json.dump(output_data, file, indent=4)