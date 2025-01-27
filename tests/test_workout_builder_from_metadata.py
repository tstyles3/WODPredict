from parsers.workout_parser import WorkoutParser
from data.workout_builder_from_metadata import WorkoutBuilderFromMetadata

def test_parser():
    parser = WorkoutParser()
    workout_text = """
Box jump over and hang power Snatch
(Time)
21-18-15-12-9-6-3
Hang power snatch(115/85)
3-6-9-12-15-18-21
Box jump over(24/20)
    """
    parsed_data = parser.parse(workout_text)
    print("Parsed Data:")
    print(parsed_data)
    return parsed_data

def test_builder():
    # Use the output from test_parser as the parsed_metadata
    parsed_metadata = test_parser()

    builder = WorkoutBuilderFromMetadata(parsed_metadata)
    structured_workout = builder.build_workout_representation()

    print("\nStructured Workout Representation:")
    print(structured_workout)

# Ensure the function runs when the script is executed
if __name__ == "__main__":
    test_builder()
