import numpy as np
import math
import re
import glob
import os

RAD2DEG = 180.0/math.pi
DEG2RAD = math.pi/180.0

class Skypos:
    """Defines a class that works with spherical geometry, specifically points
    in a unit sphere, such as the sky.

    This is general spherical geometry, with little to tie it to astronomy. The
    exceptions are the naming of longitude and latitude as RA,Dec
    """
    def_precra = 3
    def_precde = 2

    def __init__(self, ra, dec, precra=def_precra, precdec=def_precde):
        """
        Initialise a Skypos object defining a point on a unit sphere with longitude ra and latitude dec
        :param ra: right ascension (radians or hh:mm:ss.ss)
        :type ra: float or str
        :param dec: declination (radians or dd:mm:ss.ss)
        :type dec: float or str
        :param precra:
        :param precdec:
        """
        if isinstance(ra, str):
            self.ra = ras_rad(ra)
            self.dec = decs_rad(dec)
        else:
            self.ra = ra
            self.dec = dec
        self.precra = precra
        self.precdec = precdec
        self.rn = 12+self.precra-Skypos.def_precra
        self.dn = 12+self.precdec-Skypos.def_precde
        self.ras = None
        self.decs = None
        ps = math.pi * 0.5 - self.dec
        sps = math.sin(ps)
        cps = math.cos(ps)
        sra = math.sin(self.ra)
        cra = math.cos(self.ra)
        self._dvecx = [cps * cra, cps * sra, -sps]
        self._dvecy = [-sra, cra, 0.0]
        self._dvecz = [sps * cra, sps * sra, cps]
        self._vec = [cra*sps, sra*sps, cps]

    def get_vec(self):
        return self._vec
        
    def d_pa(self, other):
        ra = other.ra
        dec = other.dec
        xyz = rd_xyz(ra, dec)
        d = None
        x = self._dvecx[0] * xyz[0] + self._dvecx[1] * xyz[1] \
            + self._dvecx[2] * xyz[2]
        y = self._dvecy[0] * xyz[0] + self._dvecy[1] * xyz[1] \
            + self._dvecy[2] * xyz[2]
        z = self._dvecz[0] * xyz[0] + self._dvecz[1] * xyz[1] \
            + self._dvecz[2] * xyz[2]
        z = max(-1.0, min(z, 1.0))
        try:
            d = math.pi * 0.5 - math.asin(z)
        except ValueError:
            logger.error("Can't perform asin(z) on z = {}, math domain error".format(z))
        pa = math.atan2(y, -x)
        return d, pa

    def offset(self, dpa):
        a2 = math.pi * 0.5 - dpa[0]
        a1 = -(math.pi + dpa[1])
        xyz = rd_xyz(a1, a2)
        x = self._dvecx[0] * xyz[0] + self._dvecy[0] * xyz[1] + \
            self._dvecz[0] * xyz[2]
        y = self._dvecx[1] * xyz[0] + self._dvecy[1] * xyz[1] + \
            self._dvecz[1] * xyz[2]
        z = self._dvecx[2] * xyz[0] + self._dvecy[2] * xyz[1] + \
            self._dvecz[2] * xyz[2]
        b2 = math.asin(z)
        b1 = (2.0 * math.pi + math.atan2(y, x)) % (2.0 * math.pi)
        return Skypos(b1, b2)

    # noinspection PyUnresolvedReferences
    def separation(self, other):
        """
        Return great circle angular separation between this Skypos and another
        :param other: position on the sky to determine separation to
        :type other: `:class:Skypos`
        :return: separation angle (radians)
        """

        if self.dec == other.dec:
            if self.ra == other.ra:
                return 0.

        # vincenty formula (https://en.wikipedia.org/wiki/Great-circle_distance)
        dra = np.abs(self.ra-other.ra)
        sep = np.arctan2(np.sqrt((np.cos(other.dec)*np.sin(dra))**2
                         + (np.cos(self.dec)*np.sin(other.dec)
                         - np.sin(self.dec)*np.cos(other.dec)*np.cos(dra))**2),
                         np.sin(self.dec)*np.sin(other.dec) + np.cos(self.dec)*np.cos(other.dec)*np.cos(dra))

        return sep

    def rotate_x(self, a):
        """return a skypos determined by rotating self about the X-axis by 
        angle a."""
        x, y, z = _rotate_v_x(self._vec, a)
        b2 = math.asin(z)
        b1 = (2 * math.pi + math.atan2(y, x)) % (2.0 * math.pi)
        return Skypos(b1, b2)

    def rotate_y(self, a):
        """return a skypos determined by rotating self about the X-axis by 
        angle a."""
        x, y, z = _rotatev_y(self._vec, a)
        b2 = math.asin(z)
        b1 = (2 * math.pi + math.atan2(y, x)) % (2.0 * math.pi)
        return Skypos(b1, b2)

    def rotate_z(self, a):
        """return a skypos determined by rotating self about the X-axis by 
        angle a."""
        x, y, z = _rotate_v_z(self._vec, a)
        b2 = math.asin(z)
        b1 = (2 * math.pi + math.atan2(y, x)) % (2.0 * math.pi)
        return Skypos(b1, b2)

    def shift(self, delta_lon, delta_lat):
        """
        Shift this direction (Skypos) in longitude and latitude.
        The longitude shift will be in radian units perpendicular to the direction to pole, along a great circle.
 
        :param float delta_lon: longitude (RA) offset in radians
        :param float delta_lat: latitude (DEC) offset in radians
        """
        lat = self.dec
        lon = self.ra
        # vector along X axis (first point of Aries)
        x0 = Skypos('0h0m0s', '0:0:0', 3, 3)
        shifted_direction = x0.rotate_z(delta_lon).rotate_y(lat + delta_lat).rotate_z(lon)
        return shifted_direction

    def get_ras(self):
        if self.ras is None:
            self.ras = ras(self.ra)
            self.decs = decs(self.dec)
        return self.ras[:self.rn]

    def get_decs(self):
        if self.ras is None:
            self.ras = ras(self.ra)
            self.decs = decs(self.dec)
        return self.decs[:self.dn]

    def __str__(self):
        return '{} {}'.format(self.get_ras(), self.get_decs())

