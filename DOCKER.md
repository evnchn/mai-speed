# mai-speed Docker Guide

## What is mai-speed?

mai-speed is a Flask-based image caching proxy for maimaidx-eng.com game assets. It intercepts image requests, caches them locally, and serves cached copies to reduce load times and bandwidth usage.

The application has two components:

- **Web server** (`elucidator.py`) -- A Flask server that proxies and caches image requests from maimaidx-eng.com. Listens on port 10000.
- **Cache updater** (`dark_repulser.py`) -- A background process that refreshes all cached images daily at 7am to keep the cache up to date.

## Running with Docker Compose (Recommended)

Docker Compose runs both the web server and the cache updater together, sharing a persistent cache volume.

### Build and start

```bash
docker compose up -d --build
```

### Stop

```bash
docker compose down
```

### View logs

```bash
docker compose logs -f
```

The web server will be available at `http://localhost:10000`.

## Running with Docker (Single Container)

If you only need the web server without the background cache updater:

### Build the image

```bash
docker build -t mai-speed .
```

### Run the container

```bash
docker run -d \
  -p 10000:10000 \
  -v mai-speed-cache:/app/cache \
  --name mai-speed \
  mai-speed
```

The web server will be available at `http://localhost:10000`.

## Port Mapping

| Host Port | Container Port | Service    |
|-----------|----------------|------------|
| 10000     | 10000          | Web server |

## Persistent Cache Volume

Both services share a named volume (`cache-data` in Compose, or `mai-speed-cache` when using Docker directly) mounted at `/app/cache` inside the container. This volume persists cached images across container restarts and rebuilds.

To inspect the volume:

```bash
docker volume inspect mai-speed_cache-data
```

To remove the volume and clear the cache:

```bash
docker compose down -v
```
