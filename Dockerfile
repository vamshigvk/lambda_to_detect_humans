FROM public.ecr.aws/lambda/python:3.6
RUN yum update -y

COPY . ${LAMBDA_TASK_ROOT}/

RUN pip install --upgrade pip

RUN git clone https://github.com/ultralytics/yolov5.git && cd yolov5 &&  \
    pip3 install torch==1.10.1+cpu torchvision==0.11.2+cpu torchaudio==0.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

RUN pip install -r requirements.txt

#RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD [ "lambda_function.lambda_handler" ]
