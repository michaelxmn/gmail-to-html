from gmail_connection import GmailConnection
from gmail_reader import GmailReader
import os.path
import click

@click.command()
@click.option('--credentials', type=str, default = 'credentials.json', help='Credentials on gcp, you can login `https://console.cloud.google.com/apis/credentials`, create your credentials and then save it to local file such as my_credentials.json, pass `--credentials my_credentials.json`')
@click.option('--output_dir', type=str, default = 'output', help='Directory to place *.html')
@click.option('--label', type=str, default = 'Inbox', help='e.g. Inbox')
def main(credentials, output_dir, label):
  validate_credentials(credentials)
  create_output_directory(output_dir)
  gmail_connection = GmailConnection(credentials_file=credentials)
  gmail_reader = GmailReader(output_dir=output_dir, gmail_api_service = gmail_connection.connect())
  gmail_reader.read(label_name = label)

def validate_credentials(credentials):
  if not os.path.exists(credentials):
    raise ValueError(f"Please provide your credentials as file `{credentials}`")

def create_output_directory(output_dir):
  os.makedirs(output_dir, exist_ok=True)

if __name__ == "__main__":
  main()