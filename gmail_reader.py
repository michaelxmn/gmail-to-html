import base64
from functools import partial
import os.path

from mail import Mail
import multiprocessing

from stop_watch import Stopwatch

def invoke_instance_method(instance, args):
  instance.transform_to_html(*args)

class GmailReader:
  def __init__(self, gmail_api_service, output_dir='output'):
    self.service = gmail_api_service
    self.output_dir = output_dir

  def read(self, label_name):
    try:
      search_query = f'label:{label_name}'
      # Make a request to list messages based on the search query
      results = self.service.users().messages().list(userId='me', q=search_query).execute()
      messages = results.get('messages', [])

      if not messages:
        print(f'No messages found with the label "{label_name}".')
      else:
        print(f'Messages with the label "{label_name}":')
        self.transform_emails_to_html(self.service, label_name, messages)
    except Exception as e:
      print(f'An error occurred: {e}')

  def transform_to_html(self, service, label_name, message):
    msg = service.users().messages().get(userId='me', id=message['id']).execute()
    mail = Mail(
        id_= msg['id'],
        subject= self.get_subject(msg),
        mail_from= self.get_from(msg),
        mail_to= self.get_to(msg),
        mail_date= msg['internalDate']
      )
    payload = msg.get('payload', {})
    self.read_mail_body_by_walking_tree(service, mail, payload)
    mail.render_embbeded_attachment()

    mail_file_name = f"{self.output_dir}/{label_name}/{mail.subject}.html"
    with open(mail_file_name, "a") as mail_file:
      mail_file.write(mail.format_to_html())

  def transform_emails_to_html(self, service, label_name, messages):
    os.makedirs(f'{self.output_dir}/{label_name}', exist_ok=True)
    with multiprocessing.Pool(8) as pool:
      processing_args = []
      for message in messages:
        processing_args.append((service, label_name, message))
      partial_function = partial(invoke_instance_method, self)
      stopwatch = Stopwatch()
      stopwatch.start()
      pool.map(partial_function, processing_args)
      stopwatch.stop()
      print(f"Elapsed Time: {stopwatch.elapsed_time()} seconds")

  def read_mail_body_by_walking_tree(self, service, mail, payload):
    if payload.get('mimeType') == 'text/html':
      body = payload.get('body', {})
      self.get_mail_body(mail, body)
    elif payload.get('mimeType').startswith('image/'):
      body = payload.get('body', {})
      attachment_id = body['attachmentId']
      attachment = service.users().messages().attachments().get(
            userId='me', messageId=mail.id, id=attachment_id
        ).execute()
      mail.put_image(self.get_x_attachment_id(payload), payload.get('mimeType'), attachment['data'].replace('-', '+').replace('_', '/'))
    else:
      parts = payload.get('parts', {})
      for part in parts:
        self.read_mail_body_by_walking_tree(service, mail, part)

  def get_x_attachment_id(self, msg):
    result = None
    for header in msg.get('headers', []):
        if header['name'] == 'X-Attachment-Id':
            result = header['value']
            break
    return result

  def get_mail_body(self, mail, body):
    if 'data' in body:
        body_data = body['data']
        decoded_body = base64.urlsafe_b64decode(body_data).decode('utf-8')
        mail.append_body(decoded_body)
    elif 'attachmentId' in body:
        print('Body contains an attachment.')

  def get_subject(self, msg):
    subject = None
    for header in msg.get('payload', {}).get('headers', []):
        if header['name'] == 'Subject':
            subject = header['value']
            break
    return subject

  def get_from(self, msg):
    result = None
    for header in msg.get('payload', {}).get('headers', []):
        if header['name'] == 'From':
            result = header['value']
            break
    return result
        
  def get_to(self, msg):
    result = None
    for header in msg.get('payload', {}).get('headers', []):
        if header['name'] == 'To':
            result = header['value']
            break
    return result

  def get_cc(self, msg):
    result = None
    for header in msg.get('payload', {}).get('headers', []):
        if header['name'] == 'Cc':
            result = header['value']
            break
    return result