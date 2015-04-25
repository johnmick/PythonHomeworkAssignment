class NewOperatorStateStats():
  def __init__(self, datastore):
    self.sites = datastore["sites"]

  def apply_filter(self, entry):
    if entry["type"] == "status":
      site  = self.sites[entry["site_id"]]
      stats = site["stats"]

      # Update site's online/offline times
      site["site_online_times"] = self._compute_online_times(site["operator_activity"])

      # Update messages/emails using new site states
      (stats["messages"], stats["emails"]) = self._compute_messages_and_emails(
        site["site_online_times"], site["message_activity"]
      )

      # Number of unique operators
      stats["operators"] = len(site["unique_operators"])

    return entry

  def _compute_online_times(self, operator_activity):
    # Compute all state changes
    online_times     = {}
    online_operators = set([])
    for timestamp in sorted(operator_activity):
      for action in operator_activity[timestamp]:
        if action["online"]:
          online_operators.add(action["operator"])
        elif action["operator"] in online_operators:
          online_operators.remove(action["operator"])

      online_times[timestamp] = len(online_operators) > 0

    # Assuming site starts online, removing any leading offline events
    unnecessary_times = []
    for timestamp in sorted(online_times):
      if online_times[timestamp] == False:
        unnecessary_times.append(timestamp)
      else:
        break
    for timestamp in unnecessary_times:
      del online_times[timestamp]

    return online_times

  def _compute_messages_and_emails(self, site_online_times, message_activity):
    total_emails   = 0
    total_messages = 0

    if len(site_online_times) == 0:
      total_emails   = len(message_activity)
      total_messages = 0

    else:
      site_online     = False
      site_times      = sorted(site_online_times)
      state_index     = 0

      for msg_timestamp in sorted(message_activity):
        num_messages = len(message_activity[msg_timestamp])

        while state_index < len(site_times) and msg_timestamp >= site_times[state_index]:
          site_online = site_online_times[ site_times[state_index] ]
          state_index += 1

        if site_online:
          total_messages += num_messages
        else:
          total_emails   += num_messages

    return (total_messages, total_emails)
