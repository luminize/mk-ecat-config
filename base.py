from machinekit import rtapi as rt
from machinekit import hal

def instantiate_threads():
    print('instantiating thread(s)')
    rt.newthread('st', 1000000, fp=False)

def instantiate_components(configfile=None):
    print('instantiating components')
    # load ethercat config parser
    print('lcec_conf %s' % configfile)
    hal.loadusr('lcec_conf %s' % configfile, wait=True)
    # load ethercat realtime module
    rt.loadrt('lcec')

def add_components_to_thread():
    hal.addf('lcec.read-all', 'st')
    hal.addf('lcec.write-all', 'st')

