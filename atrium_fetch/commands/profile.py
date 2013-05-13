from atrium_fetch.db.profile import Profile
from atrium_fetch.util import dieIf

from prettytable import PrettyTable

def commandProfileAdd(args, session):
  profile = Profile()
  profile.handle = args.handle
  profile.lokki_db = args.lokki_db

  session.add(profile)
  session.commit()

  print ("Added profile '" + profile.handle + "'.")

def commandProfileRemove(args, session):
  profile = session.query(Profile).filter_by(handle=args.handle).first()
  dieIf(not profile, 'Profile not found.')

  session.delete(profile)
  session.commit()

def commandProfileSet(args, session):
  profile = session.query(Profile).filter_by(handle=args.handle).first()
  dieIf(not profile, 'Profile not found.')
  dieIf(not hasattr(profile, args.setting_name), 'Setting does not exist.')
  setattr(profile, args.setting_name, args.setting_value)
  session.commit()
  print('Set ' + args.setting_name + '=' + args.setting_value)

def commandProfileGet(args, session):
  profile = session.query(Profile).filter_by(handle=args.handle).first()
  dieIf(not profile, 'Profile not found.')
  dieIf(not hasattr(profile, args.setting_name), 'Setting does not exist.')
  print(getattr(profile, args.setting_name))

def commandProfileList(args, session):
  profiles = session.query(Profile).order_by(Profile.handle)

  table = PrettyTable(['Handle', 'Database'])
  table.align['Handle'] = 'r'
  table.align['Database'] = 'l'

  for profile in profiles:
    table.add_row([profile.handle, profile.lokki_db])

  print(table)
    

