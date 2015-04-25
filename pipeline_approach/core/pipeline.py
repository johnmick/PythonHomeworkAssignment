import time

from Queue         import Queue
from threading     import Thread

from input_worker  import InputWorker
from filter_worker import FilterWorker
from output_worker import OutputWorker

class Pipeline:
  def __init__( self, inputs = [], filters = [], outputs = [],
                input_queue_maxsize = 100, output_queue_maxsize = 100,
                num_filter_threads  = 1,   input_warmup_time = 0.05 ):
    self.inputs             = inputs
    self.filters            = filters
    self.outputs            = outputs
    self.num_filter_threads = num_filter_threads
    self.input_warmup_time  = input_warmup_time

    self.in_queue           = Queue( maxsize = input_queue_maxsize )
    self.out_queue          = Queue( maxsize = output_queue_maxsize )

  def run(self):
    # Start Inputs:
    input_threads = []
    for input_proc in self.inputs:
      in_thread = InputWorker( input_proc, self.in_queue )
      in_thread.setDaemon(True)
      in_thread.start()
      input_threads.append( in_thread )
    time.sleep( self.input_warmup_time )

    # Start Filters:
    filter_threads = []
    for filter_thread_num in range( self.num_filter_threads ):
      filter_thread = FilterWorker( self.filters, self.in_queue, self.out_queue )
      filter_thread.setDaemon(True)
      filter_thread.start()
      filter_threads.append( filter_thread )

    # Start Output Worker on a Single Thread
    output_thread = OutputWorker( self.outputs, self.out_queue )
    output_thread.setDaemon(True)
    output_thread.start()

    # Wait for Input Threads to Complete Processing
    for input_thread in input_threads:
      input_thread.join()

    # Wait for Input and Output Queues to Empty
    self.in_queue.join()
    self.out_queue.join()

    # Tell Output Worker The Pipeline is Finished, all outputs finish are called in a blocking manner
    output_thread.finish()
