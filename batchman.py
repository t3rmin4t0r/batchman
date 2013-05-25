from paramiko.client import SSHClient, AutoAddPolicy, Agent
import sys, cPickle
from parallel_map import parallel_for
from itertools import groupby
import logging

def readhosts(f):
	hosts = [l.strip() for l in open(f, "r").readlines()]
	nousers = [(None,h) for h in hosts if h.find("@") == -1]
	users = [tuple(h.split("@")) for h in hosts if h.find("@") != -1]
	return nousers+users

hosts = readhosts(sys.argv[1])

#logging.basicConfig(level=logging.DEBUG)

def timecheck(h):
	cmd = "date +%s"
	s = SSHClient()
	print "> %s" % (h,)
	s.set_missing_host_key_policy(AutoAddPolicy())
	s.connect(hostname=h[1], username=h[0])
	(_in, _out, _err) = s.exec_command( cmd, bufsize=4096)
	print "< %s" % (h,)
	return (h,_out.read())

#result = parallel_for(timecheck, ips[::], threads=10)

from sendr import package

# the crazy bit
def make_recvr(mod):
	# generate bytecode for mod.__run__(x=1)
	bytecode = (package(mod, {"x":1}));
	client_cmd=open("recvr.py", "r").read()
	client_cmd = client_cmd.replace("\n", "")
	client_cmd = client_cmd.replace("read()", "read(%d)" % len(bytecode))	
	client_cmd = "python -c '%s'" % (client_cmd)
	def recvr(h):
		s = SSHClient()
		print "> %s" % (h,)
		s.set_missing_host_key_policy(AutoAddPolicy())
		s.connect(hostname=h[1], username=h[0])	
		(_in, _out, _err) = s.exec_command(client_cmd, bufsize=4096)
		_in.write(bytecode)
		_in.flush()
		print "< %s" % (h,)
		err = _err.read()
		if(err):
			print err
		return (h,_out.read())
	return recvr

import payload
recvr = make_recvr(payload)

result = parallel_for(recvr, hosts[::], threads=10)

print result
