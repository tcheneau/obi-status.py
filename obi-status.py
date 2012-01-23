#!/bin/env python

import urllib2

import pygtk
pygtk.require('2.0')
import gtk
gtk.gdk.threads_init()
import gobject
import os
import sys

import ConfigParser

import argparse

def init_argparser():
	"""Simple argument parser to specify an extra configuration file"""
	parser = argparse.ArgumentParser(description='Return the status of the OBi110.')
	parser.add_argument('-c', '--config', help= "Path to a configuration file")
	
	return parser.parse_args(sys.argv[1:])

class ObiStatus:
	"""Obtain the status of the OBi110 through HTTP requests"""
	def __init__(self, extraconfigfile=None):
		cfg = ConfigParser.ConfigParser()
		if extraconfigfile:
			cfg.read(extraconfigfile)
		else:	
			cfg.read(["obi-status.cfg", os.path.expanduser('~/.obi-status.cfg')])
		self.url = self.buildUrl(cfg.get("general","address"))
		self.username = cfg.get("general","username")
		self.password = cfg.get("general","password")
		self.initAuth()
		
	def buildUrl(self, addr):
		return 'http://%s/DI_S_.xml' % addr

	def initAuth(self):
		auth_handler = urllib2.HTTPDigestAuthHandler()
		auth_handler.add_password(realm='admin@OBi110',
                          uri=self.url,
                          user=self.username,
                          passwd=self.password)
		opener = urllib2.build_opener(auth_handler)
		urllib2.install_opener(opener)
		
	def getpage(self):
		try:
			return urllib2.urlopen(self.url).read()
		except urllib2.HTTPError:
			return "wrong password"
		except urllib2.URLError:
			return "unable to connect"
		
	def getstatus(self):
		page = self.getpage()
		
		if "wrong password" in page:
			return "wrong password"
		elif "unable to connect" in page:
			return "unable to connect"
		elif "Register Failed" in page or "Retrying Register" in page:
			return "not connected"
		elif "Registered" in page:
			return "registered"
		else:
			return "unknown status"

class ObiLed:
	def __init__(self, statConn):
		self.icon = gtk.status_icon_new_from_file(self.icon_directory()+"unknown.png")
		self.icon.set_tooltip("unknown status")
		self.tick_interval = 60
		self.icon.set_visible(True)
		self.obiStatus = statConn
		
	def set_status(self, status):
		if status == "wrong password":
			self.icon.set_tooltip("Wrong log in or password")
			istatus = "unknown"
		elif status == "unable to connect":
			self.icon.set_tooltip("Unable to contact the OBi110")
			istatus = "unknown"
		elif status == "not connected":
			self.icon.set_tooltip("OBi110 not connected to the service provider")
			istatus = "notconnected"
		elif status == "registered":
			self.icon.set_tooltip("OBi110 is connected. Everything is fine!")
			istatus = "connected"
		else:
			raise("status not known")
			
		self.icon.set_from_file(self.icon_directory()+istatus+".png")


	def icon_directory(self):
		return os.path.dirname(os.path.realpath(__file__)) + os.path.sep
		
	def update(self):
		"""This method is called every time a tick interval occurs"""
		self.set_status(self.obiStatus.getstatus())		
		gobject.timeout_add(self.tick_interval*1000, self.update)
		
	def main(self):
		gobject.timeout_add(self.tick_interval, self.update)
		gtk.main()
	
if __name__ == "__main__":
	args = init_argparser()
	stat = ObiStatus(args.config)
	app = ObiLed(stat)
	app.main()
