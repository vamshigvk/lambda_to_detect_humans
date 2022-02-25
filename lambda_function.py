import os
import json
import boto3

s3 = boto3.client('s3')

destination_bucketname = 'yolov5.output'

def lambda_handler(event, context):
    if event:
        file_obj = event["Records"][0]
        bucketname = str(file_obj["s3"]["bucket"]["name"])
        filename = str(file_obj["s3"]["object"]["key"])
        
        main(bucketname, filename)
        
        return {
            "statusCode": 200,
            "body": json.dumps("Document processed successfully using yolov5!"),
        }

    return {"statusCode": 500, "body": json.dumps("There is an issue!")}

def main(bucketname,filename):

    print('before downloading file from S3, filename: ', filename)
    s3.download_file(bucketname, filename, 'yolov5/'+filename)
    os.system("python3 yolov5/detect.py --source yolov5/"+ filename )
    s3.upload_file(destination_bucketname, 'yolov5/runs/detect/exp/'+filename, filename)
    print('end of main')