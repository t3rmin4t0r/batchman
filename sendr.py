import marshal

import cPickle
import payload
import inspect

def package(module, args={}):
	funcs = {}
	callcode = {}
	imports = {}
	for name in dir(module):
		obj = getattr(module, name)
		if inspect.isfunction(obj):
			funcs[name] = marshal.dumps(obj.func_code)
		if inspect.ismodule(obj):
			imports[name] = obj.__name__
	callcode["module"] = module.__name__
	callcode["imports"] = imports
	callcode["funcs"] = funcs
	callcode["args"] = cPickle.dumps(args)
	return cPickle.dumps(callcode)

if __name__ == "__main__":
	print package(payload, {"x":3})

