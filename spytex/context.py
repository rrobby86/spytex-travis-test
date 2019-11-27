from typing import Any, Mapping


class ResolutionContext:
    """Holds contextual information accessible during definition resolution."""

    def __init__(self, vals: Mapping[str, Any] = {}):
        self.vals = dict(vals)

    def copy(self):
        res = ResolutionContext(
            vals=self.vals.copy()
        )
        return res

    def update_vals(self, new_vals: Mapping[str, Any]) -> "ResolutionContext":
        res = self.copy()
        res.vals.update(new_vals)
        return res
