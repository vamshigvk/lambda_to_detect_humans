import os
import json
import boto3

s3 = boto3.client('s3')

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
    print('before triggering detect, filename: ', filename)
    try:
        s3.download_file(bucketname, filename, filename)
    except:
        print('image downloading failed from S3')
    os.system("python3 detect.py -source "+ filename )
    print('after triggering detect')