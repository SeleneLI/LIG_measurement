#! /usr/bin/python3

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.append('/var/www/html/looking_glass/')
sys.path.append('/usr/local/lib/python3.4/dist-packages/') 

from lg import app as application
