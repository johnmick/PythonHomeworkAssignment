from summary_stats   import *

#= JSON File Type Processors ===================================================
def message_type_processor(entry, site):
  visitor   = entry["from"]
  timestamp = entry["timestamp"]

  # Keep track of unique visitors
  site["unique_visitors"].add(visitor)

  # Record who sent this message when
  if timestamp not in site["message_activity"]:
    site["message_activity"][timestamp] = []
  site["message_activity"][timestamp].append(visitor)

  # Update Site Stats
  update_stats(site)


def status_type_processor(entry, site):
  operator = entry["from"]

  # Keep track of unique operators
  site["unique_operators"].add(operator)

  # Add site operator state change and resort
  site["operator_activity"].append((entry["timestamp"], True if entry["data"]["status"] == "online" else False, operator))
  site["operator_activity"] = sorted( site["operator_activity"], key=lambda i: i[0] )

  # Update Site Stats
  update_stats(site)

type_processors = {
  "message": message_type_processor,
  "status":  status_type_processor
}
#===============================================================================
