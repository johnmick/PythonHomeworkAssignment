from threading import Thread

class InputWorker(Thread):
  def __init__(self, input_processor, in_queue):
    Thread.__init__(self)

    self.in_queue        = in_queue
    self.input_processor = input_processor

  def run(self):
    self.input_processor.run( self.in_queue )
