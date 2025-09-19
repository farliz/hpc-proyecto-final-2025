"""
basic.py: a simple module for auv image processing

"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

import rasterio
from rasterio.plot import show


def load(file):
    
    dataset = rasterio.open(file)
    rows, cols = dataset.height, dataset.width
    b1 = np.zeros((rows, cols), dtype=np.int16)
    b2 = np.zeros((rows, cols), dtype=np.int16)
    b3 = np.zeros((rows, cols), dtype=np.int16)
    b4 = np.zeros((rows, cols), dtype=np.int16)
    
    if dataset.count == 1:
        return dataset
    else:
        b1 = dataset.read(1)
        b2 = dataset.read(2)
        b3 = dataset.read(3)
        b4 = dataset.read(4)
        return b1, b2, b3, b4

def chunk_rows(arr, n):
    return np.array_split(arr, n, axis=0)

def ndvi(b4, b3):
    return (b4 - b3.astype(np.float32)) / (b4 + b3.astype(np.float32) + 1e-9)

def stats(arr:np.ndarray):
    print(f"Band shape:\t{arr.shape}")
    print(f"Band dtype:\t{arr.dtype}")
    print(f"Band mean:\t{arr.mean():.3f}")
    print(f"Min.:\t{arr.min():.3f}")
    print(f"Max.:\t{arr.max():.3f}")

def save(arr, base_name, out_dir: Path):
    """Save NDVI as .npy float32."""
    npy_path = out_dir / f"{base_name}_ndvi_float32.npy"
    np.save(npy_path, arr.astype(np.float32))

def show(arr: np.ndarray, cmap='PRGn'):
    
    fig, ax = plt.subplots()
    m = ax.imshow(arr, cmap=cmap)
    fig.colorbar(m)
    ax.set_axis_off()
    plt.show()
    

