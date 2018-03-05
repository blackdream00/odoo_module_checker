this code is a designed for Odoo in order to check the modules, creates a testcmdpull file with the pulls of all the modules installed in a odoo database and present locally in the addons folders.
It also writes a list of possible modules installed in the database but not present locally.

The command to use is:
python modules_checker.py  "add-on folders" -D "database" -U "postgres user" -H "server address"

The parameters are:
   the addons folder with a full path separated by commas with no spaces like / opt / openerp / v10 / extra_addons, / opt / openerp / v10 / 10cq / addons, / opt / openerp / v10 / 10cq / odoo / addons /
   - D database to check
   - U user postgres
   - H server address


Then you have to make testcmdpull executable:

chmod + x testcmdpull

and launch it:

./testcmdpull

The first time you run a git pull command, it asks for the git user password, then should not ask for it anymore.

The output of git is directed to a file: /tmp/gitout.txt examining it you see what has been updated and if there have been errors

===============================

The pull_all_modules.sh script executes the 'git pull' command for all subfolders in a folder.
It should be copied to the folder containing the extra_addons and started (giving it execution permissions).
