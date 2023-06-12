FROM python:3

RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev libicu-dev python3-tk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip && pip3 install mysqlclient numpy

# Set the working directory to /app
WORKDIR /app

# Install required R packages
RUN apt-get update && apt-get install -y r-base && \
    Rscript -e "install.packages(c('tm', 'SnowballC', 'wordcloud', 'RColorBrewer', 'syuzhet', 'ggplot2', 'magrittr', 'quanteda', 'quickPlot', 'rainette'), repos='http://cran.us.r-project.org')"

# Copy requirements.txt and .env to the /app directory
COPY requirements.txt /app/
COPY .env /app/

# Install project dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the files to the /app directory
COPY . /app/

# Set the necessary environment variables
ENV DJANGO_SETTINGS_MODULE=production.settings

# Run Django migrations
RUN python3 manage.py migrate

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Start Gunicorn server with Django
CMD gunicorn --bind 0.0.0.0:8000 production.wsgi:application
