# Gmail To Html

## Introduction
`gmail-to-html` is a Python CLI application that can download emails and save them as HTML files. It allows you to download emails that meet specified criteria based on labels and search conditions. Since the emails are saved in HTML format, you can easily use a web browser to view them or utilize these HTML files for other purposes.

## Quick Start
To run the application, follow these steps:
1. Clone this repo, locate to your directory and install all requirements:
  ```bash
  git clone git@github.com:michaelxmn/gmail-to-html.git
  cd gmail-to-html
  pip install -r requirements.txt
  ```

2. Download your GCP OAuth credentials as `<your_repository_path>/credentials.json`, visit `https://developers.google.com/workspace/guides/create-credentials` for more guides

3. Run the application using the following command:
  ```bash
  python app.py
  ```
4. Signing with your Goggle account in the browser, once you signed successfully, the application will download your emails in `Inbox` and then put all the emails to location `<your_repository_path>/output/Inbox/` with file extenstion `.html`

## Prerequisites
Ensure you have the following prerequisites installed:
- Python (version >= 3.9.0)

## Configuration
Since the application use Gmail API for read emails, you must `create OAuth consent screen` and `OAuth client credentials` on GCP.
1. create OAuth consent screen on [Credentials consent page](https://console.cloud.google.com/apis/credentials/consent), visit [Configure the OAuth consent screen and choose scopes](https://developers.google.com/workspace/guides/configure-oauth-consent?hl=en) for more guides
2. create OAuth client credentials on [GCP Credentials page](https://console.cloud.google.com/apis/credentials), visit [Create access credentials](https://developers.google.com/workspace/guides/create-credentials) for more guides
3. Click button `Download OAuth client` under column `Actions` on [GCP Credentials page](https://console.cloud.google.com/apis/credentials), download file as `credentials.json` and put it in <your_repository_path>

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
