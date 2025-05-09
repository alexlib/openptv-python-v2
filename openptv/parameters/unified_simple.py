import yaml
from openptv.parameters.control import PtvParams
from openptv.parameters.sequence import SequenceParams
# ... import other parameter classes as needed

class UnifiedParameters:
    def __init__(self, path):
        self.path = path
        self.data = {}

    def read(self):
        with open(self.path, 'r') as f:
            self.data = yaml.safe_load(f)

    def write(self):
        with open(self.path, 'w') as f:
            yaml.safe_dump(self.data, f, sort_keys=False)

    def to_classes(self):
        """Convert loaded YAML to parameter class instances."""
        ptv = PtvParams(**self.data['ptv'])
        sequence = SequenceParams(**self.data['sequence'])
        # ...repeat for other parameter sets...
        return ptv, sequence  # etc.

    def from_classes(self, ptv, sequence, ...):
        """Update YAML data from parameter class instances."""
        self.data['ptv'] = ptv.__dict__
        self.data['sequence'] = sequence.__dict__
        # ...repeat for other parameter sets...

# Usage:
# up = UnifiedParameters('parameters.yml')
# up.read()
# ptv, sequence = up.to_classes()
# # ... modify ptv, sequence ...
# up.from_classes(ptv, sequence)
# up.write()