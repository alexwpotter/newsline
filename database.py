import _mysql,couchdb,csv
from data_match import bag_compare,handle

couch = couchdb.Server()

csvfile = open('default.cfg')
reader = csv.DictReader(csvfile)
creds = list(reader)[0]
db = _mysql.connect(creds['host'],creds['username'],creds['password'],creds['database'])

def search():
	db.query("""
		select * from headlines order by date desc limit 10
	""")
	r = db.store_result()
	rows = r.fetch_row(10,how=1)
	if len(rows) > 0:
		return rows
	else:
		return []

def db_store(table):
	ids = []
	out = []
	q = "insert into headlines (bag, count, date, headline, couch_id) values {} on duplicate key update count=count+1"
	tabl = lambda x: '("'+'", "'.join([str(item) for item in [x['bag'],1,x['date'],x['original'],x['id']]])+'")'
	tbl = [tabl(row) for row in table]
	qu = q.format(', '.join(tbl))
	#print qu
	db.query(qu)

def bag_join(bags1,bags2):
	out = []
	if len(bags1) > 0 and len(bags2) > 0:
		for bag1 in bags1:
			for bag2 in bags2:
				if bag_compare(bag1,bag2):
					out.append(bag1)
				else:
					out.append(bag2)
		return out
	else:
		if len(bags1) > 0:
			return bags1
		else:
			return bags2


def docs_to_bags(docs):
	#print docs
	bags = handle(docs)
	return bags

def poll(database,callback):
	ch = database.changes(feed='continuous',heartbeat=10000)
	a = []
	for line in ch:
		a.append(line)
		if len(a) > 9:
			print "Execute"
			callback(a)
			a = []

def database_process(cb):
	old_bags = search()
	new_bags = docs_to_bags(cb)
	#print old_bags,new_bags
	join = bag_join(old_bags,new_bags)
	#print join
	db_store(join)
	print "Done"

def database_main():
	print "Polling database"
	poll(couch['huginn-events'],database_process)

if __name__ == "__main__":
	database_main()