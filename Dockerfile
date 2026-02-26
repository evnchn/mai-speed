FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY elucidator.py dark_repulser.py common_functions.py ./

RUN mkdir -p cache && touch cached_paths.txt

RUN useradd --create-home appuser && chown appuser:appuser cache cached_paths.txt
USER appuser

EXPOSE 10000

CMD ["python", "elucidator.py"]
