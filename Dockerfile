FROM flyteorg/flytekit:latest
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/app

# Expose Flyte tasks when this image is used by pyflyte
ENTRYPOINT ["bash"]
