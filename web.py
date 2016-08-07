from flask import Flask,render_template
import couchdb,_mysql,sys,csv

db = couchdb.Server()['huginn-events']

csvfile = open('default.cfg')
reader = csv.DictReader(csvfile)
creds = list(reader)[0]
mdb = _mysql.connect(creds['host'],creds['username'],creds['password'],creds['database'])

app = Flask(__name__)

@app.route("/")
def index():
	mdb.query('select * from headlines order by date desc limit 10')
	r = mdb.store_result()
	rows = r.fetch_row(10,how=1)
	o = [row for row in rows]
	return render_template('index.html',content=o,delay=5)

@app.route("/doc/<key>")
def doc(key=None):
	doc = db[key]
	return render_template('detailed.html',doc=doc)

def web_main():
	try:
		app.run(host="0.0.0.0")
	except KeyboardInterrupt:
		sys.exit()

if __name__ == "__main__":
	web_main()