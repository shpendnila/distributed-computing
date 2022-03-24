FROM python:3.8
WORKDIR /app/
COPY src ./src/
RUN pip3 install --no-cache-dir -r ./src/requirements.txt
CMD ["python", "-m", "app.main"]
