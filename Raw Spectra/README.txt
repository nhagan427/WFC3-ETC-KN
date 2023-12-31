SEDs published in Bulla 2019, "POSSIS: predicting spectra, light curves and polarization for multi-dimensional models of supernovae and kilonovae"
https://ui.adsabs.harvard.edu/abs/2019arXiv190604205B/abstract

1) FILENAME

nphX_mejY_phiZ_TW.txt
X: number of Monte Carlo photons
Y: total ejecta mass
Z: half-opening angle of the lanthanide-rich component
W: Temperature at 1 day (T0)

2) FILE FORMAT

###################################################
Nobs (number of viewing angles)
Nwave (number of wavelength bins)
Ntime (number of time bins), t_i (days), t_f (days)
#################### iobs = 0 #####################
                 itime=0   itime=1 ..........
iwave=0  wave	  flux      flux   ..........  
iwave=1  wave	  flux      flux   ..........  
.         .         .         .    ..........
.         .         .         .    ..........
.         .         .         .    ..........
.         .         .         .    ..........
#################### iobs = 1 #####################
.
.
.

	 
3) NOTES:
- Viewing angles are from equator (edge-on) to pole (face-on)
  equally-spaced in cosine (e.g. 5 viewing angles corresponds 
  to cosine(theta) = 0, 0.25, 0.5, 0.75, 1).
- Time bins have step size Dt = (t_f - t_i) / Ntime
- Reference times are [t_i + 0.5 * Dt, t_i + 1.5 * Dt, ...]
- Fluxes are given in erg s-1 cm-2 A-1 at the distance of 10 pc
- Opang=0 is a one-component model with lanthanide-poor opacities, 
  opang=90 a one-component model with lanthanide-rich opacities
