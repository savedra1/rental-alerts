FROM python:3.10

WORKDIR /home/michael/personal_projects/renting_alerts

COPY requirements.txt .

#RUN pip install --no-cache-dir -r requirements.txt 
#RUN playwright install && playwright install-deps

COPY . /home/michael/personal_projects/renting_alerts/

CMD ["python", "tmp.py"]