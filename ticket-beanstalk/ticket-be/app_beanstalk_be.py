#!/usr/bin/python

import redis
import sys
import time
import beanstalkc
import ticket_class

for a in range(1,6):
    try:
	bt = beanstalkc.Connection(host='beanstalk', port=11300)
	print >> sys.stderr, "BE is connected beanstalk server"
        break
    except:
	bt = 0
    print >> sys.stderr, "BE is reconnecting to beanstalk. Attempt %i " % a
    time.sleep(5)

r = redis.Redis(host="red")

while 1 and bt:
    msg = bt.reserve()
    t=str(msg.body)
    msg.delete()
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
