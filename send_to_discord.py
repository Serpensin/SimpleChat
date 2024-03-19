import requests
import sys

def main():
    webhook_url = sys.argv[1]
    message = {'content': 'New build available!'}
    files = {'file': open('archive.7z', 'rb')}
    requests.post(webhook_url, data=message, files=files)

if __name__ == "__main__":
    main()