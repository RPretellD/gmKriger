# gmKriger

<b>gmKriger</b>: A Kriging-based ground motion intensity measure (GMIM) calculator. <b>gmKriger</b> computes GMIMs for past earthquake events given a site's location (latitude and longitude) and the site's Vs30. gmKriger uses Ordinary Kriging interpolation and spatial correlation model developed using a Bayesian approach, ground motion data, and the functional forms proposed by Bodenmann et al. (2023). 


## Ground motion intensity measures (GMIMs) and units

| GMIM                                  | Key         | Unit |
|---------------------------------------|-------------|------|
| Peak ground aceleration               | PGA         | g    |
| Peak ground velocity                  | PGV         | cm/s |
| Arias intensity                       | Ia          | m/s  |
| Cumulative absolute velocity          | CAV         | m/s  |
| Damage-potential CAV                  | CAVdp       | g-s  |
| Pseudo-spectral acceleration @ 0.1 s  | PSA(0.100)  | g    |
| Pseudo-spectral acceleration @ 0.3 s  | PSA(0.300)  | g    |
| Pseudo-spectral acceleration @ 0.6 s  | PSA(0.600)  | g    |
| Pseudo-spectral acceleration @ 1.0 s  | PSA(1.000)  | g    |
| Pseudo-spectral acceleration @ 3.0 s  | PSA(3.000)  | g    |
| Pseudo-spectral acceleration @ 6.0 s  | PSA(6.000)  | g    |
| Pseudo-spectral acceleration @ 10.0 s | PSA(10.000) | g    |


## Models available

