# CURSO: HPC con Python // Instituo Gulich - 2025
## PROYECTO FINAL: Cálculo de NDVI

Aplicación de MPI (Message Passing Interface) para procesamiento de imágenes. 

Author: Lizardo M. Reyna Bowen

Email : lizardo.reyna@utm.edu.ec\
Ints. : Universidad Técnica de Manabí / Facultad de Ingeniería Agrícola\
Date  : 2025-09-19

## Ejecutar
```
mpiexec -n 8 python mpi_ndvi_ranks.py

python main.py

mpiexec -n 8 python mpi_ndvi_scatter.py

python main.py
```


nota:

Las imágenes utilizadas en este ejemplo pertenecen al Insituto Geográfico Militar del Ecuador.
                            --para uso estrictamente académico--

Licencia:

    Copyright 2025, L. Reyna

    Copying and distribution of this file, with or without modification,
    are permitted in any medium without royalty, provided the copyright
    notice and this notice are preserved. This file is offered as-is,
    without any warranty.







