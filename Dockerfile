FROM 2.7.12-wheezy
MAINTAINER dan.morel@gmail.com
COPY *.py .
COPY requirements.txt ./requirements.txt
COPY data ./data
COPY out ./out
RUN ["pip install -r ./requirements.txt"]

CMD ["python", "./main.py"]
