import json
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle

# Load movements
def load_movements(file_path="/Users/tobiestyles/Documents/WODPredict/Working_Directory/parsers/crossfit_movements.json"):
    with open(file_path, "r") as file:
        return json.load(file)

# Load athlete database
def load_athlete_database(file_path="/Users/tobiestyles/Documents/WODPredict/Working_Directory/data/athlete_database.json"):
    with open(file_path, "r") as file:
        return json.load(file)

# Flatten the movements dictionary to get all canonical movements
def get_all_movements(movements_data):
    all_movements = []
    for movement_type, movements in movements_data.items():
        for movement in movements.keys():
            all_movements.append(movement.lower())
    return all_movements

# Prepare data for a specific athlete
def prepare_data_for_athlete(athlete_data, all_movements):
    X, y = [], []
    for workout in athlete_data:
        features = []
        
        # Initialize movement features with 0
        movement_features = {movement: 0 for movement in all_movements}
        # movement_features = movement_features.lower()
        
        # Populate movement features with actual data
        total_reps = workout.get("total_reps", {})
        # print(total_reps)
        weights = workout.get("weights", {})
        weighted_workload = 0
        
        for movement, reps in total_reps.items():
            if movement in movement_features:
                movement_features[movement] = reps
            if movement in weights:
                weighted_workload += np.log(reps * weights[movement])
        
        # Add movement features and weighted workload
        features.extend(movement_features.values())
        features.append(weighted_workload)
        
        # Append result as the target variable
        X.append(features)
        y.append(workout["result"])

    # Convert to numpy arrays
    X = np.array(X)
    y = np.array(y)

    # Apply natural logarithm to the "running" feature
    running_index = list(all_movements).index("running")  # Find index of "running" in all_movements
    for row in X:
        if row[running_index] > 0:  # Avoid log(0) or negative values
            row[running_index] = np.log(row[running_index])
        else:
            row[running_index] = 0  # Assign 0 if "running" is not present

    # Apply natural logarithm to the "rowing" feature
    rowing_index = list(all_movements).index("rowing")  # Find index of "running" in all_movements
    for row in X:
        if row[rowing_index] > 0:  # Avoid log(0) or negative values
            row[rowing_index] = np.log(row[rowing_index])
        else:
            row[rowing_index] = 0  # Assign 0 if "running" is not present

    # Apply natural logarithm to the "rest" feature
    rest_index = list(all_movements).index("rest")  # Find index of "running" in all_movements
    for row in X:
        if row[rest_index] > 0:  # Avoid log(0) or negative values
            row[rest_index] = np.log(row[rest_index])
        else:
            row[rest_index] = 0  # Assign 0 if "running" is not present
    
    # Normalize the features
    scaler = StandardScaler()
    X_normalized = scaler.fit_transform(X)
    
    return X_normalized, y

# Train a model for a specific athlete
def train_model_for_athlete(athlete_name, athlete_data, all_movements):
    X, y = prepare_data_for_athlete(athlete_data, all_movements)
    
    # Split into train and test sets
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train = X[:-1]
    y_train = y[:-1]
    X_test = X[-1]
    # print(X_train)
    # print(y_train)
    # print(X_test)
    
    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predict and evaluate
    y_pred = model.predict(X_test.reshape(-1, len(all_movements) + 1))  # Reshape for consistency
    # score = model.score(X_test.reshape(-1, len(all_movements) + 1), y_pred)
    # print(f"Model for {athlete_name} trained. Test R^2 Score: {score:.2f}")

    return y_pred

# Main function to train models for all athletes
def main():
    movements_data = load_movements()
    all_movements = get_all_movements(movements_data)
    athlete_db = load_athlete_database()
    athlete_models = {}
    
    
    
    for athlete_name, athlete_data in athlete_db.items():
        a = prepare_data_for_athlete(athlete_data, all_movements)
        # print(a)
        print(f"Training model for {athlete_name}...")
        model = train_model_for_athlete(athlete_name, athlete_data, all_movements)
        # athlete_models[athlete_name] = model
        print(model)
    
    print("All models trained.")
    return athlete_models

# Run the script
if __name__ == "__main__":
    athlete_models = main()

# with open('model.pkl', 'wb') as file:
#     pickle.dump(line, file)
