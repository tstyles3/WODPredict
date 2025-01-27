import boto3
import json

bucket_name = "wodpredict-data-storage"
file_name = "crossfit_movements.json"

s3_client = boto3.client("s3")

response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
file_content = response["Body"].read().decode("utf-8")
movements_data = json.loads(file_content)
print(movements_data)
