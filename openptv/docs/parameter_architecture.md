# OpenPTV Parameter Architecture

## Parameter Types

1. **Core Parameters**
   - Located in `openptv.binding.parameters` (Cython) or `openptv.pyoptv.parameters` (Python)
   - Used for actual processing
   - Exposed through the main package (`openptv`)
   - Examples: `MultimediaParams`, `TrackingParams`, etc.

2. **GUI Parameters**
   - Located in `openptv.gui.parameters`
   - Used only for GUI interaction
   - Not exposed through the main package
   - Examples: `PtvParams`, `TrackingParams`, etc.

## Parameter Flow

1. GUI reads/writes parameter files using GUI parameter classes
2. When processing is needed, GUI parameters are converted to core parameters
3. Processing is done using core parameters
4. Results are converted back to GUI parameters for display

## Best Practices

1. Always use explicit imports to avoid confusion
2. Never import GUI parameters in non-GUI modules
3. Use conversion functions to convert between parameter types
4. Maintain consistent APIs between parameter types