# Parameter File Formats

**As of May 2025, YAML is the default parameter file format for OpenPTV.**

- All parameter files are now written and read as `.yaml` files by default.
- Legacy `.par` files are still supported for backward compatibility: if a `.yaml` file is not found, the corresponding `.par` file will be read and automatically converted to YAML.
- A migration script (`examples/convert_par_to_yaml.py`) is provided to convert all `.par` files in a directory to YAML.

## File Locations

All parameter files are stored in the `parameters/` folder of each experiment:

- `ptv.yaml` - Control parameters
- `track.yaml` - Tracking parameters
- `sequence.yaml` - Sequence parameters
- `criteria.yaml` - Criteria parameters
- `targ_rec.yaml` - Target recognition parameters
- `examine.yaml` - Examine parameters
- `orient.yaml` - Orientation parameters
- `calibration.yaml` - Calibration parameters

Legacy `.par` files (e.g., `ptv.par`, `track.par`, etc.) are still recognized for backward compatibility.

## File Formats

Parameter files are now in YAML format. Example for `track.yaml`:

```yaml
dvxmin: 0.1
dvxmax: 1.0
dvymin: 0.1
dvymax: 1.0
dvzmin: 0.1
dvzmax: 1.0
angle: 0.5
dacc: 0.2
add: 1
```

For details on each parameter, see the class docstrings in `openptv/gui/parameters.py`.