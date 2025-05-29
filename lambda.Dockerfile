FROM public.ecr.aws/lambda/python:3.10

RUN yum install -y gcc gcc-c++ make
COPY api/requirements.txt .
RUN pip install -r requirements.txt

COPY api .

CMD ["src.main.handler"]