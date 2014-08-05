import signal_id.noise as noise
import scipy.stats as ss
import numpy as np
from spectral_cube import SpectralCube,BooleanArrayMask
from astropy.wcs import wcs
from astropy.io import fits
HEADER_STR = \
    """SIMPLE  =                    T / Written by IDL:  Fri Feb 20 13:46:36 2009      BITPIX  =                  -32  /                                               NAXIS   =                    3  /                                               NAXIS1  =                 1884  /                                               NAXIS2  =                 2606  /                                               NAXIS3  =                  200 //                                               EXTEND  =                    T  /                                               BSCALE  =    1.00000000000E+00  /                                               BZERO   =    0.00000000000E+00  /                                               BLANK   =                   -1  /                                               TELESCOP= 'VLA     '  /                                                         CDELT1  =   -5.55555561268E-04  /                                               CRPIX1  =    1.37300000000E+03  /                                               CRVAL1  =    2.31837500515E+01  /                                               CTYPE1  = 'RA---SIN'  /                                                         CDELT2  =    5.55555561268E-04  /                                               CRPIX2  =    1.15200000000E+03  /                                               CRVAL2  =    3.05765277962E+01  /                                               CTYPE2  = 'DEC--SIN'  /                                                         CDELT3  =    1.28821496879E+03  /                                               CRPIX3  =    1.00000000000E+00  /                                               CRVAL3  =   -3.21214698632E+05  /                                               CTYPE3  = 'VELO-HEL'  /                                                         DATE-OBS= '1998-06-18T16:30:25.4'  /                                            RESTFREQ=    1.42040571841E+09  /                                               CELLSCAL= 'CONSTANT'  /                                                         BUNIT   = 'JY/BEAM '  /                                                         EPOCH   =    2.00000000000E+03  /                                               OBJECT  = 'M33     '           /                                                OBSERVER= 'AT206   '  /                                                         VOBS    =   -2.57256763070E+01  /                                               LTYPE   = 'channel '  /                                                         LSTART  =    2.15000000000E+02  /                                               LWIDTH  =    1.00000000000E+00  /                                               LSTEP   =    1.00000000000E+00  /                                               BTYPE   = 'intensity'  /                                                        DATAMIN =   -6.57081836835E-03  /                                               DATAMAX =    1.52362231165E-02  /     """

np.random.seed(8675309)
data = np.random.randn(3, 4, 5)
mask = np.ones((3, 4, 5), dtype='bool')
h = fits.header.Header.fromstring(HEADER_STR)
h['NAXIS1'] = 5
h['NAXIS2'] = 4
h['NAXIS3'] = 3
h['NAXIS4'] = 1


def test_mad():
    assert noise.mad(np.array([1, 2, 3])) == 1.4826


def test_nanmad():
    assert noise.mad(np.array([1, 2, 3, np.nan, np.nan, np.nan])) == 1.4826


def test_scalegen():

    cube = SpectralCube(data, wcs.WCS(h),
                        mask=BooleanArrayMask(mask, wcs=wcs.WCS(h)))
    noiseobj = noise.Noise(cube)
    assert np.isclose(noiseobj.scale, 0.534156264013)


def test_spatialnorm():
    cube = SpectralCube(data, wcs.WCS(h),
                        mask=BooleanArrayMask(mask, wcs=wcs.WCS(h)))
    noiseobj = noise.Noise(cube)
    noiseobj.estimate_noise()
    print noiseobj.spatial_norm
    expected = np.array([[0.09440465,  1.66883096,  0.15928848, 1.17088213,  0.12339732],
                         [0.70174314,  1.62910804,  2.85427202,  2.26766538,  0.59665047],
                         [1.3888236,  0.51415533,  0.59009925,  0.05219196,  0.23797816],
                         [1.29311331,  0.90643235,  0.42657667,  1.67327734,  2.03539431]])

    assert np.allclose(noiseobj.spatial_norm, expected)


def test_spectralnorm():
    cube = SpectralCube(data, wcs.WCS(h),
                        mask=BooleanArrayMask(mask, wcs=wcs.WCS(h)))
    noiseobj = noise.Noise(cube)
    noiseobj.estimate_noise()
    expected = np.array([ 1.14898322,  0.71345272,  1.21989125])
    assert np.allclose(noiseobj.spectral_norm, expected)
