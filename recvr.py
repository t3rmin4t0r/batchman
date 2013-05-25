from cPickle import loads as unpickle;
 
import sys, marshal, types;
 
sys.path[-1] = "/tmp/";
 
callcode = unpickle(sys.stdin.read());
module=callcode["module"];
open("/tmp/sandbox.py","w");
import sandbox;
funcs=[marshal.loads(c) for c in callcode["funcs"].values()];
map(lambda code: setattr(sandbox, code.co_name, types.FunctionType(code, sandbox.__dict__, code.co_name)), funcs);
args=unpickle(callcode["args"]);
imports=callcode["imports"];
map(lambda module: setattr(sandbox, module, __import__(imports[module])), imports);
sandbox.__run__(**args);
# This file can have no real comments because all new lines will be chomped (remember to put semi colons)
