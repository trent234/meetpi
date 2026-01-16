# MeetPi

![MeetPi Logo](./src/meetpi/static/logo.png)

A minimal JWT issuer for Jitsi meetings. This container builds a small web UI you can use to generate short-lived join links.

### Prerequisites

- Docker

### Build the image

```bash
docker build -t meetpi .
```

### Start the webserver

Run the container and forward port 8080. Provide required environment variables via `--env-file` or individual `-e` flags.

```bash
docker run -p 8080:8080 --rm --env-file .env meetpi
```

Required environment variables (put these in `.env` or pass them via `-e`):
- JWT_APP_SECRET
- JWT_ACCEPTED_ISSUERS
- JWT_ACCEPTED_AUDIENCES

Its the JWT_APP_SECRET in particular that allow this web service to  
make cryptographically secure meeting links for the Jitsi service.  
Make sure this value is consistent between this service and Jitsi.  

### Using docker-compose

As an alternative you can run the service with docker-compose. Create a `docker-compose.yml` alongside the repository (example):

```yaml
version: "3.8"
services:
  meetpi:
    build: .
    image: meetpi
    ports:
      - "8080:8080"
    env_file:
      - .env
    restart: unless-stopped
```

Start with:

```bash
docker-compose up --build
```
