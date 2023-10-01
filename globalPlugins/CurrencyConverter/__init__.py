from gui import SettingsPanel, NVDASettingsDialog,guiHelper
import config
import wx
import gui
import globalPluginHandler
import ui
from . import google_currency as gc
from scriptHandler import script
import addonHandler
addonHandler.initTranslation()

roleSECTION = "CurrencyConverter"
confspec = {
"from": "string(default=USD)",
"to": "string(default=EGP)"}

config.conf.spec[roleSECTION] = confspec

class TextWindow(wx.Dialog):
	def __init__(self, text, title):
		super(TextWindow, self).__init__(gui.mainFrame, title=title)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.outputCtrl = wx.SpinCtrl(self,min=1,max=1000000)
		self.ok=wx.Button(self,label="next")
		sizer.Add(self.ok, proportion=2, flag=wx.EXPAND)
		self.ok.Bind(wx.EVT_BUTTON,self.a1)
		self.outputCtrl.Bind(wx.EVT_KEY_DOWN, self.onOutputKeyDown)
		sizer.Add(self.outputCtrl, proportion=1, flag=wx.EXPAND)
		self.SetSizer(sizer)
		sizer.Fit(self)
		self.outputCtrl.SetValue(text)
		self.outputCtrl.SetFocus()
		self.Raise()
		self.Maximize()
		self.Show()

	def onOutputKeyDown(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.Close()
		event.Skip()
	def a1(self,event):
		a=gc.convert(config.conf[roleSECTION]["from"],config.conf[roleSECTION]["to"],self.outputCtrl.GetValue())
		re(a,"result")
		self.Close()
class re(wx.Dialog):
	def __init__(self, text, title):
		super(re, self).__init__(gui.mainFrame, title=title)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.outputCtrl = wx.TextCtrl(self,style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
		self.outputCtrl.Bind(wx.EVT_KEY_DOWN, self.onOutputKeyDown)
		sizer.Add(self.outputCtrl, proportion=1, flag=wx.EXPAND)
		self.SetSizer(sizer)
		sizer.Fit(self)
		self.outputCtrl.SetValue(text)
		self.outputCtrl.SetFocus()
		self.Raise()
		self.Maximize()
		self.Show()

	def onOutputKeyDown(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.Close()
		event.Skip()
class CRSettingsPanel(SettingsPanel):
	title = _("currency converter")
	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.tlable = sHelper.addItem(wx.StaticText(self, label=_("from"), name="ts"))
		self.sou= sHelper.addItem(wx.Choice(self, name="ts"))
		self.tlable1 = sHelper.addItem(wx.StaticText(self, label=_("to"), name="ts1"))
		self.sou1= sHelper.addItem(wx.Choice(self, name="ts1"))
		self.ad={}
		for key,value in google_currency.CODES.items():
			self.ad[value]=key
			self.sou.Append(value,key)
			self.sou1.Append(value,key)
		self.sou.SetStringSelection(google_currency.CODES[config.conf[roleSECTION]["from"]])
		self.sou1.SetStringSelection(google_currency.CODES[config.conf[roleSECTION]["to"]])
	def postInit(self):
		self.sou.SetFocus()
	def onSave(self):
		config.conf[roleSECTION]["from"]=self.ad[self.sou.StringSelection]
		config.conf[roleSECTION]["to"]=self.ad[self.sou1.StringSelection]
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory= _("currency converter")
	NVDASettingsDialog.categoryClasses.append(CRSettingsPanel)
	@script(gesture="kb:NVDA+alt+c")
	def script_hi (self, gesture):
		TextWindow(1,"currency dialog")
	script_hi.__doc__= _("convert ")
	def terminate(self):
		NVDASettingsDialog.categoryClasses.remove(CRSettingsPanel)