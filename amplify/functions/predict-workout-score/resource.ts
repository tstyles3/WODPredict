// // amplify/functions/predict-workout-score/resource.ts
// import { defineFunction } from '@aws-amplify/backend';

// export const predictWorkoutScore = defineFunction({
//   name: 'predict-workout-score',
//   entry: './handler.ts'
// });

// import * as path from 'path';
// import { defineFunction } from '@aws-amplify/backend';
// import * as aws_lambda from 'aws-cdk-lib/aws-lambda';
// import * as aws_s3 from 'aws-cdk-lib/aws-s3';
// import * as aws_iam from 'aws-cdk-lib/aws-iam';
// import * as aws_cdk from 'aws-cdk-lib';

// export const predictWorkoutScore = defineFunction((scope) => {
//   return new aws_lambda.Function(scope, 'PredictWorkoutScore', {
//     functionName: 'predict-workout-score',
//     runtime: aws_lambda.Runtime.PYTHON_3_9, // ✅ Python runtime
//     handler: 'handler.lambda_handler', // ✅ Correct function handler
//     code: aws_lambda.Code.fromAsset(path.join(__dirname, './')), // ✅ Package Python code
//     environment: {
//       S3_BUCKET: 'your-s3-bucket-name', // ✅ Allow function to access S3
//     },
//     timeout: aws_cdk.Duration.seconds(30), // ✅ Fix 'aws_cdk' error
//     memorySize: 256, // ✅ Ensure enough memory for ML processing
//     role: new aws_iam.Role(scope, 'LambdaExecutionRole', {
//       assumedBy: new aws_iam.ServicePrincipal('lambda.amazonaws.com'),
//       managedPolicies: [
//         aws_iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
//         aws_iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonS3ReadOnlyAccess'), // ✅ S3 permissions
//       ],
//     }),
//   });
// });

// import { execSync } from "node:child_process";
// import * as path from "node:path";
// import { fileURLToPath } from "node:url";
// import { defineFunction } from "@aws-amplify/backend";
// import { DockerImage, Duration } from "aws-cdk-lib";
// import { Code, Function, Runtime } from "aws-cdk-lib/aws-lambda";

// const functionDir = path.dirname(fileURLToPath(import.meta.url));

// export const predictWorkoutScore = defineFunction(
//   (scope) =>
//     new Function(scope, "predict-score", {
//       handler: "handler.lambda_handler",
//       runtime: Runtime.PYTHON_3_9, // or any other python version
//       timeout: Duration.seconds(20), //  default is 3 seconds
//       code: Code.fromAsset(functionDir, {
//         bundling: {
//           image: DockerImage.fromRegistry("dummy"), // replace with desired image from AWS ECR Public Gallery
//           local: {
//             tryBundle(outputDir: string) {
//               execSync(
//                 `python3 -m pip install -r ${path.join(functionDir, "requirements.txt")} -t ${path.join(outputDir)} --platform manylinux2014_x86_64 --only-binary=:all:`
//               );
//               execSync(`cp -r ${functionDir}/* ${path.join(outputDir)}`);
//               return true;
//             },
//           },
//         },
//       }),
//     }),
//     {
//       resourceGroupName: "auth" // Optional: Groups this function with auth resource
//     }
// );

// import { defineFunction } from '@aws-amplify/backend';

// export const predictWorkoutScore = defineFunction({
//   name: 'predict-workout-score',
//   entry: './handler.py',
// });
