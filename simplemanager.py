# encoding: utf-8

import gvsig

from gvsig import getResource

import os.path
import re

from org.gvsig.tools.identitymanagement.impl import DumbIdentityManager, DumbIdentity
from org.gvsig.tools import ToolsLocator
from org.gvsig.tools.locator import LocatorObjectFactory
from org.gvsig.tools.identitymanagement import UnauthorizedException

from java.util import Properties
from java.io import FileInputStream
from java.io import File

class SimpleUser(DumbIdentity):
  def __init__(self,id, props):
    DumbIdentity.__init__(self,id)
    self.props = props
    
  def getPassword(self):
    return str(self.props.getProperty("attr.password"))
    
  def isAuthorized(self, actionName, resource=None, resourceName=None):
    value = self.props.getProperty("action."+actionName)
    if value == None :
      param_name = self.props.getProperty("action."+actionName+".parameter.name")
      if param_name == None:
        return True
      value_pattern = self.props.getProperty("action."+actionName+".parameter.pattern")
      if value_pattern == None:
        return True
      if param_name == "file": # Este es un caso especial.
        value = resource.getFile().getAbsolutePath()
      else:
        value = resource.getDynValue(param_name)
      match = re.match(value_pattern, value)
      if match!=None:
        return False
      return True

    if value.lower() == "false":
      return False
   
class SimpleUserManager(DumbIdentityManager):
  def __init__(self):
    DumbIdentityManager.__init__(self)
    self.current = None
    self.login(None,"guest","")

  def login(self, domain, userid, password):
    fis = None
    userinfo = getResource(__file__,"users_db",userid+".properties")
    if not os.path.exists(userinfo):
      raise UnauthorizedException("login",userid,userid)
    props = Properties()
    try:
      fis = FileInputStream(File(userinfo))
      props.load(fis)
    finally:
      fis.close()
    DumbIdentityManager.login(self, domain,userid,password)
    user = SimpleUser(userid, props)
    if user.getPassword() != password :
        raise UnauthorizedException("login",userid,userid)
    self.current = user

  def getCurrentIdentity(self):
    return self.current
    
class SimpleUserManagerFactory(LocatorObjectFactory):
  def create(self,*args):
    return SimpleUserManager()

def selfRegister():
  ToolsLocator.getInstance().register(
    ToolsLocator.IDENTITY_MANAGER_NAME,
    SimpleUserManagerFactory()
  )
  
def main():
  selfRegister()
  pass
  
