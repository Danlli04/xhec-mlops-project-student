# Make sure to check bin/run_services.sh, which can be used here

# Do not forget to expose the right ports! (Check the PR_4.md)

FROM python:3.10.13-slim
WORKDIR /app_home
COPY ./requirements.txt /app_home/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /app_home/requirements.txt
COPY ./web_service /app_home/web_service
WORKDIR /app_home/web_service

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]