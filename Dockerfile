FROM pixelexperience/official_devices_ci:latest

COPY . /app

WORKDIR /app

CMD ["bash", "runner.sh"]
