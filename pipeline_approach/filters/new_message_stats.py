class NewMessageStats():
  def __init__(self, datastore):
    self.sites = datastore["sites"]

  def apply_filter(self, entry):
    if entry["type"] == "message":
      site              = self.sites[entry["site_id"]]
      stats             = site["stats"]
      msg_timestamp     = entry["timestamp"]
      site_online_times = site["site_online_times"]

      # Play site state forward until message time
      site_online = False
      for timestamp in sorted(site_online_times):
        if msg_timestamp > timestamp:
          site_online = site_online_times[timestamp]
        else:
          break

      if site_online:
        stats["messages"] += 1

      else:
        stats["emails"] += 1

      # Number of Unique Visitors
      stats["visitors"] = len(site["unique_visitors"])

    return entry
