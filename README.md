# copyvols
clone 2 InfiniBox volumes <br>
the script creates a snapshot from the source volume and creates the destination volume. <br>
it than maps both to host and preforms xcopy operation, once completed it unmaps both volumes and delete the snapshot. <br>

## Prerequisites
this script uses infinisdk and infi.storagemodel python modules. <br>
HPT and sg_utils must be installed on the host. <br>

## Usage
copyvols.py -s vcopy1 -d copydest2 -u iscsi -i ibox149

