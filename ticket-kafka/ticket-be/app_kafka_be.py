#!/usr/bin/python

import redis
import sys
import time
from kafka import KafkaConsumer
import ticket_class

for a in range(1,6):
    try:
	kc = KafkaConsumer(bootstrap_servers='kafka:9092',auto_offset_reset='earliest',consumer_timeout_ms=1000)
	print >> sys.stderr, "BE is connected kafka server"
        break
    except:
	kp=0
    print >> sys.stderr, "BE is reconnecting to kafka. Attempt %i " % a
    time.sleep(5)

kc.subscribe(['ticket'])
print >> sys.stderr, "BE is subscribed to 'ticket'"

r = redis.Redis(host="red")

while 1:
    for msg in kc:
#	    print >> sys.stderr, "BE got message: "+str(msg)
	    t=str(msg.value)
	    print >> sys.stderr, "BE got ticket: %s " % t
	    if r.exists(t):
    		print >> sys.stderr, "BE has found %s in cache" % t
		continue
	    r.setex(t,600,"@")
	    print >> sys.stderr, "BE is calculating '%s' " % t
	    o=ticket_class.Ticket(t)
	    ans=o.first()
	    if ans==None: ans="-"
	    r.set(t,ans)
	    print >> sys.stderr, "BE is ready: %s->%s " % (t,ans)

#kc.close()
