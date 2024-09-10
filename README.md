# Poverty Mapping Web Application

This repository contains the Poverty Mapping web application for Cambodia, built with Django and utilizing Google Earth Engine, designed to be deployed on an Ubuntu server using Docker.

![Poverty Mapping Screenshot](povertymappingapp.jpg)

## Table of Contents

- [Requirements](#requirements)
- [Installation Guide](#installation-guide)
  - [Step 1: Install Docker and Docker Compose](#step-1-install-docker-and-docker-compose)
  - [Step 2: Clone the Project Repository](#step-2-clone-the-project-repository)
  - [Step 3: Obtain Google Service Account Credentials](#step-5-obtain-google-service-account-credentials)
  - [Step 4: Build and Run the Application with Docker](#step-6-build-and-run-the-application-with-docker)
  - [Step 5: Configure Nginx as a Reverse Proxy](#step-7-configure-nginx-as-a-reverse-proxy)


## Requirements

- Ubuntu server
- Docker and Docker Compose installed
- Google Service Account (obtainable from developers)

## Installation Guide

### Step 1: Install Docker and Docker Compose

1. **Install Docker**:
   ```bash
   sudo apt-get update
   sudo apt-get install docker.io
   sudo apt-get install docker-compose-v2
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

2. **Clone the Project Repository**:
   ```bash
   git clone https://github.com/sig-gis/cambodia-poverty-mapping.git povertymappingapp
   ```

3. **Obtain Google Service Account Credentials**:
- Request Credentials: Contact the developers at thannarotk@gmail.com to obtain the Google Service Account credential file.
- Add Credentials: Place the credential file in the project's root directory.

4. **Build and Run the Application with Docker**:
- Build the Docker Image:
```bash
   sudo docker compose build
   ```

- Run the Container:
```bash
   sudo docker compose up -d
   ```

- Check the Status: Verify that the container is running correctly:
```bash
   sudo docker compose ps
   ```

5. **Configure Nginx as a Reverse Proxy**:
- Install Nginx:
```bash
   sudo apt install nginx
   ```
- Create Nginx Configuration: Use nano to create the Nginx configuration file:

```bash
   sudo nano /etc/nginx/sites-available/povertymappingapp.com

   ```

- Paste the Configuration: Replace <ip_or_domain_name> with your actual values:
```bash
   server {
    listen 80;
    server_name <ip_or_domain_name>;

    location / {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

   ```

- Enable Configuration: Create a symbolic link to enable the configuration:
```bash
sudo ln -s /etc/nginx/sites-available/povertymappingapp.com /etc/nginx/sites-enabled/
```

- Remove Default Configuration:
```bash
sudo rm /etc/nginx/sites-enabled/default
```

- Test and Restart Nginx:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

You can now access the tool using your server's IP or domain name.