#!/usr/bin/env python
import os
os.system('rsync -arv --delete --password-file=/etc/rsyncd.passwd /bdata/http/ fortress@10.1.20.116::fortress_bdata; rsync -arv --delete --password-file=/etc/rsyncd.passwd /home/ fortress@10.1.20.116::fortress_home')
print 'RSYNC_SUCCESS'
