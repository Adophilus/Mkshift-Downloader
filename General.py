import json;
import time;
import requests;
import urllib;
from threading import Thread;
from re import search, sub, I, escape;

class General ():
	def __init__ (self):
		pass;

	def jsonize (self, string):
		jsonData = json.loads(string);
		return jsonData;
	
	def unjsonize (self, json_data):
		string = json.dumps(json_data, indent = 4);
		return string;
		
	def load_json (self, path):
		with open(path, "r") as file:
			data = json.load(file);

			return data;

	def save_json (self, path, data):
		with open(path, "w") as file:
			json.dump(data, file, indent = 4);

	def json_save (self, path, data):
		self.save_json(path, data);

	def json_load (self, path = ""):
		self.load_json(path);

	def putContentIn (self, filePath, data):
		with open(filePath, "w") as file:
			file.write(data);

	def getContentOf (self, filePath):
		with open(filePath, "r") as file:
			return file.read();

	def setImmediate (self, method, args = {}):

		def _method (method, arguments):
			operation = method(**arguments);

		immediateObj = Thread(target = _method, args = (method, args));
		immediateObj.start();
		return immediateObj;

	def setTimeout (self, method, secs = 5, args = {}):

		def _method (method, arguments, secs):
			time.sleep(secs);
			operation = method(**arguments);

		timeoutObj = Thread(target = _method, args = (method, args, secs));
		timeoutObj.start();
		return timeoutObj;

	def setInterval (self, method, secs = 10, args = {}):
		def _method (method, arguments, secs):
			while True:
				time.sleep(secs);
				operation = method(**arguments);

				if operation == "end" or operation == "break":
					break;

		intervalObj = Thread(target = _method, args = (method, args, secs));
		intervalObj.start();
		return intervalObj;

	def clearTimeout (self, timeoutObject):
		pass;

	def clearInterval (self, intervalObject):
		self.clearTimeout(intervalObject);

	def httpPost (self, url, postData = {}):
		req = requests.post(url, data = postData);

		try:
			self.jsonize(req.text);
			return self.jsonize(req.text);
		except Exception as e:
			return req.text;

	def httpGet (self, url, getData = {}):
		req = requests.get(url, data = postData);

		return req.text;

	def exp (self, num1, num2):
		return num1 ** num2;

	def swapQuotes (self, txt):
		matchObj = search(r"'", txt, I);
		if matchObj:
			ntxt = sub(r"'", '"', txt);
			return ntxt;
		else:
			return txt;

	def downloadFile (self, url, filename):
		return urllib.urlretrieve(url, filename);

	def searchString (self, string, regex, ignoreCase = False):
		if ignoreCase:
			match = search(r"%s" % regex, string, I);
		else:
			match = search(r"%s" % regex, string);
			
		return match;
	
	def wait (self, secs):
		time.sleep(secs);
	
	def sendTrue (self, array):
		array["status"] = True
		return array

	def sendFalse (self, array):
		array["error"] = array["data"];
		array["status"] = False
		return array