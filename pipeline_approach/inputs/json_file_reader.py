import sys, json

class JsonFileReader: 
  def __init__(self, input_file=None, start_position=0):
    self.input_file     = input_file
    self.start_position = start_position

    if type(self.input_file) is not str:
      sys.stderr.write("Json File Reader may not initialize without filename\n")
      sys.exit(2)

    if type(self.start_position) is not int:
      sys.stderr.write("Json File Reader must be assigned a start_position of type 'int'")
      sys.exit(2)

  def run(self, queue):
    with open(self.input_file) as f:
      f.seek(self.start_position)

      for line in iter(f.readline, ''):
        queue.put( json.loads(line) )
