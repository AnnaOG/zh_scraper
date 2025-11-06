# zh\_scraper

Python tool to scrape mean extinction (Av) and standard deviation values from the Zaritsky & Harris extinction maps of the SMC and LMC.

It queries data from the MCPS data products webpage:
[https://www.as.arizona.edu/\~dennis/mcsurvey/Data\_Products.html](https://www.as.arizona.edu/~dennis/mcsurvey/Data_Products.html)

Please cite [Zaritsky, Harris, Thompson, Grebel, and Massey 2002, AJ, 123, 855](https://ui.adsabs.harvard.edu/abs/2002AJ....123..855Z/abstract) (SMC) and/or [Zaritsky, Harris, Thompson, and Grebel, 2004, AJ, 128, 1606](https://ui.adsabs.harvard.edu/abs/2004AJ....128.1606Z/abstract) (LMC) if you use the data obtained from this package.

---

## Requirements

* Python 3.12.11 or higher (tested)
* Dependencies below listed in `requirements.txt`:
  * requests 2.28.0 or higher (tested)
  * beautifulsoup4 4.11.0 or higher (tested)

Install dependencies using pip:

```shell
pip install -r requirements.txt
```

---

## Installation

Clone the repo and install dependencies:

```shell
git clone https://github.com/AnnaOG/zh_scraper.git
cd zh_scraper
pip install -r requirements.txt
```

---

## Function Overview

**Function:**

```python
get_extinction(galaxy, ra, dec, radius, teff='all')
```

**Inputs:**

* `galaxy` (str): `"LMC"` or `"SMC"`  
* `ra` (float): Right Ascension in units of **hours** (decimal, e.g., 5.25 for 5h15m)  
* `dec` (float): Declination in units of **degrees** (decimal, e.g., -69.5 for -69°30′)  
* `radius` (float): Search radius in arcminutes (maximum 12)  
* `teff` (str): `'all'`, `'cool'`, or `'hot'` (default = `'all'`)

You can convert your coordinates to the correct units using the units and coordinates functions in the `astropy` package, or by using [Jan Skowron's flexible converter website](https://www.astrouw.edu.pl/~jskowron/ra-dec/).

**Returns:**

* `(mean_av, stdev_av)` as floats.
* Raises `ValueError` if no stars are found within the radius or if inputs are invalid.

---

## Usage Options

### 1. Command-Line Interface (CLI)

Run the script directly from a terminal:

```shell
python zh_scraper.py --galaxy SMC --ra 1.168 --dec -72.614 --radius 3 --teff all
```

For help and argument details:

```shell
python zh_scraper.py --help
```

### 2. Python Notebook or Script

Import and use the function in a Python notebook or script:

```python
from zh_scraper import get_extinction

mean_av, stdev_av = get_extinction('SMC', 1.168, -72.614, 3, teff='all')
print(mean_av, stdev_av)
```

To view the function docstring:

```python
help(get_extinction)
```
