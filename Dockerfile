#Base Image to use
FROM python:3.12

ENV PORT 8084

EXPOSE 8084
WORKDIR /vanna_ai
COPY . ./

#install all requirements in requirements.txt
RUN pip install -r requirements.txt

# Run the web service on container startup
CMD ["python3", "app.py"]
