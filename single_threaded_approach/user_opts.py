import getopt, sys

options = {
  "input_file":      None,
  "write_frequency": 50000,
  "clear_cache":     False
}

unix_opts       = 'f:s:hc'
long_opts       = ['filename=', 'save_interval=', 'help', 'clear_cache']

#= Option Loading Helpers======================================================
def usage():
  print """
  Usage Help:
    -f, --filename      <input file>  Full path to input file 

    -s, --save_interval    <integer>  # of messages to process before saving
                                      Configured to  save every %d messages 

    -c, --clear_cache                 Clears cache generated from session runs
                                      * Current implementation must clear cache
                                      * between processing different input
                                      * files 

    -h, --help                        Displays usage options

  Examples:
    Process file from beginning, or resume if able:
      python main.py -f input_data/big_input

    Force reprocessing on an entire file:
      python main.py -s 100000 -f input_data/big_input -c
  """ % options["write_frequency"]


def validate_opts():
  if options["input_file"] is None:
    print("Input filename required for processing")
    usage()
    sys.exit(2)


def load_opts():
  try:
    opts, args = getopt.getopt(sys.argv[1:], unix_opts, long_opts)

  except getopt.GetoptError as err:
    print("Invalid Option Specified: %s" % err)
    usage()
    sys.exit(2)

  for opt, value in opts:
    if opt in ("-f", "--filename"):
      options["input_file"] = str(value)

    elif opt in ("-s", "--save_interval"):
      options["write_frequency"] = int(value)

    elif opt in ("-c", "--clear_cache"):
      options["clear_cache"] = True

    elif opt in ("-h", "--help"):
      usage()
      sys.exit(0)

  validate_opts()

  return options
#==============================================================================
