from threading import Thread

class OutputWorker(Thread):
  def __init__(self, outputs, out_queue):
    Thread.__init__(self)

    self.outputs   = outputs
    self.out_queue = out_queue

  def run(self):
    while True:
      entry = self.out_queue.get()

      for output_proc in self.outputs:
        output_proc.output( entry )

      self.out_queue.task_done()

  def finish(self):
    for output_proc in self.outputs:
      output_proc.finish()
