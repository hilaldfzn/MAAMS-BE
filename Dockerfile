FROM python:3.10-slim

EXPOSE 8000

# Argument variables
# ARG PRODUCTION
# ARG SUPABASE_URL
# ARG SUPABASE_PASSWORD
# ARG SUPABASE_USERNAME

# Required environment variables here
# ENV SECRET_KEY=value
# ENV PRODUCTION ${PRODUCTION}
ENV SUPABASE_URL ${SUPABASE_URL}
ENV SUPABASE_USERNAME ${SUPABASE_USERNAME}
ENV SUPABASE_PASSWORD ${SUPABASE_PASSWORD}


# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "maams_be.wsgi"]
