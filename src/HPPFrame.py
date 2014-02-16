#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
################################################################################
# 
#  Copyright (C) 2012-2014 Daniel Rodriguez
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""Subclass of HPPFrame, which is generated by wxFormBuilder."""

import wx

import HPPGui

import hppserv

class HPPEvent(wx.PyEvent):
    def __init__(self, pyEventId, msg=None):
        wx.PyEvent.__init__(self)
        self.SetEventType(pyEventId)
        self.msg = msg


class WxQueue(object):
    def __init__(self, frame, method):
        self.frame = frame
        self.method = method
        self.pyEventId = wx.NewId()
        self.frame.Connect(wx.ID_ANY, wx.ID_ANY, self.pyEventId, self.method)

    def put(item, block=True, timeout=None):
        # Simulate Queue interface
        wx.PostEvent(self.frame, HPPEvent(self.pyEventId, item))


# Implementing HPPFrame
class HPPFrame(HPPGui.HPPFrame):
    def createHpp(self):
	self.hppserv = hppserv.HPPThread(qout=self.qout)


    def __init__(self, parent):
	HPPGui.HPPFrame.__init__(self, parent)

        self.config = wx.Config('HPPServ', 'HPPServ');
        self.config.SetRecordDefaults(True)

        self.qout = WxQueue(frame=self, method=self.OnHppServ)
        self.createHpp()
        self.getHppConfig()


    def getHppConfig(self):
	config = self.hppserv.config

	# hppserv has a default config ... that we may load to start with

        proxysystem = self.config.ReadBool('ProxySystem', config.proxysystem)
	self.m_checkBoxUseProxySystem.SetValue(proxysystem)
        proxy = self.config.ReadBool('Proxy', config.proxy)
	self.m_checkBoxUseProxyOther.SetValue(not proxysystem and proxy)
	self.m_checkBoxUseProxyOther.Enable(not proxysystem)
        proxyurl = self.config.Read('ProxyUrl', config.proxyurl)
        self.m_textCtrlProxyUrl.SetValue(proxyurl)

        sendFullUrl = self.config.ReadBool('SendFullUrl', config.sendFullUrl)
	self.m_checkBoxSendFullUrl.SetValue(sendFullUrl)
        keepalive = self.config.ReadBool('KeepAlive', config.keepalive)
	self.m_checkBoxKeepAlive.SetValue(keepalive)
        proxykeepalive = self.config.ReadBool('ProxyKeepAlive', config.proxykeepalive)
	self.m_checkBoxKeepAliveProxy.SetValue(proxykeepalive)

        connRetry = self.config.ReadInt('ConnRetry', config.connRetry)
	self.m_spinCtrlConnRetries.SetValue(connRetry)

        dnsconnect = self.config.ReadBool('DNSConnect', config.dnsconnect)
	self.m_checkBoxConnectLocalDNS.SetValue(dnsconnect)
        connectUse10 = self.config.ReadBool('ConnectUse10', config.connectUse10)
	self.m_checkBoxConnectUseHttp10.SetValue(connectUse10)


        connectNoHost = self.config.ReadBool('ConnectNoHost', config.connectNoHost)
	self.m_checkBoxConnectRemoveHost.SetValue(connectNoHost)

        timeout = self.config.ReadInt('Timeout', config.timeout)
        self.m_spinCtrlSocketTimeout.SetValue(timeout)
        dechunk = self.config.ReadBool('DeChunk', config.dechunk)
        self.m_checkBoxDeChunk.SetValue(dechunk)
        chunknolength = self.config.ReadBool('ChunkNoLength', config.chunknolength)
        self.m_checkBoxChunkNoLength.SetValue(chunknolength)
        bufferbody = self.config.ReadBool('BufferBody', config.bufferbody)
        self.m_checkBoxBufferBody.SetValue(bufferbody)
        

        debugclient = self.config.ReadBool('DebugClient', config.debugclient)
        self.m_checkBoxDebugClient.SetValue(debugclient)
        debughpp = self.config.ReadBool('DebugHPP', config.debughpp)
        self.m_checkBoxDebugHPP.SetValue(debughpp)
        debughttpconn = self.config.ReadBool('DebugHTTPConn', config.debughttpconn)
        self.m_checkBoxDebugHttpConnection.SetValue(debughttpconn)

        host = self.config.Read('Host', config.host)
	self.m_checkBoxLocalConn.SetValue(host == 'localhost')
        port = self.config.ReadInt('Port', config.port)
	self.m_textCtrlLocalPort.SetValue(str(port))


    def setHPPConfig(self):
	config = self.hppserv.config

        config.host = 'localhost' if self.m_checkBoxLocalConn.GetValue() else ''
        self.config.Write('Host', config.host)
	config.port = int(self.m_textCtrlLocalPort.GetValue())
        self.config.WriteInt('Port', config.port)

	proxysystem = self.m_checkBoxUseProxySystem.GetValue()
        proxy = proxysystem or self.m_checkBoxUseProxyOther.GetValue()
        proxyurl = self.m_textCtrlProxyUrl.GetValue()
	config.setproxy(proxy, proxysystem, proxyurl)
        self.config.WriteBool('ProxySystem', proxysystem)
        self.config.WriteBool('Proxy', proxy)
        self.config.Write('ProxyUrl', proxyurl)

        config.sendFullUrl = self.m_checkBoxSendFullUrl.GetValue()
        self.config.WriteBool('SendFullUrl', config.sendFullUrl)
	config.keepalive = self.m_checkBoxKeepAlive.GetValue()
        self.config.WriteBool('KeepAlive', config.keepalive)
	config.proxykeepalive = self.m_checkBoxKeepAliveProxy.GetValue()
        self.config.WriteBool('ProxyKeepAlive', config.proxykeepalive)
	config.connRetry = self.m_spinCtrlConnRetries.GetValue()
        self.config.WriteInt('ConnRetry', config.connRetry)
	config.dnsconnect = self.m_checkBoxConnectLocalDNS.GetValue()
        self.config.WriteBool('DNSConnect', config.dnsconnect)
	config.connectUse10 = self.m_checkBoxConnectUseHttp10.GetValue()
        self.config.WriteBool('ConnectUse10', config.connectUse10)
	config.connectNoHost = self.m_checkBoxConnectRemoveHost.GetValue()
        self.config.WriteBool('ConnectNoHost', config.connectNoHost)
        config.timeout = self.m_spinCtrlSocketTimeout.GetValue()
        self.config.WriteInt('Timeout', config.timeout)
        config.dechunk = self.m_checkBoxDeChunk.GetValue()
        self.config.WriteBool('DeChunk', config.dechunk)
        config.chunknolength = self.m_checkBoxChunkNoLength.GetValue()
        self.config.WriteBool('ChunkNoLength', config.chunknolength)
        config.bufferbody = self.m_checkBoxBufferBody.GetValue()
        self.config.WriteBool('BufferBody', config.bufferbody)

        config.debugclient = self.m_checkBoxDebugClient.GetValue()
        self.config.WriteBool('DebugClient', config.debugclient)
        config.debughpp = self.m_checkBoxDebugHPP.GetValue()
        self.config.WriteBool('DebugHPP', config.debughpp)
        config.debughttpconn = self.m_checkBoxDebugHttpConnection.GetValue()
        self.config.WriteBool('DebugHTTPConn', config.debughttpconn)

	
    def OnButtonClickStart(self, event):
        event.Skip()
        if False:
            try:
                reload(hppserv)
            except ImportError, e:
                print "--- Error importing hppserv"
                print str(e)
                return
            else:
                pass

        self.m_buttonStart.Enable(False)
        self.m_buttonStop.Enable(True)

        self.createHpp()
        self.setHPPConfig()
        self.hppserv.hppstart()

	
    def OnButtonClickStop(self, event):
        event.Skip()
        self.m_buttonStart.Enable(True)
        self.m_buttonStop.Enable(False)

	# We will have updated the config online
	self.hppserv.hppstop()
        self.hppserv.hppexit()


    def OnCheckBoxUseProxySystem(self, event):
        event.Skip()
	onOff = self.m_checkBoxUseProxySystem.GetValue()
	self.m_checkBoxUseProxyOther.Enable(not onOff)


    def OnHppServ(self, event):
        event.Skip()


    def OnButtonClickAbout(self, event):
        event.Skip()
        dlg = HPPGui.AboutDialog(self)
        dlg.ShowModal()
        

        
