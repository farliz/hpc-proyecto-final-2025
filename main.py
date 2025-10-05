#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================
CURSO: HPC con Python // Instituto Gulich - 2025
===================================
Script para evaluar los resultados del cálculo del NDVI
==================================

exec:
    python main.py
"""

from pathlib import Path
import os

import matplotlib.pyplot as plt
import numpy as np

import src.dronepro.basic as basic

if __name__ == "__main__":

    idx=0
    output_path = "outputs_ndvi"
    output_files = [os.path.join(output_path, f) for f in os.listdir(output_path) if f.endswith('.npy')]
    ndvi = np.load(output_files[idx])

    print(Path(output_files[idx]).stem)
    print(ndvi.shape, ndvi.mean())

    basic.stats(ndvi)
    basic.show(ndvi)

