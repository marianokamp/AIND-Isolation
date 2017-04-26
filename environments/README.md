# aind


### Conda

Creating conda environment:
`create -n py2 python=2 and conda create -n py3 python=3`

Capturing current state of installed packages in environment:
`conda env export > environment.yaml`

Creating environment from captured state:
`conda env create -f environment.yaml`

For aind:
`conda env create -f environments/aind-environment-macos.yml`
`source activate aind`
