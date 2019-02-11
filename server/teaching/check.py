import re
class Check:
  @staticmethod
  def username(param):
    if not ('username' in param):
      return 10401

    username = param['username']
    username = re.sub(r'\s+', '', username, count=0)
    username_len = len(username)

    if username_len < 6:
      return 10402
    elif username_len > 30:
      return 10403

    if not re.match(r'^[a-zA-Z0-9]{6,30}$', username):
      return 10404

    return False

  @staticmethod
  def password(param):
    if not ('password' in param):
      return 10405

    password = param['password']
    password = re.sub(r'\s+', '', password, count=0)
    password_len = len(password)

    if password_len < 6:
      return 10406
    elif password_len > 20:
      return 10407

    if not re.match(r'^\S{6,20}$', password):
      return 10408

    return False

  @staticmethod
  def code(param):
    if not ('code' in param):
      return 10409

    code = param['code']
    code = re.sub(r'\s+', '', code, count=0)
    code_len = len(code)

    if code_len < 4:
      return 10410
    elif code_len > 4:
      return 10411
    
    if not re.match(r'^[a-zA-Z0-9]{4}$', code):
      return 10412

    return False
