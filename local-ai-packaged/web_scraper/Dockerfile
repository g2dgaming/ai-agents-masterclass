# Use official Python image
FROM crawl4ai

# Set the working directory inside the container
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn crawl4ai

# Expose the port that FastAPI runs on
EXPOSE 6969

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "6969"]
