from threading import Thread

class FilterWorker(Thread):
  def __init__(self, filters, in_queue, out_queue):
    Thread.__init__(self)

    self.filters   = filters
    self.in_queue  = in_queue
    self.out_queue = out_queue

  def run(self):
    while True:
      # Remove an item from the input queue
      entry = self.in_queue.get()

      # Sequentially Apply Each Filter Until Entry is Removed or End Reached
      filtered_entry = entry
      for filter_proc in self.filters:
        filtered_entry = filter_proc.apply_filter( entry )

        if filtered_entry is None:
          break

      # If the filtered entry exists, add it to the output
      if filtered_entry is not None:
        self.out_queue.put( filtered_entry )

      # Signal ready for more work
      self.in_queue.task_done()
