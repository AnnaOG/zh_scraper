# Requirements

import requests
from bs4 import BeautifulSoup

__all__ = ['get_extinction']

def get_extinction(galaxy, ra, dec, radius, teff='all'):
    """
    Query the Zaritsky & Harris dust extinction map for LMC or SMC at https://www.as.arizona.edu/~dennis/mcsurvey/Data_Products.html.
    Please cite Zaritsky, Harris, Thompson, Grebel, and Massey 2002, AJ, 123, 855
    and/or Zaritsky, Harris, Thompson, and Grebel, 2004, AJ, 128, 1606 if used.

    Parameters:
    galaxy : string
        'LMC' or 'SMC'
    ra : float
        Right Ascension in units of hours
    dec : float
        Declination in units of degrees
    radius : float
        Search radius (max 12 arcminutes)
    teff : string, optional
        'all', 'cool', or 'hot', default is all

    Returns:
    mean_av, stdev_av : tuple of floats or None
        Mean extinction Av and standard deviation within the radius if found, else None
    
    Raises:
    ValueError
        If inputs are invalid or no stars found within the radius.
    """

    galaxy = galaxy.upper()

    # Validate galaxy and coordinate ranges
    if not (type(ra) in {float,int}):
        raise ValueError("RA must be in units of hours, and a float or integer (e.g. 4.50, not 04:30:00)")
    if not (type(dec) in {float,int}):
        raise ValueError("Dec must be in units of degrees, and a float or integer (e.g. -69.50, not -69:30:00)")
    
    if galaxy == 'LMC':
        base_url = 'https://www.as.arizona.edu/~dennis/cgi-bin/lmcext.cgi'
        if (ra > 7.0):
            raise ValueError("RA must be in units of hours, not degrees (e.g. 5.20 (hours), not 78.0 (degrees))")
        if not (4.48 <= ra <= 6.27):
            raise ValueError("For LMC, RA must be between 4.48 and 6.27 hours.")
        if not (-72.5 <= dec <= -65.2):
            raise ValueError("For LMC, Dec must be between -72.5 and -65.2 degrees.")

    elif galaxy == 'SMC':
        base_url = 'https://www.as.arizona.edu/~dennis/cgi-bin/smcext.cgi'
        if (ra > 6.0):
            raise ValueError("RA must be in units of hours, not degrees (e.g. 0.75 (hours), not 11.25 (degrees))")
        if not (0.375 <= ra <= 1.375):
            raise ValueError("For SMC, RA must be between 0.375 and 1.375 hours.")
        if not (-74.9 <= dec <= -70.4):
            raise ValueError("For SMC, Dec must be between -74.9 and -70.4 degrees.")

    else:
        raise ValueError("Galaxy must be 'LMC' or 'SMC'.")

    if not (0 < radius <= 12):
        raise ValueError("Radius must be greater than 0 and no more than 12 arcminutes.")

    if teff not in {'all', 'cool', 'hot'}:
        raise ValueError("teff must be 'all', 'cool', or 'hot'.")

    params = {
        'ra': ra,
        'dec': dec,
        'searchrad': radius,
        'teff': teff
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    mean_av = None
    stdev_av = None

    for line in soup.get_text().splitlines():
        line = line.strip()
        if "<Av> =" in line:
            try:
                mean_av = float(line.split('=')[1].split()[0])
            except (ValueError, IndexError):
                continue
        elif "Standard deviation of extinction values =" in line:
            try:
                stdev_av = float(line.split('=')[1].split()[0])
            except (ValueError, IndexError):
                continue

    if mean_av is not None and stdev_av is not None:
        return mean_av, stdev_av
    else:
        raise ValueError("No stars found within the given radius. Try increasing the radius.")

# Script  usage:

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Query Harris & Zaritsky dust extinction maps for LMC/SMC. Returns Av and standard deviation.")
    parser.add_argument("--galaxy", required=True, choices=["LMC", "SMC"], help="Galaxy name: LMC or SMC")
    parser.add_argument("--ra", required=True, type=float, help="Right Ascension in hours")
    parser.add_argument("--dec", required=True, type=float, help="Declination in degrees")
    parser.add_argument("--radius", required=True, type=float, help="Search radius (max 12 arcminutes)")
    parser.add_argument("--teff", choices=["all", "cool", "hot"], default="all", help="Temperature selection, default is all")

    args = parser.parse_args()

    try:
        mean_av, stdev_av = get_extinction(
            galaxy=args.galaxy,
            ra=args.ra,
            dec=args.dec,
            radius=args.radius,
            teff=args.teff
        )
        print(f"Mean Av: {mean_av} mag, Standard deviation: {stdev_av} mag")
    except ValueError as e:
        print(f"Input error: {e}")
    except requests.RequestException as e:
        print(f"Request error: {e}")

