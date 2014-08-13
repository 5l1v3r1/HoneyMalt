#!/usr/bin/env python

from common.dbconnect import db_connect
from common.entities import KippoSession
from canari.maltego.message import Label, Field, UIMessage
from canari.maltego.entities import URL
from canari.config import config
from canari.framework import configure #, superuser

__author__ = 'catalyst256'
__copyright__ = 'Copyright 2014, Honeymalt Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'catalyst256'
__email__ = 'catalyst256@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform',
    'onterminate'
]

#@superuser
@configure(
 label='HoneyMalt: Kippo Files',
 description='Get Kippo files based on sessions',
 uuids=[ 'HoneyMalt.v2.Kippo_2_File' ],
 inputs=[ ( 'HoneyMalt', KippoSession ) ],
 debug=False
)
def dotransform(request, response, config):
  sess = request.value
  host = request.fields['kippoip']
  x = db_connect(host)
  cursor = x.cursor()
  query = ("select timestamp, url, `outfile` from downloads where session like %s")
  cursor.execute(query, (sess,))
  for timestamp, url, outfile in cursor:
    e = URL(url)
    e.url = url
    e += Field('filetime', timestamp, displayname='Time Stamp')
    e += Field('fileout', outfile, displayname='Success')
    e += Field('kippoip', host, displayname='Kippo IP')
    response += e
  return response

def onterminate():
  cursor.close()
  x.close()
  exit(0)