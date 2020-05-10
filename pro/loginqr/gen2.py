import requests, json

### QR ROTATE LOGIN EXAMPLE ###

header_list= ["android_lite", "chrome", "ios_ipad", "desktopmac", "desktopwin"]

#print(header_list)
key = "DMtTxFtFXkrd"
def login():
	header = "chrome"
#if header not in header_list:
#    raise Exception("Wrong header input")
	result = json.loads(requests.get("https://api.boteater.us/line_qr_v2?auth=" + key + "&header="+header).text)
	print("QR Link: "+result["result"]["qr_link"])
#print("Login IP: "+result["result"]["login_ip"])
#print("QR Active For 30 Seconds")
	result = json.loads(requests.get(result["result"]["callback"]+"&auth="+key).text)
	if result["status"] != 200:
		raise Exception("Timeout!!!")
	print("Pincode: "+result["result"]["pin_code"])
	result = json.loads(requests.get(result["result"]["callback"]+"&auth="+key).text)
	if result["status"] != 200:
		raise Exception("Timeout!!!")
#print("Cert: "+result["result"]["cert"])
	return result["result"]["token"]
