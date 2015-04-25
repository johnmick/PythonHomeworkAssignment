import sys

class OperatorStateProcessor:
  def __init__(self, datastore):
    self.datastore  = datastore

  def apply_filter( self, entry ):
    if entry["type"] != "status":
      return entry

    try:
      site         = self.datastore["sites"][entry["site_id"]]
      operator     = entry["from"] 
      timestamp    = entry["timestamp"] 
      online_state = entry["data"]["status"] == "online"

      # Track unique operators
      site["unique_operators"].add(operator)

      # Add site operator state change
      if timestamp not in site["operator_activity"]:
        site["operator_activity"][timestamp] = []

      site["operator_activity"][timestamp].append({
        "online":   online_state,
        "operator": operator
      })

      return entry

    except:
      sys.stderr.write("[Operator State Processor] Error processing entry\n")
      return None
