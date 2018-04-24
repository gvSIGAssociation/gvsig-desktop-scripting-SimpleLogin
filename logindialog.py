# encoding: utf-8

import gvsig
from gvsig.commonsdialog import msgbox
from gvsig.libs.formpanel import FormPanel
from org.gvsig.tools import ToolsLocator
from java.lang import System
import sys

from addons.CoordinateCapture.patchs.fixformpanel import fixFormPanelResourceLoader

class LoginDialog(FormPanel):
  def __init__(self):
    FormPanel.__init__(self)
    self.load((__file__, "logindialog.xml"))
    self.setPreferredSize(640,400)
    self._cancelled = True

  def btnLogin_click(self,*args):
    userid = self.cboUserName.getSelectedItem()
    if userid == None:
      msgbox("Entry a user identifier")
      return
    userid=str(userid)
    password = self.txtPassword.getText()
    manager = ToolsLocator.getIdentityManager()
    try:
      manager.login(None,userid,password)
    except :
      msgbox("Login failed, retry")
      return
    self._cancelled = False
    self.hide()

  def btnCancel_click(self,*args):
    self.hide()

  def cancelled(self):
    return self._cancelled

def login():
  fixFormPanelResourceLoader()
  
  login = LoginDialog()
  login.showDialog("Login")
  if login.cancelled():
    System.exit(1)

def main(*args):
  fixFormPanelResourceLoader()
  
  login = LoginDialog()
  login.showWindow("Login")

