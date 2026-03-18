# gmKriger: Versions

### V0.1.0
- Initial release. 

### V0.2.0
- First working version, implemented based on formulation described in Pretell et al. (2024). 

### V1.0.0
- Implemented Pretell et al. (2026) formulation to address epistemic uncertainty in GMM selection. 
- Modified code to address installation issues. 
- Modified codes to leverages the Cython and Python implementations of [geostats](https://github.com/RPretellD/geostats) and [gmms](https://github.com/RPretellD/gmms). Set Cython implementations as default with fallback option to Python implementations. 
- Limited applications to PGA, PGV, Ia, and CAV only. 
- Other code changes to accommodate the above updates. 

### V1.1.0
- Passed Z_hyp to CB14 model. 
- Fixed some path issues encountered in Linux. 
- Fixed typo "Lyttleton" to "Lyttelton" in the data files. 
- Added backend selection capability (Cython or Python). Backend can also be extracted to confirm. 
- Other less important modifications. 

### V1.1.1
- Something went wrong with the v1.1.0 release on GitHub. Bumping version to keep consistency between GitHub and Zenodo. 
