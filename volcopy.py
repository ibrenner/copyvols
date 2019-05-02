from infinisdk import InfiniBox
import argparse
import getpass
import os

def get_args():
    """
    Supports the command-line arguments listed below.
    """
    parser = argparse.ArgumentParser(description="Failover and cleanup script for AA Demo.")
    parser.add_argument('-s', '--srcvol', required=False, help='source volume name', type=str)
    parser.add_argument('-d', '--dstvol', required=False, help='destination volume name', type=str)
    parser.add_argument('-u', '--user', required=False, help='ibox username', type=str)
    # parser.add_argument('-p', '--password', required=False, help='ibox password', type=str)
    parser.add_argument('-i', '--ibox', required=False, help='ibox', type=str)
    args = parser.parse_args()
    return args

def infirescan():
    from subprocess import check_output,CalledProcessError,PIPE
    retcode = 0
    try:
        print("rescanning...")
        output = check_output("infinihost rescan",shell=True,stderr=PIPE)
    except CalledProcessError as e:
        retcode = e.returncode

def get_vol(vol):
    return (system.volumes.find(name=vol)).to_list()

def check_vol(dst_vol):
    if dst_vol:
        return 
    return system.volumes.create(name=args.dstvol, pool=src_vol[0].get_pool(), size=src_vol[0].get_size())

def create_snap():
    snap=src_vol[0].create_child(name='{}_tempclone'.format(src_vol[0].get_name()))
    snap.disable_write_protection()
    map_vol("map",snap.get_name())
    return snap

def map_vol(op,vol):
    from subprocess import check_output,CalledProcessError,PIPE
    retcode = 0
    try:
        output = check_output("infinihost volume {} {} --system={} --yes".format(op,vol,args.ibox),shell=True,stderr=PIPE)
    except CalledProcessError as e:
        retcode = e.returncode

def vlist():
    from infi.storagemodel.vendor.infinidat.shortcuts import get_infinidat_block_devices
    infivols = get_infinidat_block_devices()
    return infivols

def vol_compare(vol1, infivols):
    for vol in infivols:
        if vol1 == vol.get_vendor().get_volume_name():
            return vol.get_device_mapper_access_path()
            


def compilecmd(src,dst):
    cmd = 'sg_xcopy if={} of={} bpt=16384'.format(src,dst)
    return cmd
    

if __name__ == '__main__':
    args = get_args()
    password = getpass.getpass('enter password: ')
    system = InfiniBox(args.ibox, auth=(args.user,password))
    system.login()
    src_vol = get_vol(args.srcvol)
    dst_vol = get_vol(args.dstvol)
    new_vol = check_vol(dst_vol)
    if new_vol:
        print("creating and mapping snapshot")
        snap = create_snap()
        print("creating new volume")
        map_vol("map",new_vol.get_name())
    else:
        print("volume already exist, please use another name")
        exit(1)
    infirescan()
    infivols = vlist()
    source_vol = vol_compare(snap.get_name(), infivols) 
    target_vol = vol_compare(new_vol.get_name(), infivols)
    print("starting copy, please wait...")
    cmd=compilecmd(source_vol,target_vol)
    os.system(cmd)
    print("copy finished, cleaning up")
    map_vol("unmap",snap.get_name())
    map_vol("unmap",new_vol.get_name())
    snap.delete()


