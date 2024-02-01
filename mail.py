
from datetime import datetime, timezone
import html

from embeded_resource import EmbededResource

class Mail():
  def __init__(self, id_, subject, mail_from, mail_to, mail_date=None, mail_body=''):
    self.id = id_
    self.subject = subject
    self.mail_from = mail_from
    self.mail_to = mail_to
    self.mail_date = mail_date
    self.body = mail_body
    self.attachments = {}

  def append_body(self, body):
    self.body = self.body + body

  def format_to_html(self):
    mail_date_str = datetime.utcfromtimestamp(int(self.mail_date) / 1000).replace(tzinfo=timezone.utc)
    # Format the datetime object as a string
    formatted_date_time = mail_date_str.astimezone().strftime('%Y-%m-%d %H:%M:%S')
    return "<p>Subject: {}</p><p>Mail from: {}</p><p>Date: {}</p><div>{}</div>".format(
      html.escape(self.subject), 
      html.escape(self.mail_from), 
      html.escape(formatted_date_time), 
      self.body
    )

  def put_image(self, key, mime_type, value):
    resource = EmbededResource(resource_id=key, mime_type=mime_type, base64_content=value)
    self.attachments[key] = resource

  def render_embbeded_attachment(self):
    for attachemnt_id, resource in self.attachments.items():
      self.body = self.body.replace(f"cid:{attachemnt_id}", f"data:{resource.mime_type};base64,{resource.base64_content}")