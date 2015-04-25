import os, cPickle, time, shutil

tmp_dir         = ".homeworktmp"
sincedb_file    = "%s/%s" % (tmp_dir, ".last_processed")
cache_file      = "%s/%s" % (tmp_dir, ".site_data")

#= State Save and Load =========================================================
def clear_cache():
  shutil.rmtree(tmp_dir)
  
def save_position(seek_position):
  with open(sincedb_file, "w+") as f:
    f.write("%d\n" % seek_position)


def save_stats(data):
  # Write to temp file
  temp_name = "%s%d" % (cache_file, int(time.time()))
  with open(temp_name, "wb") as f:
    cPickle.dump(data, f, 2)

  # Place in final save location
  if os.path.exists(cache_file):
    os.remove(cache_file)
  os.rename(temp_name, cache_file)


def load_last_processed_position():
  last_read = 0
  if os.path.isfile(sincedb_file):
    with open(sincedb_file, "r") as f:
      try:
        last_read = int(f.read())
      except ValueError as err:
        pass

  return last_read


def load_last_stored_data():
  if os.path.exists(cache_file):
    with open(cache_file, "rb") as f:
      data = cPickle.load(f)
    return data
  else:
    return None
#===============================================================================
