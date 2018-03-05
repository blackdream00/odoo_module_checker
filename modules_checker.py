#!/usr/bin/env python
import psycopg2
import os
import getpass
from optparse import OptionParser
#
# comando:  python modules_checker.py /opt/openerp/v10/extra_addons,/opt/openerp/v10/10cq/addons,/opt/openerp/v10/10cq/odoo/addons/ -D test10zero1 -U openerp -H localhost
# i parametri sono:
#   la/le cartelle di addons con path completo separate da virgole senza spazi
#   -D database da controllare
#   -U utente postgres
#   -H indirizzo del server
# chiede la password dell'utente postgres e stampa a video l'elenco dei moduli che non ci sono in locale, inoltre
#   crea il file testcmdpull con le pull di tutti i moduli installati nel database e presenti in locale
#
parser = OptionParser()
parser.add_option("-D", "--database", dest="database",metavar="hydronit2018",
                  help="Choose Postgres database name")
parser.add_option("-U", "--user", dest="user",metavar="hydronit",
                  help="Choose Postgres database user")
parser.add_option("-H", "--host", dest="hostname",metavar="cq-server-ubuntu",
                  help="Choose Postgres database hostname")
parser.add_option("-B", "--branch", dest="branches",metavar="master",
                  help="All branches (all) or Master only (master)")

optlist, args = parser.parse_args()
if len(args) <1:
	errmsg='This programs needs the addons folder path as a command line argument'
	raise SyntaxError(errmsg)
	

db_name=optlist.database
db_user=optlist.user
host=optlist.hostname
if optlist.branches:
	whichb = optlist.branches
else:
	whichb = 'master'
addons_path=args[0].split(",")
try:
# connessione di default con autenticazione peer, da provare
    conn = psycopg2.connect("dbname='%s'" % db_name)
    print "OK connessione peer"
except:
# connessione con password se non ha funzionato la precedente
    password=getpass.getpass('Enter password for user \x1b[1;36;40m%s\x1b[0m\n' % (db_user) )
    conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (db_name,db_user,host,password) )
cur=conn.cursor()
#cur.execute("SELECT name from ir_module_module WHERE state='installed' and name != 'base' and name not ilike 'web%';")
cur.execute("SELECT name from ir_module_module WHERE state='installed' or state='to upgrade';")
rows=cur.fetchall()
db_modules=[]
for row in rows:
	db_modules.append(row[0])
#modules_on_drive= os.listdir(addons_path)
#modules_on_drive.append('base')
#posso avere varie cartelle di addons
modules_on_drive=[]
modules_to_pull=[]
peroutp = ' > /tmp/gitout.txt 2>&1'
for ppath in addons_path:
	modules_on_drive.extend(os.listdir(ppath))
	tmp=os.listdir(ppath)
        for t in tmp:
		if t in db_modules:
                        if whichb == 'all':
				modules_to_pull.extend(['cd '+ppath+'/'+t,'git pull -v'+peroutp])
			else:
				modules_to_pull.extend(['cd '+ppath+'/'+t,'git pull -v origin '+whichb+peroutp])
			peroutp = ' >> /tmp/gitout.txt 2>&1'

modules_on_drive=set(modules_on_drive)
db_modules=set(db_modules)
missing = db_modules - modules_on_drive
print 'The database \033[92m%s\033[0m has %d modules installed\nYour hard drive contains %d modules' % (db_name,len(db_modules),len(modules_on_drive))
if len(missing):
	print 'The following modules are installed in the database \033[92m%s\033[0m but are missing from your hard drive:\n' % (db_name)
	for i in missing:
		print i
else:
	print 'You have all the required modules to run database \033[92m%s\033[0m' % (db_name)

conn.close()
f1=open('./testcmdpull', 'w+')
print>>f1,"git config --global credential.helper cache"
for i in modules_to_pull:
	print>>f1, i
