class InitSiteRecords:
  def __init__(self, datastore):
    self.datastore  = datastore

  def apply_filter( self, entry ):
    if entry["site_id"] not in self.datastore["sites"]:
      self.datastore["sites"][entry["site_id"]] = {
        "site_online_times": {},
        "operator_activity": {},
        "message_activity":  {},
        "unique_operators":  set([]),
        "unique_visitors":   set([]),

        "stats": {
          "messages":  0,
          "emails":    0,
          "operators": 0,
          "visitors":  0
        }
      }

    return entry
