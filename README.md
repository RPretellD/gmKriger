# gmms: Ground Motion Models (GMMs) and supporting tools

This repository provides a ground motion models (GMMs) and supporting tools. The models are listed below, and the tools include codes for computing the distances required in GMMs. 

| Ground motion model           | Ground motion intensity measure                                             |
|-------------------------------|-----------------------------------------------------------------------------|
| Campbell & Bozorgnia (2010)   | Geometric mean horizontal standardized cumulative absolute velocity (CAVgm) |
| Campbell & Bozorgnia (2011)   | Damage-potential cumulative absolute velocity (CAVdp)                       |
| Campbell & Bozorgnia (2019)   | Arias intensity (Ia)                                                        |
| Campbell & Bozorgnia (2019)   | Cumulative absolute velocity (CAV)                                          |
| Foulser-Piggott & Goda (2015) | Arias Intensity (Ia)                                                        |
| Foulser-Piggott & Goda (2015) | Cumulative absolute velocity (CAV)                                          |


## Example
Three examples on Jupyter Notebooks are presented:
- [Example 1](https://github.com/RPretellD/gmms/blob/main/Examples/Example1.ipynb): Use of Campbell and Bozorgnia models for the 1989 Loma Prieta Earthquake (single-segment fault). En español [aquí](https://github.com/RPretellD/gmms/blob/main/Ejemplos/Ejemplo1.ipynb).
- [Example 2](https://github.com/RPretellD/gmms/blob/main/Examples/Example2.ipynb): Use of Campbell and Bozorgnia models for the 2023 Pazarcik Earthquake (multi-segment fault). En español [aquí](https://github.com/RPretellD/gmms/blob/main/Ejemplos/Ejemplo2.ipynb).
- [Example 3](https://github.com/RPretellD/gmms/blob/main/Examples/Example3.ipynb): Use of the Foulser-Piggott and Goda models for the 2003 Tokachi Earthquake. En español [aquí](https://github.com/RPretellD/gmms/blob/main/Ejemplos/Ejemplo3.ipynb).


## Acknowledgements
- The cython codes for the estimation of Joyner-Boore and rupture distances are based on Pengfei Wang's [R implementations](https://github.com/wltcwpf/RPSHA/blob/main/R/distance_calc.R).


## References
- Campbell KW and Bozorgnia Y (2010) A ground motion prediction equation for the horizontal component of cumulative absolute velocity (CAV) based on the PEER-NGA strong motion database. Earthquake Spectra 26(3): 635–650. 
- Campbell KW and Bozorgnia Y (2011) Prediction equations for the standardized version of cumulative absolute velocity as adapted for use in the shutdown of U.S. nuclear power plants. Nuclear Engineering and Design 241(2011): 2558–2569. 
- Campbell KW and Bozorgnia Y (2019) Ground motion models for the horizontal components of Arias intensity (AI) and cumulative absolute velocity (CAV) using the NGA-West2 Database. Earthquake Spectra 35(3): 1289–1310. 
- Foulser‐Piggott R and Goda K (2015) Ground‐motion prediction models for Arias intensity and cumulative absolute velocity for Japanese earthquakes considering single‐station sigma and within‐event spatial correlation. Bulletin of the Seismological Society of America 105 (4): 1903–1918. 


## Citation
If you use these codes, please cite:<br>
Pretell, R. (2023). gmms: Ground motion models and supporting tools (0.1.1). Zenodo. http://doi.org/10.5281/zenodo.10397816<br>

[![DOI](https://zenodo.org/badge/716445161.svg)](https://zenodo.org/doi/10.5281/zenodo.10127854)

## Contact
For any questions or comments, contact Renmin Pretell at rpretell@unr.edu.