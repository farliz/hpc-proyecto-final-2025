#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================
CURSO: HPC con Python // Instituo Gulich - 2025
===================================
PROYECTO FINAL: Cálculo de NDVI
==================================
MPI (Message Passing Interface)
Parallelize across images
scatter/gather

Este script calcula el NDVI a partir de una lista de imágenes aéreas
que contienen 4 bandas; r, g, b, nir.

flujo del proceso:

    - obtner una lista con las imágenes del directorio
    - cargar y particiona las imagenes
    - distribuye el los datos a los procesos
    - calcula el NDVI (embarrassingly parallel)
    - colecta los resultados en root
    - reconstruir la matriz/imagen
    - guardar en formato .npy

exec:
    mpiexec -n 8 python mpi_ndvi_scatter.py

result:

    Processing: data/orthophotos/MIV-B2c-F3.jp2
    NDVI shape: (7679, 7729)

    Processing: data/orthophotos/MIV-B2c-F4.jp2
    NDVI shape: (7679, 7729)

    Processing: data/orthophotos/MIV-B2d-A1.jp2
    NDVI shape: (7679, 7729)

    Processing: data/orthophotos/MIV-B2d-A2.jp2
    NDVI shape: (7679, 7729)

    Processing: data/orthophotos/MIV-B2d-A3.jp2
    NDVI shape: (7679, 7729)

    Processing: data/orthophotos/MIV-B2d-A4.jp2
    NDVI shape: (7679, 7729)

output:

    output_ndvi/
     MIV-B2c-F3_ndvi_float32.npy
     MIV-B2c-F4_ndvi_float32.npy
     MIV-B2d-A1_ndvi_float32.npy
     MIV-B2d-A2_ndvi_float32.npy
     MIV-B2d-A3_ndvi_float32.npy
     MIV-B2d-A4_ndvi_float32.npy

Author: Lizardo M. Reyna Bowen
Email : lizardo.reyna@utm.edu.ec
Inst. : Universidad Técnica de Manabí / Facultad de Ingeniería Agrícola
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

from mpi4py import MPI
import os
from pathlib import Path

import numpy as np

from src.dronepro import basic

directory_path = "data/orthophotos"
out_dir = Path("outputs_ndvi")
out_dir.mkdir(parents=True, exist_ok=True)

files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.jp2')]


if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nprocs = comm.Get_size()


    for file in files:
        base = Path(file).stem
        if rank == 0:
            print(f"\nProcessing: {file}")
            b1, b2, b3, b4 = basic.load(file)

            # Split rows across workers (nprocs-1 workers)
            blocks_b4 = basic.chunk_rows(b4, nprocs)
            blocks_b3 = basic.chunk_rows(b3, nprocs)

        else:
            blocks_b4 = None
            blocks_b3 = None

        # Scatter chunks to all ranks
        my_b4 = comm.scatter(blocks_b4, root=0)
        my_b3 = comm.scatter(blocks_b3, root=0)

        # Compute local NDVI
        my_ndvi = basic.ndvi(my_b4, my_b3)

        # Gather NDVI blocks
        ndvi_blocks = comm.gather(my_ndvi, root=0)

        if rank == 0:
            ndvi = np.vstack(ndvi_blocks)
            print(f"NDVI shape: {ndvi.shape}")

            # Save outputs for this image
            basic.save(ndvi, base_name=base, out_dir=out_dir)