Get them using [this code](https://github.com/RPretellD/gmKriger/blob/main/Examples/Get_models.ipynb).

The spatial correlation models for the events and ground motion intensity measures below are accessible via [DesignSafe](https://www.designsafe-ci.org/data/browser/public/designsafe.storage.published/PRJ-4022v2) (Pretell et al. 2023).

|           Earthquake           |   PGA    |   PGV    |    Ia    |   CAV    |  CAVdp   |
|--------------------------------|----------|----------|----------|----------|----------|
| 1968 M8.2 Tokachi-Oki          | No       | No       | Yes      | Yes      | No       |
| 1971 M6.6 San Fernando         | Yes      | Yes      | Yes      | Yes      | No       |
| 1978 M7.7 Miyagiken-Oki        | No       | No       | Yes      | Yes      | No       |
| 1979 M6.5 Imperial Valley      | Yes      | Yes      | Yes      | Yes      | No       |
| 1980 M6.3 Victoria             | Yes      | Yes      | Yes      | Yes      | No       |
| 1981 M5.9 Westmorland          | Yes      | Yes      | Yes      | Yes      | No       |
| 1983 M7.7 Nihonkai-Chubu       | No       | No       | Yes      | Yes      | No       |
| 1983 M6.8 Nihonkai-Chubu       | No       | No       | Yes      | Yes      | No       |
| 1987 M6.5 Superstition Hills   | Yes      | Yes      | Yes      | Yes      | No       |
| 1989 M6.9 Loma Prieta          | Yes      | Yes      | Yes      | Yes      | No       |
| 1993 M7.6 Kushiro-Oki Hokkaido | No       | No       | Yes      | Yes      | No       |
| 1994 M6.7 Northridge           | Yes      | Yes      | Yes      | Yes      | No       |
| 1994 M8.3 Toho-Oki Hokkaido    | No       | No       | Yes      | Yes      | No       |
| 1995 M6.9 Kobe                 | Yes      | Yes      | Yes      | Yes      | No       |
| 1999 M7.5 Kocaeli              | Yes      | Yes      | Yes      | Yes      | No       |
| 1999 M7.6 Chi-Chi              | Yes      | Yes      | Yes      | Yes      | No       |
| 2000 M6.6 Tottori              | Yes      | Yes      | Yes      | Yes      | No       |
| 2002 M5.0 Au Sable Forks       | No       | No       | No       | No       | No       |
| 2003 M8.3 Tokachi              | No       | No       | Yes      | Yes      | No       |
| 2007 M6.8 Chuetsu-oki          | Yes      | Yes      | Yes      | Yes      | No       |
| 2010 M7.2 El Mayor-Cucapah     | Yes      | Yes      | Yes      | Yes      | No       |
| 2010 M7.0 Darfield             | Yes      | Yes      | Yes      | Yes      | No       |
| 2010 M8.8 Maule                | No       | No       | Yes      | Yes      | No       |
| 2011 M6.2 Christchurch         | Yes      | Yes      | Yes      | Yes      | No       |
| 2011 M5.0 Christchurch         | Yes      | No       | No       | No       | No       |
| 2011 M6.0 Christchurch         | Yes      | Yes      | Yes      | Yes      | No       |
| 2011 M5.9 Lyttleton            | Yes      | Yes      | Yes      | Yes      | No       |
| 2011 M9.1 Tohoku-Oki           | No       | No       | Yes      | Yes      | No       |
| 2012 M6.1 Emilia               | Yes      | Yes      | Yes      | Yes      | No       |
| 2012 M6.0 Emilia               | Yes      | Yes      | Yes      | Yes      | No       |
| 2019 M7.06 Ridgecrest          | Yes      | Yes      | Yes      | Yes      | No       |
| 2019 M6.48 Ridgecrest          | Yes      | Yes      | Yes      | Yes      | No       |
| 2020 M7.0 Samos                | Yes      | Yes      | Yes      | Yes      | No       |
| 2023 M7.81 Pazarcik            | Yes      | Yes      | Yes      | Yes      | Yes      |
| 2023 M7.74 Kahramanmaras       | Yes      | Yes      | Yes      | Yes      | Yes      |
| 2023 M6.81 Nurdagi             | Yes      | Yes      | Yes      | Yes      | Yes      |
| 2023 M6.37 Yayladagi           | Yes      | Yes      | Yes      | Yes      | Yes      |

Also, PSA at several oscillator periods for some events: 

|           Earthquake           | PSA(0.100) | PSA(0.300) | PSA(0.600) | PSA(1.000) | PSA(3.000) | PSA(6.000) | PSA(10.000) |
|--------------------------------|------------|------------|------------|------------|------------|------------|-------------|
| 2023 M7.81 Pazarcik            | Yes        | Yes        | Yes        | Yes        | Yes        | Yes        | Yes         |
| 2023 M7.74 Kahramanmaras       | Yes        | Yes        | Yes        | Yes        | Yes        | Yes        | Yes         |
| 2023 M6.81 Nurdagi             | Yes        | Yes        | Yes        | Yes        | Yes        | Yes        | Yes         |
| 2023 M6.37 Yayladagi           | Yes        | Yes        | Yes        | Yes        | Yes        | Yes        | Yes         |

Note: The CAVdp values estimated by gmKriger require close attention. Some estimates might be unexpectedly high at R_JB > 100 km, when no seismic station is nearby. 


## Installation

Need the following packages:
```Python
pip install nvector
pip install torch
pip install geopy
pip install shapely
pip install nvector

pip install geostats
pip install gmms
pip install pygmm
pip install gmKriger
```


## How to use

### Inputs
<b>site:</b><br>Site ID(s) or site name(s).<br><br>
<b>latitude:</b><br>Site's latitude(s).<br><br>
<b>longitude:</b><br>Site's longitude(s).<br><br>
<b>Vs30:</b><br>Time-average shear-wave velocity in the top 30 m for the site(s).<br><br>
<b>earthquake:</b><br>Event from the available models (e.g., '1989 M6.9 Loma Prieta').<br><br>
<b>model:</b><br>
- ***realizations:*** To use 1000 spatial correlation models.<br>
- ***MAP:***          To use the maximum a posteriori spatial correlation model.<br>
- ***all:***          To use all the 1000 and the maximum a posteriori spatial correlation models.<br>

<b>gmim:</b><br>Ground motion intensity measure from the available models (e.g., 'PGA'). 


### Run
```Python
import gmKriger

site      = ['Alameda Naval Air Station', 'Treasure Island', 'Alameda Bay Farm Island', 'Farris Farm', 'POO7']
latitude  = [37.785748,37.8261394,37.73380567,36.91026828,37.805242]
longitude = [-122.309346,-122.3712351,-122.250101,-121.7437891,-122.339702]
Vs30      = [186.2,181.1,230.7,209.5,223]

earthquake = '1989 M6.9 Loma Prieta'
model      = 'realizations'
gmim       = 'PGA'

gmKriger.get_Kgmim(site,latitude,longitude,Vs30,earthquake,model,gmim)
```
| Site                      |   Lat (deg) |   Lon (deg) |   PGA (g) |   sigma_PGA (ln) |
|:--------------------------|------------:|------------:|----------:|-----------------:|
| Alameda Naval Air Station |     37.7857 |    -122.309 |  0.189312 |         0.386172 |
| Treasure Island           |     37.8261 |    -122.371 |  0.135361 |         0.273654 |
| Alameda Bay Farm Island   |     37.7338 |    -122.250 |  0.151978 |         0.429026 |
| Farris Farm               |     36.9103 |    -121.744 |  0.458404 |         0.494209 |
| POO7                      |     37.8052 |    -122.339 |  0.154422 |         0.350264 |


## Examples
- <b>Example 1:</b> Compute PGA for the 1989 Loma Prieta Earthquake using all the 1000 spatial correlation models. [here](https://github.com/RPretellD/gmKriger/blob/main/Examples/Example_1.ipynb).
- <b>Example 2:</b> Compute several ground motion intensity measures for the 2023 M7.8 Pazarcik Earthquake using the maximum aposteriori spatial correlation model. [here](https://github.com/RPretellD/gmKriger/blob/main/Examples/Example_2.ipynb).
- <b>Example 3:</b> Compute several ground motion intensity measures for the 1987 M6.5 Superstition Hills Earthquake all the 1000 and the maximum aposteriori spatial correlation model. [here](https://github.com/RPretellD/gmKriger/blob/main/Examples/Example_3.ipynb).


## Acknowledgements
- The implementation of gmKriger greatly benefitted from discussions with Scott J. Brandenberg and Jonathan P. Stewart.


## Citation
If you use these codes, please cite:<br>

> Pretell, R. (2023). RPretellD/gmKriger: Initial release (0.2.0). Zenodo. https://doi.org/10.5281/zenodo.10399419<br>

> Pretell, R., Brandenberg, S.J., and Stewart, J.P. "Optimizing ground motion intensity measures for soil liquefaction case histories." (In preparation). 

> Pretell, R., Brandenberg, S., and Stewart, J. (2023) "Consistently computed ground motion intensity measures for liquefaction triggering assessment." DesignSafe-CI. https://doi.org/10.17603/ds2-6vj1-t096 v2

[![DOI](https://zenodo.org/badge/732896925.svg)](https://zenodo.org/doi/10.5281/zenodo.10399418)


## Contact
For any questions or comments, contact Renmin Pretell at rpretell@unr.edu.