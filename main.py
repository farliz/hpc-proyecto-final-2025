#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================
CURSO: HPC con Python // Instituto Gulich - 2025
===================================
Script para evaluar los resultad del cálculo del NDVI
==================================

exec:
    python main.py
"""

from pathlib import Path
import os

import matplotlib.pyplot as plt
import numpy as np

import src.dronepro.basic as basic

directory_path = "outputs_ndvi"
files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.npy')]

idx = 0
data = np.load(files[idx])
print(Path(files[idx]).stem)
print(data.shape, data.mean())
basic.stats(data)
basic.show(data)
