# # // import * as AWS from 'aws-sdk';
# # // import { APIGatewayEvent, Context } from 'aws-lambda';
# # // import * as fs from 'fs';
# # // import * as path from 'path';
# # // import * as util from 'util';
# # // import { exec } from 'child_process';

# # // const s3 = new AWS.S3();
# # // const dynamodb = new AWS.DynamoDB.DocumentClient();
# # // const BUCKET_NAME = 'your-bucket-name';
# # // const MODEL_KEY = 'your-model-file-path/workout_score_model.joblib';
# # // const ENCODER_KEY = 'your-model-file-path/section_type_encoder.joblib';
# # // const WORKOUT_TABLE = 'WorkoutData';
# # // const PREDICTION_TABLE = 'predictWorkoutScore';

# # // // Paths for the downloaded model and encoder
# # // const MODEL_PATH = '/tmp/workout_score_model.joblib';
# # // const ENCODER_PATH = '/tmp/section_type_encoder.joblib';

# # // // Promisify exec for async/await support
# # // const execPromise = util.promisify(exec);

# # // /**
# # //  * Download a file from S3 to Lambda's temporary storage (/tmp/)
# # //  */
# # // async function downloadFromS3(bucket: string, key: string, destPath: string): Promise<void> {
# # //   try {
# # //     const params = { Bucket: bucket, Key: key };
# # //     const data = await s3.getObject(params).promise();
# # //     fs.writeFileSync(destPath, data.Body as Buffer);
# # //   } catch (error) {
# # //     console.error(`Error downloading ${key} from S3:`, error);
# # //     throw new Error(`Failed to download ${key} from S3.`);
# # //   }
# # // }

# # // /**
# # //  * Runs a Python script in a separate process and returns the output.
# # //  */
# # // async function runPythonPrediction(workoutData: string): Promise<number> {
# # //   try {
# # //     const pythonScript = `
# # // import json
# # // import joblib
# # // import numpy as np

# # // # Load model and encoder
# # // model = joblib.load("${MODEL_PATH}")
# # // encoder = joblib.load("${ENCODER_PATH}")

# # // def extract_features(workout_json):
# # //     total_movements = 0
# # //     total_reps = 0
# # //     total_weight = 0
# # //     movement_types = set()

# # //     try:
# # //         sections = json.loads(workout_json)
# # //     except json.JSONDecodeError:
# # //         return np.array([0, 0, 0, 0, encoder.transform(["unknown"])[0]])

# # //     for section in sections:
# # //         for movement in section.get("movements", []):
# # //             total_movements += 1
# # //             movement_types.add(movement.get("movement", "").lower())

# # //             if "reps" in movement:
# # //                 total_reps += int(movement["reps"]) if isinstance(movement["reps"], str) else movement["reps"]

# # //             if "weight" in movement:
# # //                 total_weight += float(movement["weight"]) if isinstance(movement["weight"], str) else movement["weight"]

# # //     section_type = sections[0]["type"] if sections else "unknown"
# # //     section_type_encoded = encoder.transform([section_type])[0]

# # //     return np.array([total_movements, total_reps, total_weight, len(movement_types), section_type_encoded])

# # // # Process input
# # // input_features = extract_features('${workoutData}').reshape(1, -1)

# # // # Predict score
# # // predicted_score = model.predict(input_features)[0]

# # // print(predicted_score)
# # // `;

# # //     const scriptPath = path.join('/tmp', 'predict.py');
# # //     fs.writeFileSync(scriptPath, pythonScript);

# # //     const { stdout } = await execPromise(`python3 ${scriptPath}`);
# # //     return parseFloat(stdout.trim());
# # //   } catch (error) {
# # //     console.error('Error running Python script:', error);
# # //     throw new Error('Python prediction failed.');
# # //   }
# # // }

# # // /**
# # //  * Lambda handler function
# # //  */
# # // export async function handler(event: APIGatewayEvent, context: Context) {
# # //   try {
# # //     // Download the model and encoder from S3 if not already available
# # //     await downloadFromS3(BUCKET_NAME, MODEL_KEY, MODEL_PATH);
# # //     await downloadFromS3(BUCKET_NAME, ENCODER_KEY, ENCODER_PATH);

# # //     // Parse the request body
# # //     const body = event.body ? JSON.parse(event.body) : {};
# # //     const workout = body.workout;
# # //     const actualScore = body.score || '0';

# # //     if (!workout) {
# # //       return { statusCode: 400, body: JSON.stringify({ error: 'No workout data provided' }) };
# # //     }

# # //     // Run prediction
# # //     const predictedScore = await runPythonPrediction(JSON.stringify(workout));

# # //     // Save the prediction to DynamoDB
# # //     const predictionData = {
# # //       id: Math.floor(Math.random() * 1000000).toString(),
# # //       workout: JSON.stringify(workout),
# # //       actualScore: actualScore,
# # //       predictedScore: predictedScore,
# # //     };

