import requests

def pwndb(arg):
	# Always expect a list of arg
	email = arg[0]
	if '@' in email:
		# Website	: http://pwndb2am4tzkvold.onion/
		url = 'http://pwndb2am4tzkvold.onion/'

		header = {
			'Host': 'pwndb2am4tzkvold.onion',
			'User-Agent': 'pwnTeams',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate',
			'Referer': 'http://pwndb2am4tzkvold.onion/',
			'Content-Type': 'application/x-www-form-urlencoded',
		}

		results = {}
		luser = email[:email.index('@')]
		domain = email[email.index('@')+1:]
		# Setting up for Tor
		session = requests.session()
		session.proxies = {}
		session.proxies['https'] = 'socks5h://localhost:9050'
		session.proxies['http'] = 'socks5h://localhost:9050'
		data = {
			'luser':luser,
			'domain':domain,
			'luseropr':'1',  # 0 : = , 1 : LIKE //(SQL)
			'domainopr':'1', # 0 : = , 1 : LIKE //(SQL)
			'submitform':'em'
		}
		r = session.post(url, data = data, headers=header)
		recvData = r.content
		output = recvData[recvData.find('<pre>')+5:recvData.find('</pre>')]
		# First Array is a garbage !
		luser = output[output.find('[luser]')+11:output.find('\n    [domain]')]
		domain = output[output.find('[domain]')+12:output.find('\n    [password]')]
		passwd = output[output.find('[password]')+14:output.find('\n)')]
		output = output[output.find('\n)')+2:]

		if 'Array' in output:
			db = "<table border='1'><tr><th>Email</th><th>Password</th></tr>"
			for i in range(output.count('Array')):
				pwn = "<tr>"
				luser = output[output.find('[luser]')+11:output.find('\n    [domain]')]
				domain = output[output.find('[domain]')+12:output.find('\n    [password]')]
				passwd = output[output.find('[password]')+14:output.find('\n)')]
				output = output[output.find('\n)')+2:]
				pwn += "<td>" + luser + '@' + domain + "</td>"
				pwn += "<td>" + passwd + "</td>"
				pwn += "</tr>"
				db += pwn 
			db += "</table>"
		else:
			db = "Error: We didn't find it !"
		return db
	else:
		db = "Error: The email is not valid !"
		return db
