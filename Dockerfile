FROM python:3.9

# SET THE WORKING DIRECTORY INSIDE THE CONTAINER TO /APP

WORKDIR /app

#Copy the requirements.txt file from the local directory  to the /app directory in the container

COPY requirements.txt .


RUN pip install --no-cache-dir --upgrade -r requirements.txt 

#Copy the entire app directory (containing main.py and any other files) from the local directory to the /app
COPY ./app /app


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]