from threading import Thread
from database import database_main
from web import web_main
import sys

webThread = Thread(target=web_main)
dbThread = Thread(target=database_main)

if __name__ == "__main__":
	webThread.start()
	dbThread.start()
	except KeyboardInterrupt:
		webThread.stop()
		dbThread.stop()