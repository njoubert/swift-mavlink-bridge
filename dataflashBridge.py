'''

Requirements:

  pip install mavlink

'''
from pymavlink.DFReader import *

filename = "60.BIN"

'''
This function takes in a filename for a ArduPilot dataflash log, 
and returns an array of (timestamp, bytearray) tuples.
The bytearray contains raw SBP binary data logged directly from the serial port.
Each tuple should contain exactly one SBP message if I did this right!
'''
def extractSBP(filename):
  extractedData = []

  log = DFReader_binary(filename)
  last_m = None

  while True:
    m = log.recv_match(type=['SBR1', 'SBR2'])
    if m is None:
        break

    bin_data = None
    timestamp = None
    msg_type = None
    sender_id = None
    msg_len = None

    if last_m != None and last_m.get_type() == 'SBR1' and m.get_type() == 'SBR2':
      #append the two
      bin_len = last_m.msg_len
      timestamp = getattr(last_m, '_timestamp', 0.0)
      bin_data = bytearray((last_m.d1 + m.d2 + m.d3 + m.d4)[0:bin_len])
      msg_type = last_m.msg_type
      sender_id = last_m.sender_id
      msg_len = last_m.msg_len


    elif last_m != None and last_m.get_type() == 'SBR1' and m.get_type() == 'SBR1':
      #extract the last one, save this one
      bin_len = last_m.msg_len
      timestamp = getattr(last_m, '_timestamp', 0.0)
      bin_data = bytearray((last_m.d1)[0:bin_len])
      msg_type = last_m.msg_type
      sender_id = last_m.sender_id
      msg_len = last_m.msg_len
      last_m = m

    else:
      #just save this one
      last_m = m

    if bin_data != None:
      extractedData.append((timestamp, msg_type, sender_id, msg_len, bin_data))
  return extractedData
    

print extractSBP(filename)
