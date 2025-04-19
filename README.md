# Cambridge Core Merge

This is a python script to merge books downloaded from Cambridge Core into a single PDF file.

## Installation
```bash
uv tool install git+https://github.com/SinTan1729/cambridge-core-merge
```

## Usage
```bash
cambridge-core-merge [-h] -z ZIPFILE -n NAME [-c COVER]
```
Available options:
```bash
  -h, --help            show this help message and exit
  -z, --zipfile ZIPFILE
                        The path of the zip file obtained from Cambridge Core.
  -n, --name NAME       The path of the final PDF file.
  -c, --cover COVER     The path of the cover file. (Ideally JPG.)
```

[Link to the base repo.](https://git.sayantansantra.com/SinTan1729/cambridge-core-merge)
