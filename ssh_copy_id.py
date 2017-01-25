from paramiko.client import SSHClient, AutoAddPolicy, Agent
import sys, cPickle
from parallel_map import parallel_for
from itertools import groupby
import logging
from os.path import expanduser

def readhosts(f):
	hosts = [l.strip() for l in open(f, "r").readlines() if l[0] != '#']
	nousers = [(None,h) for h in hosts if h.find("@") == -1]
	users = [tuple(h.split("@")) for h in hosts if h.find("@") != -1]
	return nousers+users

hosts = readhosts(sys.argv[1])

#logging.basicConfig(level=logging.DEBUG)

def timecheck(h):
	cmd = """
		mkdir -p ~/.ssh ; 
		chmod 0600 ~/.ssh/; 
		echo '%s' >> ~/.ssh/authorized_keys; 
		chmod 0600 ~/.ssh/*""" % (open(expanduser("~/.ssh/authorized_keys")).read())
	s = SSHClient()
	print "> %s" % (h,)
	s.set_missing_host_key_policy(AutoAddPolicy())
	s.connect(hostname=h[1], username=h[0])#, password='')
	(_in, _out, _err) = s.exec_command( cmd, bufsize=4096)
	print "< %s" % (h,)
	return (h,_out.read())

result = parallel_for(timecheck, hosts[::], threads=10)

print result