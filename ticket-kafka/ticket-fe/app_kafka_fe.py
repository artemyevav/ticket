#!/usr/bin/python

from flask import Flask, render_template, request
import redis
import time
import sys
from kafka import KafkaProducer

app = Flask(__name__)
    
@app.route('/')
def index():
    t=request.args.get("ticket")
    if t and len(t)==6:

	if r.exists(t):
	    ans=r.get(t)
	    if ans == '-':
		return "FE: No answer for '%s'" %t
	    elif ans == '@':
		return "FE: Answer for '%s' is being calculated" % t
	    else:
		return "FE: Found: (%s,%s)" % (t,ans)
	else:
	    print >> sys.stderr, "FE is sending '%s' to kafka" % t
	    if kp: kp.send('ticket',b""+str(t))
	    return "Sent %s" % t
    return render_template('index.tpl')


if __name__ == "__main__":
    for a in range(1,6):
	try:
	    kp=KafkaProducer(bootstrap_servers=['kafka:9092'])
	    print >> sys.stderr, "FE is connected to kafka server"
	    break
	except:
	    kp=0
	print >> sys.stderr, "FE is reconnecting to kafka. Attempt %i " % a
	time.sleep(5)

    r = redis.Redis(host="red")

    if kp and r: app.run(host="0.0.0.0",debug=True,use_reloader=False)
#    app.run(host="0.0.0.0")
