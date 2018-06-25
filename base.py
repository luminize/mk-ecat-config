from machinekit import rtapi as rt
from machinekit import hal


def instantiate_threads():
    print('instantiating thread(s)')
    rt.newthread('st', 1000000, fp=True)


def setup_lcec(configfile=None):
    # load ethercat config parser
    print('lcec_conf %s' % configfile)
    hal.loadusr('lcec_conf %s' % configfile, wait=True)
    # load ethercat realtime module
    rt.loadrt('lcec')


def create_joint_plumbing(st, joint_nr):
    rt.newinst('offsetv2', 'joint%i_offset' % joint_nr)
    hal.addf('joint%i_offset.update-output' % joint_nr, "%s" % st)
    hal.addf('joint%i_offset.update-feedback' % joint_nr, st)
    rt.newinst('mult2v2', 'joint%i_scale_pos_cmd' % joint_nr)
    hal.addf('joint%i_scale_pos_cmd' % joint_nr, st)
    rt.newinst('div2v2', 'joint%i_scale_pos_fb' % joint_nr)
    hal.addf('joint%i_scale_pos_fb.funct' % joint_nr, st)
    jointscale = hal.newsig('joint%i_scale' % joint_nr, hal.HAL_FLOAT)
    hal.Pin('joint%i_scale_pos_fb.deadband' % joint_nr).set( 0.00000001)
    
    # now connect the components, scale to mult and div
    jointscale.link('joint%i_scale_pos_cmd.in1' % joint_nr)
    jointscale.link('joint%i_scale_pos_fb.in1' % joint_nr)
    
    # offset joint (ROS) position to scale mult
    hal.Pin('joint%i_offset.out' % joint_nr).link(
        'joint%i_scale_pos_cmd.in0' % joint_nr)
    # (de)offset scale div to joint (ROS) position
    hal.Pin('joint%i_scale_pos_fb.out' % joint_nr).link(
        'joint%i_offset.fb-in' % joint_nr)


def setup_joint_values(joint_nr):
    pass


def setup_joint(st):
    # for each joint we need
    # - an offset (from the joints zero) either for when an encoder
    #   is not homed, or for finetuning manufacturing dimensions.
    # - a scale, converting the angle in radians to pulses per revolution
    #   of the output shaft. Consisting of PI, encoder resolution and ratio
    # - convert float to u32
    for joint_nr in range(0,5):
        create_joint_plumbing(st, joint_nr)
        setup_joint_values(joint_nr)


def instantiate_components(configfile=None, demo=False):
    # name of the servothread
    st = 'st'
    print('instantiating components')
    if demo == False:
        setup_lcec(configfile)
        # write lcec-read-all first
        hal.addf('lcec.read-all', st)
        # load other stuff
        setup_joint(st)
        # do some final writing of functions to the thread
        # write lcec-write-all last
        hal.addf('lcec.write-all', st)
    else:
        # create a demo joint for when EtherCAT not available
        create_joint_plumbing(st, 6)


def add_components_to_thread():
    pass
