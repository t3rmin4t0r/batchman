
#!/usr/bin/python
import sys as XX
import glob
import json 

def blah(a):
	return [XX.executable]+a
def foo(x):
	return blah(glob.glob("/var/log/*"))
def bar(x=1):
	return foo(x)
def __run__(**kwargs):
	print json.dumps(bar(**kwargs))

if __name__ == "__main__":
	__run__(x=1)
