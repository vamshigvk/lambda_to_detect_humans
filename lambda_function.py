import os
import json
import boto3
import smtplib
from email.message import EmailMessage
from os import environ
from datetime import date
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


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
    print('path found for S3 is:', path)
    print('Key we are downloading is: ',filename)
    
    print('before downloading file from S3, filename: at /tmp/', filename)
    try:
        bucket.download_file(file_key_name, "/tmp/" + filename)
    except Exception as e:
        print('failed to download file from S3, exception occurred: ',e)

    print('inside this directory: ',os.getcwd())
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    print('contents in current directory:', files)

    print('before calling detect python file')
    try:
        os.system("python3 detect.py --project /tmp/ --exist-ok --source /tmp/"+ filename  )
    except Exception as e:
        print('exception occurred in detect python file: ', e)

    print('before uploading output file to destination S3 bucket')
    
    try:
        s3.upload_file('/tmp/exp/'+filename, destination_bucketname, path+'/output_'+filename)
    except:
        print('inside exp 2 ')
        s3.upload_file('/tmp/exp2/'+filename, destination_bucketname, path+'/output_'+filename)
    
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
    try:
        with open('/tmp/'+filename, 'rb') as f:
            img_data = f.read()

        msg = MIMEMultipart()
        msg['Subject'] = "Image from lambda, Client/Cam: " + path + " " + filename
        msg['From'] = from_mail
        msg['To'] = to_mail

        text = MIMEText("Image: ")
        msg.attach(text)
        image = MIMEImage(img_data, name=os.path.basename(filename))
        msg.attach(image)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(smtp_mail, smtp_mail_password)
            smtp.send_message(msg)
        print('Done mailing the user')
    except Exception as e:
        print('trying from the second emailing method, exception is: ',e)
        SendMail1(smtp_mail, from_mail, to_mail, smtp_mail_password, path, filename)
        print('done sending email from sendmail1 method')


def SendMail1(smtp_mail, from_mail, to_mail, smtp_mail_password, path, filename):
    print('inside mail_user method')
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(smtp_mail, smtp_mail_password)

    msg = MIMEMultipart()  # create a message

    f = open('/tmp/'+filename, 'rb')
    image = MIMEImage(f.read())
    # image.add_header('Content-Disposition', "Koeman88")
    f.close()
    msg.attach(image)

    # setup the parameters of the message

    msg['From'] = from_mail
    msg['To'] = to_mail
    msg['Subject'] = "Image from lambda, Client/Cam: " + path + " " + filename

    # add in the message body
    msg.attach(MIMEText('test', 'plain'))
    # send the message via the server set up earlier.
    s.send_message(msg)
    s.quit()
    print('Done mailing the user')
