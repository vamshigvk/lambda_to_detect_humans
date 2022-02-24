def lambda_handler(event, context):

    main()

def main():
    python3 detect.py -weights "model path" -source "img file" -view-img
    return "hi from main"