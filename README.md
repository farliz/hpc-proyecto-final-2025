# CURSO: HPC con Python // Instituo Gulich - 2025
## PROYECTO FINAL: Cálculo de NDVI

Aplicación de MPI (Message Passing Interface) para procesamiento de imágenes. 

Author: Lizardo M. Reyna Bowen\
Email : lizardo.reyna@utm.edu.ec\
Ints. : Universidad Técnica de Manabí / Facultad de Ingeniería Agrícola\
Date  : 2025-09-19

## El índice de vegetación NDVI
El NDVI (Normalized Difference Vegetation Index) mide la cantidad y el
estado de la vegetación a partir de la intensidad con que las plantas
reflejan la luz en el espectro rojo (RED) y infrarrojo cercano
(NIR). En este caso las bandas o canales NIR (banda 4) y Red (banda 3)
son las requeridas para el cálculo.

- La vegetación sana absorbe gran parte de la luz roja (usada en la
  fotosíntesis) y refleja fuertemente la luz infrarroja cercana.
- La vegetación poco saludable o escasa refleja más luz roja y menos
  infrarroja.
  
$
  ndvi = \frac{nir-red}{nir + red}
$

*Interpretación referencial del NDVI:*\

| Valor NDVI | Condición de la vegetación   |
| ---------- | ---------------------------- |
| < 0.0      | Agua, nubes o nieve          |
| 0.0–0.2    | Suelo desnudo o rocas        |
| 0.2–0.4    | Vegetación escasa            |
| 0.4–0.6    | Vegetación moderada          |
| 0.6–1.0    | Vegetación densa y saludable |

## Directorio

```

├── data
│   └── orthophotos
│       ├── MIV-B2c-F3.jp2
│       ├── MIV-B2c-F4.jp2
│       ├── MIV-B2d-A1.jp2
│       ├── MIV-B2d-A2.jp2
│       ├── MIV-B2d-A3.jp2
│       └── MIV-B2d-A4.jp2
├── main.py
├── mpi_ndvi_ranks.py
├── mpi_ndvi_scatter.py
├── README.md
└── src
    └── dronepro
        ├── basic.py
        ├── __init__.py
		
```
**dronepro:** es un conjunto de funciones simples para procesar las imagenes.\
**rasterio:** (requerido) es una librería de python para cargar imágenes georeferenciadas\

## Ejecutar
```
mpiexec -n 8 python mpi_ndvi_ranks.py

python main.py
```
Este script calcula el NDVI a partir de una sola imagen.
```
mpiexec -n 8 python mpi_ndvi_scatter.py

python main.py
```
Este script calcacula el NDVI de un conjunto de imágenes que estan un mismo directorio.

**Formato:** el formato de las imágenes de entrada es jpg2000


nota:

Las imágenes utilizadas en este ejemplo pertenecen al Instituto Geográfico Militar del Ecuador.\
                            --para uso estrictamente académico--

Licencia:

    Copyright 2025, L. Reyna

    Copying and distribution of this file, with or without modification,
    are permitted in any medium without royalty, provided the copyright
    notice and this notice are preserved. This file is offered as-is,
    without any warranty.








