class DuplicateMessageFilter:
  def __init__(self, datastore):
    self.message_ids = datastore["message_ids"]

  def apply_filter( self, entry ):
    if entry["id"] not in self.message_ids:
      self.message_ids.add(entry["id"])
      return entry

    else:
      return None
