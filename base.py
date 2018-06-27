from machinekit import rtapi as rt
from machinekit import hal
import os
import ConfigParser


def set_joint_scale(joint_nr, scale):
    hal.Signal('joint%i_scale' % joint_nr).set(float(scale))

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
    # offset
    rt.newinst('offsetv2', 'joint%i_offset' % joint_nr)
    hal.addf('joint%i_offset.update-output' % joint_nr, "%s" % st)
    hal.addf('joint%i_offset.update-feedback' % joint_nr, st)

    # scaling
    rt.newinst('mult2v2', 'joint%i_scale_pos_cmd' % joint_nr)
    hal.addf('joint%i_scale_pos_cmd.funct' % joint_nr, st)
    rt.newinst('div2v2', 'joint%i_scale_pos_fb' % joint_nr)
    hal.addf('joint%i_scale_pos_fb.funct' % joint_nr, st)
    jointscale = hal.newsig('joint%i_scale' % joint_nr, hal.HAL_FLOAT)
    hal.Pin('joint%i_scale_pos_fb.deadband' % joint_nr).set( 0.00000001)
    
    # converting components
    rt.newinst('conv_float_s32', 'joint%i_cmd_s32' % joint_nr)
    rt.newinst('conv_s32_float', 'joint%i_fb_flt' % joint_nr)
    hal.addf('joint%i_cmd_s32.funct' % joint_nr, st)
    hal.addf('joint%i_fb_flt.funct' % joint_nr, st)

    # now connect the components, scale to mult and div
    jointscale.link('joint%i_scale_pos_cmd.in1' % joint_nr)
    jointscale.link('joint%i_scale_pos_fb.in1' % joint_nr)
    
    # offset joint (ROS) position to scale mult
    hal.Pin('joint%i_offset.out' % joint_nr).link(
        'joint%i_scale_pos_cmd.in0' % joint_nr)
    # (de)offset scale div to joint (ROS) position
    hal.Pin('joint%i_scale_pos_fb.out' % joint_nr).link(
        'joint%i_offset.fb-in' % joint_nr)

    # connect converting components
    hal.Pin('joint%i_scale_pos_cmd.out' % joint_nr).link(
        'joint%i_cmd_s32.in' % joint_nr)
    hal.Pin('joint%i_fb_flt.out' % joint_nr).link(
        'joint%i_scale_pos_fb.in0' % joint_nr)


def create_fb_simulation(st, joint_nr):
    # create delayline component to simulate feedback
    # connect with scale component
    # shortcut output cmd with input fb
    pass


def connect_lcec(st, testsetup=False):
    if testsetup == False:
        for joint_nr in range(1,7):
            pass
    else:
        connect_lcec_to_plumbing(6,3)


def connect_lcec_to_plumbing(joint_nr, slave_nr):
    # in my dev setup the 6th joint is slave 3
    #
    # first connect the feedback from the encoder to the plumbing
    # lcec.0.3.position-actual-value
    # this will then show the actual position in radians, and
    # take that once to set the position pin joint6_offset.in
    flt_to_s32 = 'joint%i_cmd_s32.out' % joint_nr
    s32_to_flt = 'joint%i_fb_flt.in' % joint_nr
    lcec_cmd = 'lcec.0.%i.target-position' % slave_nr
    lcec_fb =  'lcec.0.%i.position-actual-value' % slave_nr
    hal.Pin(flt_to_s32).link(lcec_cmd)
    hal.Pin(lcec_fb).link(s32_to_flt)


def connect_sim(st):
    for joint_nr in range(1,7):
        create_fb_simulation(st, joint_nr)


def setup_joints(st):
    # for each joint we need
    # - an offset (from the joints zero) either for when an encoder
    #   is not homed, or for finetuning manufacturing dimensions.
    # - a scale, converting the angle in radians to pulses per revolution
    #   of the output shaft. Consisting of PI, encoder resolution and ratio
    # - convert float to u32
    joints_config = ConfigParser.ConfigParser()
    directory = os.getcwd() + '/config'
    configfile = directory + '/joints.ini'
    joints_config.read(configfile) 
    # read joint offset from ini file
    for joint_nr in range(1,7):
        create_joint_plumbing(st, joint_nr)
        enc_scale = joints_config.get('joint%s' % joint_nr, 'encoder_scale')
        gearbox_i = joints_config.get('joint%s' % joint_nr, 'gear_ratio')
        set_joint_scale(joint_nr, float(enc_scale) * float(gearbox_i))


def instantiate_components(arguments):
    demosetup = arguments.demo
    testsetup = arguments.testsetup
    configfile = arguments.config
    # name of the servothread
    st = 'st'
    print('instantiating components')
    if demosetup == False:
        setup_lcec(configfile)
        # write lcec-read-all first
        hal.addf('lcec.read-all', st)
        # load other stuff
        setup_joints(st)
        connect_lcec(st, testsetup)
        # do some final writing of functions to the thread
        # write lcec-write-all last
        hal.addf('lcec.write-all', st)
    else:
        # create a demo joint for when EtherCAT not available
        setup_joints(st)
        connect_sim(st)

def add_components_to_thread():
    pass
