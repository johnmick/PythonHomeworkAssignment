import json, cPickle, sys, os

from user_opts       import *
from type_processors import *
from state_save_load import *

#= Core ========================================================================
def main():
  load_opts()

  if options["clear_cache"]:
    clear_cache()


  # Establish Starting State
  if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)
  start_position = load_last_processed_position()
  data           = init_data(start_position)

  # Process Input Messages
  process_messages(data, start_position, options["write_frequency"])

  # Print Statistics
  print_stats(data["sites"])


def process_messages(data, start_position, write_freq=50000):
  with open(options["input_file"]) as f:
    # Resume playhead
    f.seek(start_position)

    # Count number of lines processed while reading file
    for stat_processed_count, line in enumerate(iter(f.readline, '')):
      handle_entry(json.loads(line), data)

      # Save on processed item interval
      if stat_processed_count > 0 and stat_processed_count % write_freq == 0:
        save_stats(data)
        save_position(f.tell())

    # If we read the file at all, save again
    if start_position != f.tell():
      save_stats(data)
      save_position(f.tell())


def handle_entry(entry, data):
  # Establish a site reference
  if entry["site_id"] not in data["sites"]:
    data["sites"][entry["site_id"]] = init_site()
  site = data["sites"][entry["site_id"]]

  # Only process unique messages
  if entry["id"] not in data["message_ids"]:
    data["message_ids"].add(entry["id"])

    # If we have a processor for the message, process message and update stats
    if type_processors.has_key( entry["type"] ):
      type_processors[ entry["type"] ](entry, site)
      update_stats(site)


def init_data(seek_position):
  data = None
  if seek_position != 0:
    data = load_last_stored_data()
  if data is None:
    data = {
      "sites":       {},
      "message_ids": set([])
    }

  return data


def init_site():
  return {
    "operator_activity": [],
    "unique_operators":  set([]),
    "unique_visitors":   set([]),
    "message_activity":  {},

    "stats": {
      "messages":         0,
      "emails":           0,
      "unique_operators": 0,
      "unique_visitors":  0
    }
  }
#===============================================================================

if __name__ == "__main__":
  main()
