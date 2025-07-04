#Dockerfile
FROM python:3.11


#Set Working Directory
WORKDIR /app

#Install Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy App Code
COPY . .

#Expose Port and Run Server
CMD ["uvicorn", "--host", "127.0.0.1", "--port","8000"]