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
    
    print('start of main')

    try:
        print('before downloading file from S3, filename: ', filename)
        s3.download_file(bucketname, filename, filename)
        print('After downloading file from S3 ')
    except:
        print('image downloading failed from S3')


    try:
        print('before triggering detect')
        os.system("python3 detect.py --source "+filename )
        print('after triggering detect')
    except:
        print('exception while running detect')


    try:
        print('before saving output file to S3 ')
        s3.download_file(destination_bucketname, 'runs/detect/exp/'+filename, filename)
        print('after saving output file to S3')

    except:
        print('image downloading failed from S3')

    print('end of main')