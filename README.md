# Your Application Name

## Introduction
Briefly introduce your application here. Include its purpose, main features, and any other relevant information.

## Quick Start
To run the application, follow these steps:
1. Clone this repo, locate to your directory and install all requirements:
  ```bash
  git clone git@github.com:michaelxmn/gmail-to-html.git
  cd gmail-to-html
  pip install -r requirements.txt
  ```

2. Download your GCP oauth-credentials as `<your_repository_path>/credentials.json`, guides: `https://developers.google.com/workspace/guides/create-credentials`

3. Run the application using the following command:
  ```bash
  python app.py
  ```
4. Signing with your Goggle account in the browser, once you signed successfully, the application will download your emails in `Inbox` and then put all the emails to location `<your_repository_path>/output/Inbox/` with file extenstion `.html`

## Prerequisites
Ensure you have the following prerequisites installed:
- Python (version >= 3.9.0)

## Configuration
- create GCP OAuth `credentials.json` in <your_repository_path>

## Usage
- Download your emails in `Inbox` and then put all the emails to location `<your_repository_path>/output/Inbox/` with file extenstion `.html`
  ```bash
  python app.py
  ```
- Change label to `Important` to download emails tagged with label `Important`:
  ```bash
  python app.py --label Important
  ```

- Filter emails with `--q` or `--query`:
  ```bash
  python app.py --label Important --q "Subject:This is a subject of email"
  ```
  or 
  ```bash
  python app.py --label Important --query "Subject:This is a subject of email"
  ```

- Change output directory:
  ```bash
  python app.py --output_dir my_output_dir
  ```

- Change default credentials file:
  ```bash
  python app.py --credentials my_credentials.json
  ```

## License
Apache 2.0
