import concurrent.futures
import logging
import queue
import sys
import threading
from Cris_HorseRaces.Threading import meetingResultsToExcell, getMeetings

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if len(sys.argv) > 1:
    #Get address from command line.
    #print('raw ',sys.argv)
    address = ' '.join(sys.argv[1:])
    runtime_parm_entered = True
    #print(type(address))
    #print('Address is ',address)
    address_parts = []
    address_parts = address.split("&")
    #print(address_parts[1])
else:
    address = "https://cris.rwwa.com.au/meeting.aspx?meeting=5159078"

pipeline = queue.Queue(maxsize=10)
event = threading.Event()
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(getMeetings, pipeline, event, address)
        executor.submit(meetingResultsToExcell, pipeline, event)
        event.set()
logging.info("Finished updating excel sheet: Horse Race.xlsx")