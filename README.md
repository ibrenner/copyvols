# copyvols
clone 2 InfiniBox volumes
the script creates a snapshot from the source volume and creates the destination volume.
it than maps both to host and preforms xcopy operation, once completed it unmaps both volumes and delete the snapshot.

## Prerequisites
this script used infinisdk and infi.storagemodel  modules


## Usage
copyvols.py -s vcopy1 -d copydest2 -u iscsi -i ibox149

