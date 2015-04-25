#= Defaults ===================================================================
unix_opts = 'f:h'
long_opts = ['filename=', 'help']

options = {
  "input_file":           None,
  "config_file":          None,
  "sincedb_file":         ".last_processed",
  "data_cache_file":      ".site_data",
  "max_input_queue_size": 1000
}
#==============================================================================


#= Pipeline Types in Use ======================================================
from core    import Pipeline

from inputs  import JsonFileReader

from filters import DuplicateMessageFilter
from filters import InitSiteRecords
from filters import OperatorStateProcessor
from filters import ClientMessageProcessor
from filters import NewMessageStats
from filters import NewOperatorStateStats

from outputs import StatsSummary
#==============================================================================


#= Python Modules =============================================================
from pprint import pprint
from Queue import Queue
import getopt, sys, importlib, cPickle
#==============================================================================


#= Load user options, resume state, define pipeline, run pipeline, show results
def main():
  # Apply User Options
  _load_opts()

  # Establish starting state
  start_position = _load_start_position(options["sincedb_file"])
  if start_position > 0:
    data = _load_cached_data(options["data_cache_file"])
  else:
    data = _init_datastore()

  # Define Inputs
  pipeline_inputs = [
    JsonFileReader( 
      input_file     = options["input_file"],
      start_position = start_position
    )
  ]

  # Define Filters/Processors Chain
  pipeline_filters = [
    DuplicateMessageFilter(data),
    InitSiteRecords(data),

    OperatorStateProcessor(data),
    ClientMessageProcessor(data),

    NewMessageStats(data),
    NewOperatorStateStats(data)
  ]

  # Define Pipeline Outputs
  pipeline_outputs = [
    StatsSummary(data)
  ]

  # Execute Pipeline
  Pipeline(
    inputs  = pipeline_inputs,
    filters = pipeline_filters,
    outputs = pipeline_outputs
  ).run()
#==============================================================================


#= Initialize State ============================================================
def _load_start_position(sincedb_filename):
  import os.path
  last_read = 0
  if os.path.isfile(sincedb_filename):
    with open(sincedb_filename, "r") as f:
      try:
        last_read = int(f.read())
      except ValueError as err:
        pass

  return last_read

def _load_cached_data(data_cache_filename):
  data = None
  with open(data_cache_filename, "rb") as f:
    data = cPickle.load(f)

  if data == None:
    data = _init_datastore()

  return data

def _init_datastore():
  return {
    "sites":       {},
    "message_ids": set([])
  }
#==============================================================================


#= Option Loading Helpers======================================================
def _usage():
  print """
  Site Message Stat Muncher Usage Help:
    -f, --filename <input file>  Full path to input file 
    -h, --help                   Displays usage options
  """

def _load_opts():
  try:
    opts, args = getopt.getopt(sys.argv[1:], unix_opts, long_opts)

  except getopt.GetoptError as err:
    print("Invalid Option Specified: %s" % err)
    _usage()
    sys.exit(2)

  for opt, value in opts:
    if opt in ("-f", "--filename"):
      options["input_file"]  = value
    elif opt in ("-h", "--help"):
      _usage()
      sys.exit(0)
#==============================================================================
if __name__ == "__main__":
  main()
