import config
import wx
import gui
import globalPluginHandler
import ui
from . import google_currency as gc
from scriptHandler import script
import addonHandler
addonHandler.initTranslation()
ad={}
for key,value in google_currency.CODES.items():
	ad[value]=key

roleSECTION = "CurrencyConverter"
confspec = {
"from": "string(default=USD)",
"to": "string(default=EGP)"}

config.conf.spec[roleSECTION] = confspec

class TextWindow(wx.Dialog):
	def __init__(self, text, title):
		super(TextWindow, self).__init__(gui.mainFrame, title=title)
		self.tlable = wx.StaticText(self, label=_("from"), name="ts")
		self.sou= wx.Choice(self, name="ts")
		self.tlable1 = wx.StaticText(self, label=_("to"), name="ts1")
		self.sou1= wx.Choice(self, name="ts1")
		self.outputCtrl = wx.SpinCtrl(self,min=1,max=1000000)
		self.ok=wx.Button(self,label="next")
		self.ok.Bind(wx.EVT_BUTTON,self.a1)
		self.outputCtrl.Bind(wx.EVT_KEY_DOWN, self.onOutputKeyDown)
		self.aaa()
		self.outputCtrl.SetValue(text)
		self.Show()
	def aaa(self):
		self.sou.Set(list(ad.keys()))
		self.sou1.Set(list(ad.keys()))
		self.sou.SetStringSelection(google_currency.CODES[config.conf[roleSECTION]["from"]])
		self.sou1.SetStringSelection(google_currency.CODES[config.conf[roleSECTION]["to"]])

	def onOutputKeyDown(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.Close()
		event.Skip()
	def a1(self,event):
		config.conf[roleSECTION]["from"]=ad[self.sou.StringSelection]
		config.conf[roleSECTION]["to"]=ad[self.sou1.StringSelection]
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
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory= _("currency converter")
	@script(gesture="kb:NVDA+alt+c")
	def script_hi (self, gesture):
		TextWindow(1,"currency dialog")
	script_hi.__doc__= _("convert ")
