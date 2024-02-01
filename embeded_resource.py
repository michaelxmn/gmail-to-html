
class EmbededResource:
  def __init__(self, resource_id, mime_type, base64_content):
    self.resource_id=resource_id
    self.mime_type=mime_type
    self.base64_content=base64_content