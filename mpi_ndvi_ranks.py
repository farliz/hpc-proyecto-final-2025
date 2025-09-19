#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""==================================
CURSO: HPC con Python // Instituo Gulich - 2025
===================================
PROYECTO FINAL: Cálculo de NDVI
==================================
MPI (Message Passing Interface)
point-to-point send/recv


Este script calcula el NDVI a partir de una imagen aerea que contiene
4 bandas; r, g, b, nir.

flujo del proceso:

    - obtner una lista con las imágenes del directorio
    - cargar una imagen de la lista
    - separar las bandas
    - fraccionar las bandas nir y  r en n partes (n=número de procesos)
    - enviar a calcular el ndvi cada parte e imprimir el promedio y número de proceso
    - reconstruir la matriz
    - guardar en formato .npy

exec:
    mpiexec -n 8 python mpi_ndvi_ranks.py

result con idx=0:

     NDVI mean:0.273364782333374, array shape:(1097, 7729), rank:1
     NDVI mean:0.28310343623161316, array shape:(1097, 7729), rank:2
     NDVI mean:0.26648253202438354, array shape:(1097, 7729), rank:3
     NDVI mean:0.24006535112857819, array shape:(1097, 7729), rank:4
     NDVI mean:0.26734060049057007, array shape:(1097, 7729), rank:5
     NDVI mean:0.27270129323005676, array shape:(1097, 7729), rank:6
     NDVI mean:0.2884851396083832, array shape:(1097, 7729), rank:7
     Full NDVI shape: (7679, 7729)
     total time:0.5831 seconds

output:

    output_ndvi/MIV-B2c-F3_ndvi_float32.npy

Author: Lizardo M. Reyna Bowen
Email : lizardo.reyna@utm.edu.ec
Ints. : Universidad Técnica de Manabí / Facultad de Ingeniería Agrícola
Date  : 2025-09-19

nota:

    Las imágenes utilizadas en este ejemplo pertenecen al Insituto Geográfico Militar del Ecuador.
                              --para uso estrictamente académico--
Licencia:

    Copyright 2025, L. Reyna

    Copying and distribution of this file, with or without modification,
    are permitted in any medium without royalty, provided the copyright
    notice and this notice are preserved. This file is offered as-is,
    without any warranty.
"""




from pathlib import Path
import os
import sys
import time

from mpi4py import MPI
import matplotlib.pyplot as plt
import numpy as np

from src.dronepro import basic

directory_path = "data/orthophotos"
files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.jp2')] 


idx=0
b1, b2, b3, b4 = basic.load(files[idx])

if __name__ == '__main__':
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nprocs = comm.Get_size()
    
    start = MPI.Wtime()

    # Split rows across workers (nprocs-1 workers)
    blocks_b4 = basic.chunk_rows(b4, max(nprocs - 1, 1))
    blocks_b3 = basic.chunk_rows(b3, max(nprocs - 1, 1))
    
    if rank == 0:
     # Send data
        for r in range(1, nprocs):
            data = (blocks_b4[r-1], blocks_b3[r-1])
            comm.send(data, dest=r, tag=0)

        # Collect results
        ndvi_blocks = []
        for r in range(1, nprocs):
            block_ndvi = comm.recv(source=r, tag=1)
            ndvi_blocks.append(block_ndvi)

        # Rebuild full NDVI by stacking along rows
        ndvi = np.vstack(ndvi_blocks)

        end = MPI.Wtime()
        print(f"Full NDVI shape: {ndvi.shape}")
        print(f"total time:{end-start:.4f} seconds")

        # ---------- SAVE OUTPUTS ----------
        out_dir = Path("outputs_ndvi")
        out_dir.mkdir(parents=True, exist_ok=True)
        base = Path(files[idx]).stem  # name of the input jp2 without extension

        # Save raw float array as .npy (best for later processing)
        basic.save(ndvi, base_name=base, out_dir=out_dir)
        # print(basic.istats(ndvi))
        

    else:
        # Worker computes its NDVI block
        data = comm.recv(source=0, tag=0)
        _ndvi = basic.ndvi(data[0], data[1])
        print(f"NDVI mean:{_ndvi.mean()}, array shape:{_ndvi.shape}, rank:{rank}")
        
        # Send block back to rank 0
        comm.send(_ndvi, dest=0, tag=1)



