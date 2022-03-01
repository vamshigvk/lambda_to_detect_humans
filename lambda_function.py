import os
import json
import boto3
from decimal import Decimal
import smtplib
from email.message import EmailMessage
from os import environ
from datetime import date

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')


destination_bucketname = os.environ['destination_bucketname']


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
    os.system("python3 detect.py --project /tmp/ --source /tmp/"+ filename )

    print('before uploading output file to destination S3 bucket')
    
    try:
        s3.upload_file('/tmp/exp/'+filename, destination_bucketname, path+'output_'+filename)
    except:
        s3.upload_file('/tmp/exp2/'+filename, destination_bucketname, path+'output_'+filename)
    
    print('end of yolo processing and uploading output image to s3 bucket')

    
    smtp_mail = os.environ['from_mail']
    from_mail = os.environ['from_mail']
    to_mail = os.environ['to_mail']
    smtp_mail_password = os.environ['password']
    
    print('before calling email function')
    mail_user(smtp_mail, from_mail, to_mail, smtp_mail_password, path, filename)
    print('after sending email')

    return {
        "statusCode": 200,
        "body": json.dumps("Document processed successfully using yolov5!"),
    }



def mail_user(smtp_mail, from_mail, to_mail, smtp_mail_password, path, filename):

    print('inside mail_user method')
    subject = "Image from lambda, Name: " + path + " " + filename
    header = """
        <html>
        <body>
             <TABLE CELLPADDING=10 CELLSPACING=20>
        <tr> """ + " <th style='text-align:centre'> Cam Image: " + "<img src=" + "/tmp/" + filename + "alt='failed to load image'> </th> </tr>"

    mailer = ""
        
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_mail
    msg['To'] = to_mail
    msg.set_content('Hi. \n Please find the image. \n Thank you.')
    msg.add_alternative(header + mailer, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(smtp_mail, smtp_mail_password)
        smtp.send_message(msg)
    print('Done mailing the user')