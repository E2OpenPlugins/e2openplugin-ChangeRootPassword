#Graphics by Army


from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.VirtualKeyBoard import VirtualKeyBoard

from Components.ActionMap import ActionMap
from Components.config import config, ConfigText, ConfigSubsection, getConfigListEntry, NoSave
from Components.ConfigList import ConfigListScreen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Plugins.Plugin import PluginDescriptor
from random import Random 
from telnetlib import Telnet
import string


class SetPasswdMain(Screen, ConfigListScreen):
	skin = """
		<screen position="center,center" size="800,600" title="Set Root Password" flags="wfNoBorder" >
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ChangeRootPassword/backg.png" position="0,0" size="800,600" alphatest="on" />
		<widget name="config" position="100,200" zPosition="1" size="600,60" scrollbarMode="showOnDemand" transparent="1" />
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.skin = SetPasswdMain.skin
		self.list = []
		ConfigListScreen.__init__(self, self.list)
		
		self["key_red"] = Label(_("Set Password"))
		self["key_green"] = Label(_("Generate"))
		self["key_yellow"] = Label(_("Virtual Keyb"))
		self["key_blue"] = Label(_("Cancel"))

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
		{
			"red": self.DoConnectPass,
			"green": self.greenPressed,
			"yellow": self.yellowPressed,
			"blue": self.close,
			"cancel": self.close
		}, -1)
	
		self.newpass = self.buildPass()
		self.oldp = NoSave(ConfigText(fixed_size = False, default = ""))
		self.newp = NoSave(ConfigText(fixed_size = False, default = self.newpass))
		self.updateList()
	
	def updateList(self):
		self.list = []
		self.list.append(getConfigListEntry('Enter old Password', self.oldp))
		self.list.append(getConfigListEntry('Enter new Password', self.newp))
		self["config"].list = self.list
		self["config"].l.setList(self.list)
		
	def buildPass(self):
		passwd = string.ascii_letters + string.digits
		return ''.join(Random().sample(passwd, 8)) 

	def greenPressed(self):
		self.newp.value = self.buildPass()
		self.updateList()
		
	def yellowPressed(self):
		sel = self["config"].getCurrent()
		value = self.oldp.value
		self.valuetype = 0
		if sel[0] == "Enter new Password":
			value = self.newp.value
			self.valuetype = 1
		self.session.openWithCallback(self.virtualKeybDone, VirtualKeyBoard, title=sel[0], text=value)
		
	
	def virtualKeybDone(self, passw):
		if self.valuetype == 0:
			self.oldp.value = passw
		else:
			self.newp.value = passw
		self.updateList()

	def DoConnectPass(self):
		self.session.open(SetPasswdDo, self.oldp.value, self.newp.value)


class SetPasswdDo(Screen):
	skin = """
		<screen position="center,center" size="700,424" title="Set Root Password" flags="wfNoBorder" >
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ChangeRootPassword/backg2.png" position="0,0" size="700,424" alphatest="on" />
			<widget name="lab" position="40,20" size="620,384" font="Regular;20" zPosition="1" transparent="1" />
		</screen>"""

	def __init__(self, session, oldp, newp):
		Screen.__init__(self, session)
				
		self["lab"] = Label("")
		self["actions"] = ActionMap(["WizardActions"],
			{
				"ok": self.end,
				"back": self.end,
			}, -1)
		
		self.oldp = oldp
		self.newp = newp
		self.connected = True
		self.connect()
		
	def connect(self):
		tn = Telnet("localhost")
		out = tn.read_until(b"login:", 3)
		tn.write(b"root\n")
		check = tn.read_until(b"Password:", 2)
		out += check
		if check.__contains__(b"Password:"):
			tn.write(self.oldp.encode() + b"\n")
			check = tn.read_until(b"~#", 2)
			out += check
		if check.__contains__(b"~#"):
			tn.write(b"passwd\n")
			out += tn.read_until(b"password", 2)
			tn.write(self.newp.encode() + b"\n")
			out += tn.read_until(b"password", 2)
			tn.write(self.newp.encode() + b"\n")
			out += tn.read_until(b"xxx", 1)
			tn.write(b"exit\n")
			out += tn.read_all()
		else:
			out += b"\nLogin incorrect, wrong password."
			tn.close()
		
		self.connected = False
		self["lab"].setText(out)
	
	def end(self):
		if self.connected == False:
			self.close()

		
def main(session, **kwargs):
	session.open(SetPasswdMain)

def Plugins(**kwargs):
	return PluginDescriptor(name="Change root password", description="Change the root password of your box", icon="icon.png", where = PluginDescriptor.WHERE_PLUGINMENU, fnc=main)
	
