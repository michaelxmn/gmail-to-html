from gmail_connection import GmailConnection
from gmail_reader import GmailReader
import os.path

OUTPUT_DIR = 'output'

def main():
  gmail_connection = GmailConnection()
  gmail_reader = GmailReader(output_dir=OUTPUT_DIR, gmail_api_service = gmail_connection.connect())
  gmail_reader.read(label_name = 'Certification')

def initialize():
  os.makedirs(OUTPUT_DIR, exist_ok=True)

if __name__ == "__main__":
  initialize()
  main()