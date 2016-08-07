from threading import Thread
from database import database_main
from web import web_main
import sys

def help():
	o = ""
	o += "Usage for run.py:\n"
	o += "	-r: Run with all modules enabled\n"
	o += "	-h: Return this documentation\n"
	o += "	-d: Run with only database\n"
	o += "	-w: Run with only web\n"
	print o

def argProcess():
	argv = sys.argv
	print argv
	if len(argv) >= 2:
		if argv[1] == "-h":
			return 1
		elif argv[1] == "-d":
			return 2
		elif argv[1] == "-w":
			return 3
		elif argv[1] == "-r":
			return 0
		else:
			return 9
	else:
		return -1

webThread = Thread(target=web_main)
dbThread = Thread(target=database_main)

if __name__ == "__main__":
	a = argProcess()
	print a
	try:
		if a == 0:
			webThread.start()
			dbThread.start()
		elif a == 1 or a == 9 or a == -1:
			help()
		elif a == 2:
			dbThread.start()
		elif a == 3:
			webThread.start()
	except KeyboardInterrupt:
		webThread.stop()
		dbThread.stop()