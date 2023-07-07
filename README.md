# Simple Chat-Server and Client

## Overview

This server provides file-sharing and chat functionalities. The code is based on Flask, a web server library in Python, and SQLite, a database engine. The server's functionalities include uploading and downloading files, creating chat rooms, and sending chat messages.

The main functions of the server include:

- File upload and download
- Creating chat rooms
- Sending chat messages

## Installation

The server image is available on ![Docker Pulls](https://img.shields.io/docker/pulls/serpensin/chatserver?logo=docker&label=Docker%20Hub&link=https%3A%2F%2Fhub.docker.com%2Frepository%2Fdocker%2Fserpensin%2Fchatserver%2Fgeneral). Execute the following command to download and start the image:

```bash
docker pull serpensin/chatserver
docker run -d -p 5000:5000 \
    -e UPLOAD_SIZE_LIMIT=100 #Upload size limit in MB
    -e FOLDER_SIZE_LIMIT=1 #Upload folder limit in GB
    -e FILE_AGE_LIMIT=10 #File age limit in minutes before deletion
    -e BASE_URL=http://localhost #Base URL for the server
    -e PORT=5000 #Port for the server. In Docker it's the port on the left side
    serpensin/chatserver
```


## Usage

After the server is started, it communicates over the following endpoints:

- `POST /upload_file`: Upload a file.
- `GET /get_file`: Download a file with a specified filename.
- `POST /create_room`: Create a new chat room with a unique ID.
- `GET /room_exists`: Check if a chat room with a given ID exists.
- `GET /health`: A health-check endpoint that returns a JSON object indicating that the server is running correctly.

For example, to create a new room, you can send an HTTP POST request to `/create_room`. The request could look like this in Python using the `requests` library:

```python
import requests

response = requests.post('http://localhost:5000/create_room', json={'room_id': 'example_room'})

if response.status_code == 201:
    print('Room created successfully.')
else:
    print('Failed to create room.')
```

Communications is handled with websockets. All messages are encrypted with AES-256 in transit between room members.
This means, that the server does not store any messages, and cannot read them. Each client that connects to a room, receives the channel key, which is used to encrypt and decrypt messages.
