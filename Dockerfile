# Use official Python image
FROM python:3.14

# Set work directory
WORKDIR /app

# Copy requirements and install globally
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the code
COPY src/ ./src/

# Add src to PYTHONPATH for imports
ENV PYTHONPATH="/app/src"

# Run tests with correct pattern
WORKDIR /app/src
CMD ["python", "-m", "unittest", "discover", "-s", "Tests", "-p", "*Tests.py"]
