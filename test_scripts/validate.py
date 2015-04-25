file_one = "output_data/my_big_output"
file_two = "output_data/big_output"

passes = 0
site_fails = 0
messages_fails = 0
emails_fails = 0
operators_fails = 0
visitors_fails = 0

def parse_line(line):
  data              = {}
  d                 = line.split(",")
  data["site"]      = int(d[0])
  data["messages"]  = int(d[1].split("=")[1]) 
  data["emails"]    = int(d[2].split("=")[1]) 
  data["operators"] = int(d[3].split("=")[1]) 
  data["visitors"]  = int(d[4].split("=")[1]) 
  return data

with open(file_one, "r") as f1, open(file_two, "r") as f2:
  for line_one in f1:
    line_two = f2.readline()
    d1 = parse_line(line_one)
    d2 = parse_line(line_two)

    fails = []
    if d1["site"] != d2["site"]:
      fails.append( "Mismatched Sites: %s and %s" % (d1["site"], d2["site"]) )
      site_fails += 1

    if d1["messages"] != d2["messages"]:
      fails.append( "Mismatched Messages: %s and %s" % (d1["messages"], d2["messages"]) )
      messages_fails += 1
    
    if d1["emails"] != d2["emails"]:
      fails.append( "Mismatched Emails: %s and %s" % (d1["emails"], d2["emails"]) )
      emails_fails += 1

    if d1["operators"] != d2["operators"]:
      fails.append( "Mismatched Operators: %s and %s" % (d1["operators"], d2["operators"]) )
      operators_fails += 1

    if d1["visitors"] != d2["visitors"]:
      fails.append( "Mismatched Visitors: %s and %s" % (d1["visitors"], d2["visitors"]) )
      visitors_fails += 1

    if len(fails) > 0:
      print "- Test Fail -"
      for failure in fails:
        print failure
        print " Source:", line_one.rstrip()
        print " Target:", line_two.rstrip()
        print " "
      print "-           -"
    else:
      passes += 1


if site_fails > 0:
  print "Site Failures: %d" % site_fails

if messages_fails > 0:
  print "Messages Failures: %d" % messages_fails

if emails_fails > 0:
  print "Emails Failures: %d" % emails_fails

if operators_fails > 0:
  print "Operators Failures: %d" % operators_fails

if visitors_fails > 0:
  print "Visitors Failures: %d" % visitors_fails

print "Passes: %d" % passes
#1,messages=4,emails=4,operators=2,visitors=5
