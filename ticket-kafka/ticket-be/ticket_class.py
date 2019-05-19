#!/usr/bin/python

from random import randint
import itertools

class Ticket:

    def __init__(self,ticket):
	self.t_len=6
	self.t_goal=100
	self.t_ops=['+','-','*','/']
	self.o_best={"o":None,"ops":self.t_len,"neg":self.t_len}
	self.ticket=map(int,list(ticket))


    def add_neg(self,v):
	if len(v)==1:return [[v[0]],[-v[0]]]
	return [[m*v[0]]+s for s in self.add_neg(v[1:]) for m in [1,-1]]

    def variants(self):
        ret=[]
        for i in range(0,2**(self.t_len-1)):
            stack=[self.ticket[0]]
            for b in range(0,self.t_len-1):
        	if i & (1<<b):
    		    stack.append(self.ticket[b+1])
		else:
		    stack.append(int(str(stack.pop())+str(self.ticket[b+1])))
	    ret+=self.add_neg(stack)
	return ret

    def ops(self,variant):
	if len(variant)==1: return [variant]
	if len(variant)==2:
	    return [variant+[o] for o in self.t_ops]
	else:
	    s1=self.ops(variant[1:])
	    s2=self.ops(variant[:-1])
	    return [[variant[0]]+v+[o] for v in s1 for o in self.t_ops]+[v+[variant[-1]]+[o] for v in s2 for o in self.t_ops]
    
    def calc(self,o):
	stack=[]
	for i in o:
    	    if i in self.t_ops:
		v2=float(stack.pop())
	        v1=float(stack.pop())
	        if i == '+':
	    	    stack.append(v1+v2)
		elif i == '-':
		    stack.append(v1-v2)
		if i == '*':
		    stack.append(v1*v2)
		if i == '/':
		    if v2 == 0:return 0 # divide by zero
		    stack.append(v1/v2)
	    else:
		stack.append(float(i))
	return stack.pop()

    def decrypt(self,o):
	stack=[]
        for i in o:
    	    if i in self.t_ops:
	        v2=stack.pop()
	        v1=stack.pop()
	        if i in ["*"]:
		    stack.append(str(v1)+i+str(v2))
		else:
		    stack.append("("+str(v1)+i+str(v2)+")")	    
	    else:
		stack.append("("+str(i)+")" if i<0 else str(i))
	return stack.pop()
    

    def best(self,o):
	neg=len([x for x in o if x<0])
	ops=(len(o)+1)/2
	if ops<=self.o_best["ops"]:
	    if neg<self.o_best["neg"]:
		self.o_best={"o":o,"ops":ops,"neg":neg}
    
    def run(self):
	vs=self.variants()
#	perc=10
	for i,v in enumerate(vs):
#	    p=100*i/len(vs)
#	    if p % 5 == 0:
#		if p>perc:
#		    print "%d %%: %s" % (perc,self.decrypt(self.o_best["o"]) if self.o_best["o"] else "-")
#		    perc=p
	    for o in self.ops(v):
		if self.calc(o) ==self.t_goal:
		    self.best(o)
	return self.decrypt(self.o_best["o"])

    def first(self):
	vs=self.variants()
	for i,v in enumerate(vs):
	    for o in self.ops(v):
		if self.calc(o) ==self.t_goal:
		    return self.decrypt(o)

#t=Ticket('716976')
#print t.first()
