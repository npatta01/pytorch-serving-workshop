FROM pytorch/torchserve:0.4.0-cpu

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /home/model-server/
#COPY * /home/model-server/
COPY model_store model_store
COPY * /home/model-server/


USER model-server


RUN pwd
RUN ls
CMD ["torchserve", \
     "--start", \
     "--ts-config=/home/model-server/config.properties"]