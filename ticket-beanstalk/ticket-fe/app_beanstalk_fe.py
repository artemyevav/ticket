#!/usr/bin/python

from flask import Flask, render_template, request
import redis
import time
import sys
import beanstalkc

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
	    if bt: bt.put(str(t))
	    return "Sent %s" % t
    return render_template('index.tpl')


if __name__ == "__main__":
    for a in range(1,6):
	try:
	    bt=beanstalkc.Connection(host='beanstalk', port=11300)
#	    bt=beanstalkc.Connection(host='localhost', port=11300)
	    print >> sys.stderr, "FE is connected to beanstalk"
	    break
	except:
	    bt=0
	print >> sys.stderr, "FE is reconnecting to beanstalk. Attempt %i " % a
	time.sleep(5)

    r = redis.Redis(host="red")

    if bt and r: app.run(host="0.0.0.0",debug=True,use_reloader=False)
#    app.run(host="0.0.0.0")
