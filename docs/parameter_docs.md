# Parameter File Formats

This document describes the parameter file formats used by OpenPTV.

## File Locations

All parameter files are stored in the `parameters/` folder of each experiment:

- `ptv.par` - Control parameters
- `track.par` - Tracking parameters
- `sequence.par` - Sequence parameters
- `criteria.par` - Criteria parameters
- `targ_rec.par` - Target recognition parameters
- `examine.par` - Examine parameters
- `orient.par` - Orientation parameters
- `calibration.par` - Calibration parameters

## File Formats

### track.par

```
dvxmin
dvxmax
dvymin
dvymax
dvzmin
dvzmax
angle
dacc
add
```

### sequence.par

```
first
last
```

...