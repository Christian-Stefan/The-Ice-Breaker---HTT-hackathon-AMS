# Use Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# 1. Install dependencies MANUALLY since you have no requirements.txt
# I included standard ones. Add others here if your code needs them.
RUN pip install --no-cache-dir fastapi uvicorn openai python-dotenv requests

# Copy all files from the current folder (backend) to the container
COPY . .

# Open the port
EXPOSE 8000

# 2. CRITICAL CHANGE:
# "server:app" means: look in "server.py" for the object named "app".
# If your FastAPI variable is named something else (e.g., 'api'), change "app" to that name.
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
