from flask import Flask, render_template, jsonify
from influxdb import InfluxDBClient

application = Flask(__name__)
# app.debug = True
# app.run(host = '10.106.79.198',port=5000)
def influxdbfun():
	client = InfluxDBClient(host='10.106.79.198',port=8086)
	client.switch_database('telegraf') 
	data = client.query('SELECT "source", "neighbor_address_xr/ipv4_address" AS IP, "is_this_neighbor_us", "interface_name" FROM "Cisco-IOS-XR-ipv4-pim-oper:pim/active/default-context/neighbors/neighbor" WHERE time > now() - 1m GROUP BY "source"')
	routers=[]
	routernames=[]
	unrouternames=[]
	results=[]
	ipmap = {}
	#intmap = {}
	unidenno=1
	for i in data:
		for j in i:
			for k,v in j.items():
				if k == 'IP' and v.startswith("192.184.163"):
					results.append(j)
	for j in results:
		for k,v in j.items():
			if k == 'source' and v not in routers:
				routers.append(v)
				routernames.append({"id": v}) 
		for k,v in j.items():
			if k=='is_this_neighbor_us' and v == 'true':
				ipmap[j['IP']]=j['source']
				#intmap[j['interface_name']]=j['source']
	for j in results:
		if j['IP'] in ipmap and j['is_this_neighbor_us']=='false': # and j['interface_name'] in intmap:
			j['target'] = ipmap[j['IP']]  
		elif j['IP'] not in ipmap and j['is_this_neighbor_us']=='false':
			j['target']='Unidentified Router'+str(unidenno)
			unidenno=unidenno+1    
	# print("Total Numbers of Known Active Routers :",len(routernames))
	for j in results:
		for k,v in j.items():
			if k == 'target' and v not in routers:
				unrouternames.append({"id": v})
	print("Total Numbers of Unknown Active Routers :",len(unrouternames))
	# print("Nodes(Known Routers) :",routernames)
	# print("\n")
	detailed_results=results
	for i in results:
		del i['time']
		del i['IP']
		del i['interface_name']
		del i['is_this_neighbor_us']
	# print(results)
	ans=[]
	for j in results:
		if len(j)==2 and not j['target'].startswith('Unidentified'):
			ans.append(j)
	print(ans)
	return (routernames, ans)
	# random_decimal_returning_var=client.query('SELECT * FROM "routers"')
	# return random_decimal_returning_var

@application.route('/update_decimal', methods=['POST'])
def updatedecimal():
	routernames, results=influxdbfun()
	return {"x":routernames, "y":results}
	# return jsonify('', render_template('index.html', x=routernames, y=results))
	# return jsonify('', render_template('random_decimal_model.html', x=results))

	# random_decimal=influxdbfun()
	# return jsonify('', render_template('random_decimal_model.html', x=random_decimal))

@application.route('/')
def homepage ():
	routernames, results=influxdbfun()
	print(routernames,results)
	return render_template('index.html', x=routernames, y=results)
	# return render_template('index.html', x=results)

	# random_decimal=influxdbfun()
	# return render_template('index.html', x=random_decimal)
application. run()