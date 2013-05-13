from atrium_fetch.db.setting import Setting

def commandConfigSet(args, session):
  setting = session.query(Setting).filter_by(name=args.setting_name).first()

  if (not setting):
    setting = Setting()
    setting.name = args.setting_name
    session.add(setting)

  setting.value = args.setting_value

  session.commit()
  print("Set " + setting.name + "=" + setting.value +".")

def commandConfigGet(args, session):
  setting = session.query(Setting).filter_by(name=args.setting_name).first()
  if (not setting):
    print ("Setting was not found.")
  else:
    print (setting.value)

def commandConfigList(args, session):
  for setting in session.query(Setting).order_by(Setting.name): 
    print (setting.name + "=" + setting.value)
