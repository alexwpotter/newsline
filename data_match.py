import couchdb,string,nltk,os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tag import StanfordPOSTagger
db = couchdb.Server()['huginn-events']
stop = stopwords.words('english')
wnl = WordNetLemmatizer().lemmatize
stem = PorterStemmer().stem

os.environ['CLASSPATH'] = ':'.join(["/usr/share/stanford-ner-2015-12-09/",
									"/usr/share/stanford-postagger-2015-12-09/",
									"/usr/share/stanford-parser-full-2015-12-09/"])

os.environ['STANFORD_MODELS'] = ':'.join(["/usr/share/stanford-ner-2015-12-09/classifiers",
										  "/usr/share/stanford-postagger-2015-12-09/models",
										  "/usr/share/stanford-parser-full-2015-12-09/"])

NewsKeys = [
	"last_updated"
]

ScannerKeys = [
	"time",
	"address"
]

table = []

def parse_event(e):
	table.append({
		"original": [e['orig']],
		"bag": e['text'],
		"id": [e['id']],
		"date": e['date']
		})

def bag_compare(b1,b2,limit=3):
	l1 = len(set(list(iter(b1))+list(iter(b2))))
	l2 = len(b2)+len(b1)
	return l1 < l2-limit

def table_parse():
	for i1 in table:
		for i2 in table:
			if bag_compare(i1['bag'],i2['bag']):
				i1['id'].append(i2['id'][0])
				i1['original'].append(i2['original'][0])

def pretty_table(t):
	o = []
	minimum = 3
	for row in table:
		if len(row['id']) > minimum:
			o.append({
				"headlines": row['original'],
				"bags": row['bag'],
				"ids": row['id']
				})
	return o

st = StanfordPOSTagger('english-bidirectional-distsim.tagger')

def destem_stanford(txt):
	tag = st.tag(txt)
	o = []
	for word in tag:
		pos = word[1][:1]
		if pos == "N" or pos == "V":
			w = wnl(word[0],pos=pos.lower())
			o.append(w)
		else:
			o.append(stem(word[0]))
	return o

def vectorize(l):
	k = set(l)
	o = {}
	for item in k:
		o[item] = 0
	for item in l:
		o[item] += 1
	return o

def clean_text(txt,id,date):
	tbl = string.maketrans(string.punctuation,' '*len(string.punctuation)) 
	txt = string.translate(txt.encode('ascii'),tbl)
	rem = [i for i in txt.lower().split() if i not in stop]
	de = destem_stanford(rem)
	return {"orig": txt, "text": vectorize(de), "id": id, "date": date}

def clean_scanner(txt):
	x = ' '.join(txt.strip().split(' ')[1:])
	if x[0] in string.uppercase:
		return x[:-3]
	else:
		return x[1:-2]
def data():
	for row in db.view('_all_docs'):
		doc = db[row.id]
		doc_keys = list(iter(doc))
		#print doc
		if len(set(doc_keys+NewsKeys)) == len(doc_keys):
			parse_event(clean_text(doc['title'],doc.id))	
		elif len(set(doc_keys+ScannerKeys)) == len(doc_keys):
			pass

def handle(dat):
	for row in dat:
		doc = db[row['id']]
		doc_keys = list(iter(doc))
		#print doc
		if len(set(doc_keys+NewsKeys)) == len(doc_keys):
			parse_event(clean_text(doc['title'],doc.id,doc['date_published']))	
		elif len(set(doc_keys+ScannerKeys)) == len(doc_keys):
			pass
	return table

if __name__ == "__main__":
	data()
	table_parse()
	print pretty_table(table)
	#clean_text("He threw the thrown object")