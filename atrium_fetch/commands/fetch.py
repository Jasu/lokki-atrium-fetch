import urllib
import http.client
from pprint import pprint
import json
import math
import os
import subprocess

import oauthlib.oauth1

from atrium_fetch.util import dieIf, expandEnvironmentVariables
from atrium_fetch.db.profile import Profile
from atrium_fetch.db.setting import Setting

def _getSetting(session, name):
  setting = session.query(Setting).filter_by(name=name).first()
  dieIf(not setting, 'Setting ' + name + ' not set.')
  return setting.value

def _request(connection, url, headers, body):
  if body:
    method = 'POST'
  else:
    method = 'GET'
  url_parsed = urllib.parse.urlparse(url)
  path = urllib.parse.urlunparse([
    '',
    '',
    url_parsed.path,
    url_parsed.params,
    url_parsed.query,
    ''
  ])
  connection.request(method, path, body, headers)
  response = connection.getresponse()
  dieIf(response.status != 200, 
    "Request to " + url + " failed: " + str(response.status) + " " 
    + response.reason)
  return response.read().decode('utf-8')

def _invokeLokki(profile, commandLine, isJson=True):
  env = os.environ.copy()
  env['LK_DB_PATH'] = expandEnvironmentVariables(profile.lokki_db)
  output = subprocess.check_output(commandLine, env=env).decode('utf-8')
  if isJson:
    return json.loads(output)
  else:
    return output

def _createInvoice(profile):
  result = _invokeLokki(profile, [
    'lk',
    'invoice',
    'add',
    '--json',
  ])

  dieIf('invoice' not in result, 'Failed to create invoice.')
  dieIf('invoice_number' not in result['invoice'], 'Failed to create invoice.')

  return result['invoice']['invoice_number']


def _addCompositeRow(profile, invoiceNumber, title):
  result = _invokeLokki(profile, [
    'lk',
    'composite',
    'add',
    '--json',

    '--external_source',
    'atrium-fetch',

    title,
  ])

  dieIf('index' not in result, 'Failed to create composite row.')

  return result['index']

def _addSubrow(profile, 
               invoiceNumber, 
               rowIndex, 
               node_id, 
               title, 
               units):

  cmd = [
    'lk',
    'subrow',
    'add',
    
    '--row',
    str(rowIndex),

    '--external_source',
    'atrium-fetch',

    '--external_id',
    str(node_id),
  ]

  if invoiceNumber:
    cmd += [
      '--invoice_number',
      str(invoiceNumber)
    ]

  cmd += [
    title,
    str(profile.price_per_hour),
    str(units)
  ]

  result = _invokeLokki(profile, cmd, isJson=False)

def _getAddedSubrows(profile):

  cmd = [
    'lk',
    'external',
    'subrows',

    '--json',

    '--external_source',
    'atrium-fetch',
  ]

  return _invokeLokki(profile, cmd)


def commandFetch(args, session):
  profile = (session.query(Profile)
             .filter_by(handle=args.profile_handle)
             .first())

  oauth_key = _getSetting(session, 'oauth_key')
  oauth_secret = _getSetting(session, 'oauth_secret')
  baseurl = _getSetting(session, 'baseurl')
  baseurl_parsed = urllib.parse.urlparse(baseurl)
  connection = http.client.HTTPConnection(baseurl_parsed.netloc)

  oauth_client = oauthlib.oauth1.Client(oauth_key, client_secret=oauth_secret)

  viewUrl = urllib.parse.urljoin(baseurl + '/', profile.endpoint) + '/'
  viewUrl = urllib.parse.urljoin(viewUrl, 'views') + '/'
  viewUrl = urllib.parse.urljoin(viewUrl, profile.view_name) 
  if profile.display_name:
    viewUrl = urllib.parse.urljoin(viewUrl, '?display_id='+profile.display_name)

  uri, headers, body = oauth_client.sign(viewUrl)
  response = _request(connection, uri, headers, body)
  data = json.loads(response)

  if args.invoice_number:
    invoiceNumber = args.invoice_number
  elif args.create_invoice:
    invoiceNumber = _createInvoice(profile)
  else:
    invoiceNumber = None

  compositeRows = {}
  addedSubrows = _getAddedSubrows(profile)
  for row in data:
    if row['id'] not in addedSubrows:
      if row['project_id'] not in compositeRows:
        compositeRows[row['project_id']] = _addCompositeRow(profile, 
                                                         invoiceNumber,
                                                         row['project_title'])

      _addSubrow(profile,
                 invoiceNumber,
                 compositeRows[row['project_id']],
                 row['id'],
                 row['title'],
                 math.ceil(float(row['hours'])))
