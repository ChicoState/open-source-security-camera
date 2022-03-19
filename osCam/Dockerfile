FROM python:3.9.10
COPY requirements.txt ./
RUN pip install --user -r requirements.txt
COPY . ./
RUN chmod +x docker_run_server.sh
EXPOSE 80
ENTRYPOINT ["./docker_run_server.sh"]