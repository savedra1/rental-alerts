FROM test-run

WORKDIR /home/michael/personal_projects/renting_alerts

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

#&& playwright install && playwright install-deps

COPY . /home/michael/personal_projects/renting_alerts/

CMD ["python", "src/main.py"]