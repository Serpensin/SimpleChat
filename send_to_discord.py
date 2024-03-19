import os
import requests
import sys

def main():
    webhook_url = sys.argv[1]
    for file in os.listdir():
        if file.startswith("archive"):
            files = {'file': open(file, 'rb')}
            response = requests.post(webhook_url, files=files)
            print(response.text)

if __name__ == "__main__":
    main()