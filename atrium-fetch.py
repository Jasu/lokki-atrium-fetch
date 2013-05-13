#!/usr/bin/python

import os
import sys
import argparse
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from atrium_fetch.commands.init import commandInit
from atrium_fetch.commands.shell import commandShell

from atrium_fetch.commands.config import (
  commandConfigSet, 
  commandConfigGet, 
  commandConfigList
  )

from atrium_fetch.commands.profile import (
  commandProfileAdd, 
  commandProfileRemove, 
  commandProfileSet, 
  commandProfileGet, 
  commandProfileList
  )

from atrium_fetch.commands.fetch import commandFetch


commandLineParser = argparse.ArgumentParser(
                      description='AF - Fetch from Atrium to Lokki')

subcommandParsers = commandLineParser.add_subparsers(
                      title='Subcommands',
                      description='valid subcommands')

###############################################################################
# COMMAND shell                                                               #
###############################################################################

shellSubcommandParser = subcommandParsers.add_parser('shell')
shellSubcommandParser.set_defaults(func=commandShell)
shellSubcommandParser.add_argument('db_path', help='SQLite database to use.')

###############################################################################
# COMMAND init                                                                #
###############################################################################

initSubcommandParser = subcommandParsers.add_parser('init')
initSubcommandParser.set_defaults(func=commandInit)
initSubcommandParser.add_argument('db_path', 
  help='SQLite database to init. The file must not exist.')

###############################################################################
# COMMAND config                                                              #
###############################################################################

configSubcommandParser = subcommandParsers.add_parser('config')
configSubcommandSubParsers = configSubcommandParser.add_subparsers(
                                title='Configuration commands')

configSetSubcommandParser = configSubcommandSubParsers.add_parser('set')
configSetSubcommandParser.set_defaults(func=commandConfigSet)
configSetSubcommandParser.add_argument('setting_name', help='Setting name')
configSetSubcommandParser.add_argument('setting_value', help='Setting value')

configGetSubcommandParser = configSubcommandSubParsers.add_parser('get')
configGetSubcommandParser.set_defaults(func=commandConfigGet)
configGetSubcommandParser.add_argument('setting_name', help='Setting name')

configListSubcommandParser = configSubcommandSubParsers.add_parser('list')
configListSubcommandParser.set_defaults(func=commandConfigList)

###############################################################################
# COMMAND profile
###############################################################################

profileSubcommandParser = subcommandParsers.add_parser('profile')
profileSubcommandSubParsers = profileSubcommandParser.add_subparsers(
                                title='profile commands')

profileAddSubcommandParser = profileSubcommandSubParsers.add_parser('add')
profileAddSubcommandParser.set_defaults(func=commandProfileAdd)
profileAddSubcommandParser.add_argument('handle', help='Profile handle')
profileAddSubcommandParser.add_argument('lokki_db', help='Path to Lokki database')

profileRemoveSubcommandParser = profileSubcommandSubParsers.add_parser('remove')
profileRemoveSubcommandParser.set_defaults(func=commandProfileRemove)
profileRemoveSubcommandParser.add_argument('handle', help='Profile handle')

profileSetSubcommandParser = profileSubcommandSubParsers.add_parser('set')
profileSetSubcommandParser.set_defaults(func=commandProfileSet)
profileSetSubcommandParser.add_argument('handle', help='Profile handle')
profileSetSubcommandParser.add_argument('setting_name', help='Setting name')
profileSetSubcommandParser.add_argument('setting_value', help='Setting value')

profileGetSubcommandParser = profileSubcommandSubParsers.add_parser('get')
profileGetSubcommandParser.set_defaults(func=commandProfileGet)
profileGetSubcommandParser.add_argument('handle', help='Profile handle')
profileGetSubcommandParser.add_argument('setting_name', help='Setting name')

profileListSubcommandParser = profileSubcommandSubParsers.add_parser('list')
profileListSubcommandParser.set_defaults(func=commandProfileList)

###############################################################################
# COMMAND fetch                                                               #
###############################################################################

fetchSubcommandParser = subcommandParsers.add_parser('fetch')
fetchSubcommandParser.set_defaults(func=commandFetch)
fetchSubcommandParser.add_argument('profile_handle', help='Profile handle')
fetchSubcommandParser.add_argument('--invoice_number', 
                                  help='Invoice number. If not provided, a '
                                       'the most recent invoice is used.',
                                  required=False)
fetchSubcommandParser.add_argument('--create_invoice', 
                                  help='Create a new Lokki invoice.',
                                  required=False,
                                  action='store_true')

###############################################################################
# Connect to database                                                         #
###############################################################################

db = None
session = None
if 'AF_DB_PATH' in os.environ:
  db = sqlalchemy.create_engine('sqlite:///' + os.environ['AF_DB_PATH'])
  session = sessionmaker(bind=db, autoflush=False)()

###############################################################################
# Invoke the command                                                          #
###############################################################################

arguments = commandLineParser.parse_args()
if ('func' in arguments):
  arguments.func(arguments, session)
else:
  commandLineParser.print_help()