# # //     await dynamodb.put({
# # //       TableName: PREDICTION_TABLE,
# # //       Item: predictionData,
# # //     }).promise();

# # //     // Return the predicted score
# # //     return {
# # //       statusCode: 200,
# # //       body: JSON.stringify({ predictedScore, actualScore }),
# # //     };

# # //   } catch (error) {
# # //     console.error('Handler error:', error);
# # //     return { statusCode: 500, body: JSON.stringify({ error: error.message }) };
# # //   }
# # // }


# # import json
# # import boto3
# # import xgboost as xgb
# # import numpy as np
# # import tempfile

# # # S3 settings (update with your actual bucket name and model path)
# # BUCKET_NAME = "your-s3-bucket-name"
# # MODEL_KEY = "xgboost-model.json"

# # s3 = boto3.client("s3")

# # def lambda_handler(event, context):
# #     try:
# #         print("Received event:", json.dumps(event))

# #         # Parse the workout data
# #         workout_data = json.loads(event["body"])
# #         features = np.array([workout_data["features"]])  # Ensure data shape matches model input

# #         # Download the model from S3
# #         with tempfile.NamedTemporaryFile(delete=True) as temp_model:
# #             s3.download_file(BUCKET_NAME, MODEL_KEY, temp_model.name)
# #             model = xgb.Booster()
# #             model.load_model(temp_model.name)

# #         # Convert workout data to DMatrix for prediction
# #         dmatrix = xgb.DMatrix(features)
# #         prediction = model.predict(dmatrix)

# #         return {
# #             "statusCode": 200,
# #             "body": json.dumps({"prediction": prediction.tolist()}),
# #         }
# #     except Exception as e:
# #         print(f"Error: {e}")
# #         return {
# #             "statusCode": 500,
# #             "body": json.dumps({"error": str(e)}),
# #         }

# # import type { Schema } from "../../data/resource"
# # import json

# # def lambda_handler(event, context):
# #     # Simulate prediction logic for now
# #     prediction_message = "Your predicted score is 200 reps"

# #     return {
# #         "statusCode": 200,
# #         "body": json.dumps({
# #             "prediction": prediction_message
# #         }),
# #     }


# # lambda_function.py
# import json
# import logging

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# def lambda_handler(event, context):
#     """
#     Lambda function to predict workout score based on workout data
#     """
#     logger.info(f"Received event: {json.dumps(event)}")
    
#     # Use provided workout data or fallback to hardcoded data for testing
#     workout_data = event.get('workoutData') if 'workoutData' in event else get_hardcoded_workout_data()
    
#     # Process the workout data and predict score
#     predicted_score = predict_workout_score(workout_data)
    
#     # Return the response
#     response = {
#         'statusCode': 200,
#         'body': {
#             'message': 'Workout score prediction successful',
#             'workoutData': workout_data,
#             'predictedScore': predicted_score
#         }
#     }
    
#     logger.info(f"Response: {json.dumps(response)}")
#     return response

# def get_hardcoded_workout_data():
#     """
#     Function to get hardcoded workout data for testing
#     """
#     return {
#         'userId': 'user123',
#         'workoutType': 'strength',
#         'exercises': [
#             {
#                 'name': 'Bench Press',
#                 'sets': 3,
#                 'reps': 10,
#                 'weight': 135
#             },
#             {
#                 'name': 'Squat',
#                 'sets': 4,
#                 'reps': 8,
#                 'weight': 185
#             },
#             {
#                 'name': 'Deadlift',
#                 'sets': 3,
#                 'reps': 5,
#                 'weight': 225
#             }
#         ],
#         'duration': 45,  # minutes
#         'intensity': 'high',
#         'caloriesBurned': 320
#     }

# def predict_workout_score(workout_data):
#     """
#     Simple placeholder function to predict workout score
#     In a real scenario, this would contain your ML model logic
#     """
#     # This is a very simplified placeholder calculation
#     # In reality, you would use your ML model here
    
#     base_score = 0
    
#     # Add points based on workout duration
#     base_score += workout_data['duration'] * 0.5
    
#     # Add points based on intensity
#     if workout_data['intensity'] == 'high':
#         base_score += 50
#     elif workout_data['intensity'] == 'medium':
#         base_score += 30
#     else:
#         base_score += 15
    
#     # Add points based on calories burned
#     base_score += workout_data['caloriesBurned'] * 0.1
    
#     # Add points based on exercises
#     for exercise in workout_data['exercises']:
#         volume_score = exercise['sets'] * exercise['reps'] * exercise['weight'] * 0.01
#         base_score += volume_score
    
#     # Round to 2 decimal places
#     return round(base_score * 100) / 100