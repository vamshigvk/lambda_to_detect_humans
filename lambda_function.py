import os
import json
import boto3

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')


destination_bucketname = 'yolov5.output'

def lambda_handler(event, context):
    
    print("Event :", event)
    source_bucket_name = event['Records'][0]['s3']['bucket']['name']
    print("Source bucket name is: ", source_bucket_name, "only")

    file_key_name = event['Records'][0]['s3']['object']['key']
    print('File key name is: ', file_key_name, "only")
    
    bucket = s3_resource.Bucket(source_bucket_name)
    path, filename = os.path.split(file_key_name)
    print('Key we are downloading is: ',filename)
    
    print('before downloading file from S3, filename: at /tmp/', filename)
    bucket.download_file(file_key_name, "/tmp/" + filename)

    print('inside this directory: ',os.getcwd())
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    print('contents in current directory:', files)

    print('before calling detect python file')
    os.system("python3 detect.py --source /tmp/"+ filename )

    print('before uploading output file to destination S3 bucket')
    s3.upload_file('runs/detect/exp/'+filename, destination_bucketname, 'output_'+filename)
    print('end of main') 

    return {
        "statusCode": 200,
        "body": json.dumps("Document processed successfully using yolov5!"),
    }