def ras(ra):
    s = ra * (4.0 * 60.0 * RAD2DEG)
    hh = int(s / 3600.0)
    mm = int(s / 60.0) - hh * 60
    ss = s - 60 * (mm + 60 * hh)
    if "{:9.6f}".format(ss) == '60.000000':
        ss = 0.0
        mm += 1
        if mm == 60:
            mm = 0
            hh += 1
            if hh == 24:
                hh = 0
    return "%02d:%02d:%09.6f" % (hh, mm, ss)


def decs(dec):
    s = abs(dec) * (60.0 * 60.0 * RAD2DEG)
    dd = int(s / 3600.0)
    mm = int(s / 60.0) - dd * 60
    ss = s - 60 * (mm + 60 * dd)
    if "%8.5f" % ss == '60.00000':
        ss = 0.0
        mm += 1
        if mm == 60:
            mm = 0
            dd += 1
    sign = ' '
    if dec < 0.0:
        sign = '-'
    return "%s%02d:%02d:%08.6f" % (sign, dd, mm, ss)

def _rotate_v_x(vec, a):
    """Return a skypos determined by rotating vec about the X-axis by 
    angle a."""
    ca, sa = math.cos(a), math.sin(a)
    x = vec[0]
    y = vec[1] * ca - vec[2] * sa
    z = vec[1] * sa + vec[2] * ca
    return [x, y, z]


def _rotatev_y(vec, a):
    """Return a skypos determined by rotating vec about the Y-axis by 
    angle a."""
    ca, sa = math.cos(a), math.sin(a)
    x = vec[0] * ca - vec[2] * sa
    y = vec[1]
    z = vec[0] * sa + vec[2] * ca
    return [x, y, z]


def _rotate_v_z(vec, a):
    """Return a skypos determined by rotating vec about the Z-axis by 
    angle a."""
    ca, sa = math.cos(a), math.sin(a)
    x = vec[0] * ca - vec[1] * sa
    y = vec[0] * sa + vec[1] * ca
    z = vec[2]
    return [x, y, z]


def ras_rad(ra_string):
    """
    Convert right ascension string to radians
    :param ra_string: right ascension string (hh:mm:ss.ss)
    :type ra_string: str
    :return: right ascension in radians
    :rtype: float
    """
    if ra_string[0] == '-':
        raise ValueError('Right ascension may not be negative: {}'.format(ra_string))
    (a, b, c) = re.findall("[0-9.]+", ra_string)
    hh, mm = list(map(int, [a, b]))
    ss = float(c)
    return (ss + 60.0 * (mm + 60.0 * hh)) * 2.0 * math.pi / 86400.0


def decs_rad(dec_string):
    """
    Convert declination string to radians
    :param dec_string: declination string (dd:mm:ss.ss)
    :type dec_string: str
    :return: declination in radians
    :rtype: float
    """
    a, b, c = re.findall('[0-9.]+', dec_string)
    dd, mm = list(map(int, [a, b]))
    ss = float(c)
    r = (ss + 60.0 * (mm + 60.0 * dd)) * 2.0 * math.pi / 1296000.0
    if dec_string[0] == '-':
        r = -r
    return r


def dp_to_lm(dp):
    """
    Given a distance, position_angle offset relative to a sky position,
    return the equivalent (l,m)

    :param dp: distance, position_angle offset
    :return: rectangular offset

    """
    #
    x = math.sin(dp[0]) * math.sin(dp[1])
    y = math.sin(dp[0]) * math.cos(dp[1])
    return x, y


def lm_to_dp(lm):
    """
    Given an (l,m) rectangular offset relative to a sky position,
    return the equivalent distance,position angle

    :param lm: rectangular offset
    :return:  distance,position angle
    """
    p = math.atan2(lm[0], lm[1])
    d = math.asin(math.sqrt(lm[0] * lm[0] + lm[1] * lm[1]))
    return d, p


def lm_to_true(lm):
    """
    Given an (l,m) rectangular offset relative to a sky position,
    return the equivalent true angle offsets in the antenna frame
    as used by casa ms

    :param lm: rectangular offset (orthographic projection)
    :return:  true angle offsets a,b (radians)
    """

    # note, adding zero to avoid -0.0000 representation of zero breaking tests
    a = math.asin(lm[0])
    b = math.atan2(lm[1], math.cos(math.asin(math.sqrt(lm[0]**2 + lm[1]**2))))

    return [a+0, b+0]


def rd_xyz(ra, dec):
    """TBD"""
    v = [math.cos(ra) * math.cos(dec), math.sin(ra) * math.cos(dec),
         math.sin(dec)]
    return v

