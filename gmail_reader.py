import base64
import os.path

from mail import Mail

class GmailReader:
  def __init__(self, gmail_api_service):
    self.service = gmail_api_service
    self.output_dir = 'output'
    os.makedirs(self.output_dir, exist_ok=True)

  def read(self, label_name):
    try:
      # search_query = f'label:{label_name} subject:#BlogContest# When Generative AI Enter Enterprise Architecture Space #博客大赛# 当生成式AI 进入企业架构的空间'
      # label_name = 'Certification'
      search_query = f'label:{label_name}'

      # Make a request to list messages based on the search query
      results = self.service.users().messages().list(userId='me', q=search_query).execute()
      messages = results.get('messages', [])

      if not messages:
        print(f'No messages found with the label "{label_name}".')
      else:
        print(f'Messages with the label "{label_name}":')
        save_emails(self, self.service, label_name, messages)
    except Exception as e:
      print(f'An error occurred: {e}')

def save_emails(self, service, label_name, messages):
    os.makedirs(f'{self.output_dir}/{label_name}', exist_ok=True)
    for message in messages:
      msg = service.users().messages().get(userId='me', id=message['id']).execute()
      mail = Mail(
        id_= msg['id'],
        subject= get_subject(msg),
        mail_from= get_from(msg),
        mail_to= get_to(msg),
        mail_date= msg['internalDate']
      )

      # Get the body of the email
      payload = msg.get('payload', {})
      read_mail_body_by_walking_tree(service, mail, payload)
      mail.render_embbeded_attachment()

      mail_file_name = f"{self.output_dir}/{label_name}/{mail.subject}.html"
      with open(mail_file_name, "a") as mail_file:
        mail_file.write(mail.format_to_html())

def read_mail_body_by_walking_tree(service, mail, payload):
    if payload.get('mimeType') == 'text/html':
      body = payload.get('body', {})
      get_mail_body(mail, body)
    elif payload.get('mimeType').startswith('image/'):
      body = payload.get('body', {})
      attachment_id = body['attachmentId']
      attachment = service.users().messages().attachments().get(
            userId='me', messageId=mail.id, id=attachment_id
        ).execute()
      mail.put_image(get_x_attachment_id(payload), payload.get('mimeType'), attachment['data'].replace('-', '+').replace('_', '/'))
    else:
      parts = payload.get('parts', {})
      for part in parts:
        read_mail_body_by_walking_tree(service, mail, part)

def get_x_attachment_id(msg):
  result = None
  for header in msg.get('headers', []):
      if header['name'] == 'X-Attachment-Id':
          result = header['value']
          break
  return result

def get_mail_body(mail, body):
    if 'data' in body:
        body_data = body['data']
        decoded_body = base64.urlsafe_b64decode(body_data).decode('utf-8')
        mail.append_body(decoded_body)
    elif 'attachmentId' in body:
        print('Body contains an attachment.')

def get_subject(msg):
    subject = None
    for header in msg.get('payload', {}).get('headers', []):
        if header['name'] == 'Subject':
            subject = header['value']
            break
    return subject

def get_from(msg):
    result = None
    for header in msg.get('payload', {}).get('headers', []):
        if header['name'] == 'From':
            result = header['value']
            break
    return result
        
def get_to(msg):
    result = None
    for header in msg.get('payload', {}).get('headers', []):
        if header['name'] == 'To':
            result = header['value']
            break
    return result

def get_cc(msg):
    result = None
    for header in msg.get('payload', {}).get('headers', []):
        if header['name'] == 'Cc':
            result = header['value']
            break
    return result