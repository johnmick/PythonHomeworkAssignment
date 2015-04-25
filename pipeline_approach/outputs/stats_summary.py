from pprint import pprint
class StatsSummary:
  def __init__(self, datastore):
    self.datastore = datastore
    pass

  def output(self, entry):
    pass

  def finish(self):
    sites = self.datastore["sites"]

    for site_id in sorted(sites):
      stats = sites[site_id]["stats"]
      print("%s,messages=%d,emails=%d,operators=%d,visitors=%d" % (
        site_id, 
        stats["messages"], 
        stats["emails"], 
        stats["operators"], 
        stats["visitors"]
      ))
