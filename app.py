from gmail_connection import GmailConnection
from gmail_reader import GmailReader

def main():
  gmail_connection = GmailConnection()
  gmail_reader = GmailReader(gmail_api_service = gmail_connection.connect())
  gmail_reader.read(label_name = 'Certification')

if __name__ == "__main__":
  main()