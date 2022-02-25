import os
import json

def lambda_handler(event, context):
    if event:
        file_obj = event["Records"][0]
        bucketname = str(file_obj["s3"]["bucket"]["name"])
        filename = str(file_obj["s3"]["object"]["key"])
        
        main(bucketname, filename)
        
        return {
            "statusCode": 200,
            "body": json.dumps("Document processed successfully!"),
        }

    return {"statusCode": 500, "body": json.dumps("There is an issue!")}

def main(bucketname,filename):
    print('before triggering detect, filename: ', filename)
    os.system("python3 detect.py -source "+ filename )
    print('after triggering detect')