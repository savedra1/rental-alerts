FROM python:3.10

WORKDIR /app

COPY requirements.txt .

#RUN pip install --no-cache-dir -r requirements.txt 
#RUN playwright install && playwright install-deps

COPY . /app

CMD ["python", "tmp.py"]