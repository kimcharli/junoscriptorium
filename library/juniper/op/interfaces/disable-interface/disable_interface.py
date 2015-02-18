
import jcs
import sys
import argparse
from jnpr.junos import Device
from pprint import pprint

arguments = {
  'interface': 'Interface to deactivate',
  'silent': 'Decides where the output will go, 0 -> stdout, 1 -> syslog'}


def emit_success(message,silent):
  if silent:
    jcs.syslog("user.info", "disable-interface.slax[Success]: ", message)
  else:
	print message

# 
def do_commit(dev,config_str,format="xml"):
  from jnpr.junos.utils.config import Config
  jcs.trace("do_commit() with config_str = %s" % config_str)
  cu = Config(dev)
  cu.lock()
  res = cu.load(config_str, format=format, merge=True)
  cu.commit()
  cu.unlock()
  return res

def recursive_dict(element):
     return element.tag, \
            dict(map(recursive_dict, element)) or element.text

def main():
  print "sys.argv[0] = %s" % sys.argv[0]
  parser = argparse.ArgumentParser(description='This is a demo script.')
  parser.add_argument('-interface', required=True)
  parser.add_argument('-silent', required=False)
  args = parser.parse_args()
  print "interface = %s" % args.interface
  print "silent = %s" % args.silent
  
  dev = Device().open()
  if(not dev):
    jcs.emit_error("Not able to connect to local mgd")
    sys.exit(1)
  config_set = "set interfaces %s disable" % args.interface[1:-1]
  from jnpr.junos.exception import RpcError
  res = None
  try:
    res = do_commit(dev,config_set,"set")
  except RpcError as e:
    print "== RpcError"
    msg = recursive_dict(e)
    #print "==== RpcError %s, dir() %s: errs=%s, msg=%s" % (str(e), dir(e),e.errs,e.message)
    print "==== RpcError: %s" % msg
    print "  == fin RpcError"
    #errs = e.xpath('//rpc-error')
    #for ee in errs:
    #  print "   %s: %s, %s" % (dir(ee),ee.tag, ee.values )
  except:
    print "Exception!!", sys.exc_info()[0]
  else:
    print "success"
    recur = recursive_dict(res)
    print "  res = %s" % recur
    #pprint(recur)
    
  print "hello!"
  dev.close()

if __name__ == '__main__':
  main()

