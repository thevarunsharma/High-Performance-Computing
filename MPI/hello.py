#!/usr/bin/env python
"""
Parallel Hello World
"""
# Run using:
# mpiexec -n 4 ipython hello.py
# here 4 is the number of processors

from mpi4py import MPI
import sys

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()

sys.stdout.write(
    "Hello, World! I am process %d of %d on %s.\n"
    % (rank, size, name))
