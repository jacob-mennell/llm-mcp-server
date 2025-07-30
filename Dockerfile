FROM python:3.10-slim

# Install Poetry
RUN pip install --no-cache-dir poetry

WORKDIR /app

# Copy only dependency files first for better Docker cache
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the code
COPY . .

# Expose port
EXPOSE 8000

# Run the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
