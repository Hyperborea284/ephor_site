# Use Python 3 as base image
FROM python:3

# Update packages and install necessary dependencies
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev libicu-dev python3-tk r-base && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python packages
RUN pip3 install --upgrade pip && pip3 install mysqlclient numpy

# Set the working directory to /app
WORKDIR /app

# Set Locale
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install required R packages
RUN Rscript -e "install.packages(c('textshaping', 'ragg', 'tm', 'SnowballC', 'wordcloud', 'RColorBrewer', 'syuzhet', 'ggplot2', 'magrittr', 'quanteda', 'rainette'), repos='http://cran.us.r-project.org')"

# Copy requirements.txt and .env to the /app directory
COPY requirements.txt .env /app/

# Install project dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Download Spacy language models
RUN python3 -m spacy download pt_core_news_sm
RUN python3 -m spacy download es_core_news_sm
RUN python3 -m spacy download en_core_web_sm

# Copy the rest of the files to the /app directory
COPY . /app/

# Set the necessary environment variables
ENV DJANGO_SETTINGS_MODULE=production.settings

# Run Django migrations
RUN python3 manage.py collectstatic --noinput
Run python3 manage.py makemigrations
Run python3 manage.py migrate

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Start Gunicorn server with Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "production.wsgi:application"]
