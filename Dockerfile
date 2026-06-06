# Use an official lightweight Python image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files
# and to keep stdout unbuffered so logs show up immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set up a non-root user (Required for Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory inside the container
WORKDIR $HOME/app

# Copy the requirements file first to leverage Docker cache
COPY --chown=user backend/requirements.txt $HOME/app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend folder contents into the app directory
COPY --chown=user backend/ $HOME/app/

# Hugging Face Spaces uses port 7860 by default.
EXPOSE 7860

# Command to start the Uvicorn server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
