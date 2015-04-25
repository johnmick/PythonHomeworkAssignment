#= Summary Statistics ==========================================================
def print_stats(sites):
  for site_id in sorted(sites):
    stats = sites[site_id]["stats"]
    print("%s,messages=%d,emails=%d,operators=%d,visitors=%d" % (
      site_id, stats["messages"], stats["emails"],
      stats["unique_operators"], stats["unique_visitors"]
    ))


def update_stats(site):
  stats = site["stats"]

  stats["unique_operators"] = len(site["unique_operators"])
  stats["unique_visitors"]  = len(site["unique_visitors"])
  stats["emails"]    = 0 
  stats["messages"]  = 0 

  operators   = set([])
  state_index = 0
  for timestamp in sorted(site["message_activity"]):
    num_messages = len(site["message_activity"][timestamp])

    # Roll state forward
    while state_index < len(site["operator_activity"]) and timestamp >= site["operator_activity"][state_index][0]:
      online   = site["operator_activity"][state_index][1]
      operator = site["operator_activity"][state_index][2]
      if online:
        operators.add(operator)
      elif operator in operators:
        operators.remove(operator)
      state_index += 1

    if len(operators) > 0:
      stats["messages"] += num_messages
    else:
      stats["emails"]   += num_messages
#===============================================================================
