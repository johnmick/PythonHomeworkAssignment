import sys

class ClientMessageProcessor:
  def __init__(self, datastore):
    self.datastore = datastore

  def apply_filter( self, entry ):
    if entry["type"] != "message":
      return entry

    try:
      site      = self.datastore["sites"][entry["site_id"]]
      visitor   = entry["from"]
      timestamp = entry["timestamp"]

      # Track unique visitors
      site["unique_visitors"].add(visitor)

      # Record who sent this message when
      if timestamp not in site["message_activity"]:
        site["message_activity"][timestamp] = []
      site["message_activity"][timestamp].append(visitor)

      return entry

    except:
      sys.stderr.write("[Client Message Processor] Error processing entry\n")

      return None
