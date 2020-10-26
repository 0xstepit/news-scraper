# Base image
FROM python:3.7

COPY ./requirements.txt /requirements.txt

# Work directory
WORKDIR /

# Install requirements
RUN pip install -r requirements.txt

COPY . /

# Execute commands when image loads
CMD ["python3", "src/scraper.py"]