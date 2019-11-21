"""
PASS MESSAGE IN RING
"""
import sys
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    msg = input("Starting at P0, enter message: ")
else:
    msg = comm.recv(source=(rank-1)%4)

comm.send(msg, dest=(rank+1)%size)

if rank == 0:
    msg = comm.recv(source=(rank-1)%4)

print("Current P%d recieved message:%s from P%d"%(rank, msg, (rank-1)%size))
