# Step 1: Use an official lightweight Python image
FROM python:3.10-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy only the requirements first (to use Docker cache)
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your backend code
COPY . .

# Step 6: Expose the port FastAPI runs on
EXPOSE 8000

# Step 7: The command to run your app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
