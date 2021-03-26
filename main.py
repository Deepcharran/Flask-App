from flask import Flask, render_template, jsonify
from influxdb import InfluxDBClient

application = Flask(__name__)
def influxdbfun():
	client = InfluxDBClient(host='10.106.79.198',port=8086)
	client.switch_database('telegraf')
	data = client.query('SELECT "source", "neighbor_address_xr/ipv4_address", "is_this_neighbor_us", "interface_name" FROM "Cisco-IOS-XR-ipv4-pim-oper:pim/active/default-context/neighbors/neighbor" WHERE time > now() - 30s GROUP BY "source"')
	routers=[]
	routernames=[]
	results=[]
		#ipdict = {}
	for i in data:
		for j in i:
			#j['target']='target'
			for k,v in j.items():
				if k == 'neighbor_address_xr/ipv4_address' and v.startswith("192.184.163"):
					results.append(j)
	for j in results:
		#j['target']='target'
		for k,v in j.items():
			if k == 'source' and v not in routers:
				routers.append(v)
				routernames.append({"id": v}) 
		#for k,v in j.items():
		#    if k=='is_this_neighbor_us' and v == 'true':
		#        ipdict[j['interface_name']]=j['source']
	for j in results:
		#if j['interface_name'] in ipdict:
		#    j['target']=ipdict[j['interface_name']]  
		if j['neighbor_address_xr/ipv4_address'] == '192.184.163.5':
			j['target']='ASR-9906-B'
		elif j['neighbor_address_xr/ipv4_address'] == '192.184.163.9':
			j['target']='ASR-9906-B'
		elif j['neighbor_address_xr/ipv4_address'] == '192.184.163.22':
			j['target']='ASR-9906-B'
		elif j['neighbor_address_xr/ipv4_address'] == '192.184.163.2':
			j['target']='ASR9906-A'
		elif j['neighbor_address_xr/ipv4_address'] == '192.184.163.6':
			j['target']='ASR9906-A'
		elif j['neighbor_address_xr/ipv4_address'] == '192.184.163.1':
			j['target']='NCS-5508-A'
		elif j['neighbor_address_xr/ipv4_address'] == '192.184.163.14':
			j['target']='NCS-5508-A'
		elif j['neighbor_address_xr/ipv4_address'] == '192.184.163.18':
			j['target']='NCS-5508-A'
		elif j['neighbor_address_xr/ipv4_address'] == '192.184.163.10':
			j['target']='ASR-9904-G-LS'
		elif j['neighbor_address_xr/ipv4_address'] == '192.184.163.17':
			j['target']='ASR-9904-G-LS'
		elif j['neighbor_address_xr/ipv4_address'] == '192.184.163.26':
			j['target']='ASR-9904-G-LS'
		elif j['neighbor_address_xr/ipv4_address'] == '192.184.163.21':
			j['target']='ASR-9906-C-LS'
		elif j['neighbor_address_xr/ipv4_address'] == '192.184.163.25':
			j['target']='ASR-9906-C-LS'
		elif j['neighbor_address_xr/ipv4_address'] == '192.184.163.13':
			j['target']='NCS-5508-B'
		
	#print("Total Numbers of Active Routers :",len(routernames))
	for j in results:
		for k,v in j.items():
			if k == 'target' and v not in routers:
				routers.append(v)
				routernames.append({"id": v})
	# print("Nodes(Routers) :",routernames)
	# print("\n")
	detailed_results=results
	# print(detailed_results)
	for i in results:
		del i['time']
		del i['neighbor_address_xr/ipv4_address']
		del i['interface_name']
		del i['is_this_neighbor_us']

	# print("\n")
	# print(results)
	return (routernames, results)




	# random_decimal_returning_var=client.query('SELECT * FROM "routers"')
	# return random_decimal_returning_var

@application.route('/update_decimal', methods=['POST'])
def updatedecimal():
	routernames, results=influxdbfun()
	return jsonify('', render_template('random_decimal_model.html', xrouterlist=routernames, ytargetrouter=results))
	# return jsonify('', render_template('random_decimal_model.html', x=results))

	# random_decimal=influxdbfun()
	# return jsonify('', render_template('random_decimal_model.html', x=random_decimal))

@application.route('/')
def homepage ():
	routernames, results=influxdbfun()
	return render_template('index.html', xrouterlist=routernames, ytargetrouter=results)
	# return render_template('index.html', x=results)

	# random_decimal=influxdbfun()
	# return render_template('index.html', x=random_decimal)
application. run()