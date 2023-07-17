# Use Python 3 as base image
FROM python:3

# Update packages and install necessary dependencies
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev libicu-dev libharfbuzz-dev libfribidi-dev python3-tk r-base && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python packages
RUN pip3 install --upgrade pip && pip3 install mysqlclient numpy

# Set the working directory to /app
WORKDIR /app

# Set the locale
RUN apt-get clean && apt-get update && apt-get install -y locales
RUN locale-gen pt_BR.UTF-8
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR:pt
ENV LC_ALL pt_BR.UTF-8

# Install required R packages syuzhet
RUN Rscript -e "install.packages(c('tidyverse', 'syuzhet', 'textshaping', 'ragg', 'tm', 'SnowballC', 'wordcloud', 'RColorBrewer', 'syuzhet', 'ggplot2', 'magrittr', 'quanteda', 'rainette'), repos='http://cran.us.r-project.org')"

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
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# Run nlp.py script to download necessary files
RUN python3 nlp.py 'european' 'english' 13 2 5 'en' 2 3 5

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Start Gunicorn server with Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "production.wsgi:application"]
