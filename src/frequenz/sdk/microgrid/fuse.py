# License: MIT
# Copyright © 2023 Frequenz Energy-as-a-Service GmbH

"""Fuse data class."""

from dataclasses import dataclass

from ..timeseries import Current


@dataclass(frozen=True)
class Fuse:
    """Fuse data class.

    Attributes:
        rated_current_phase_1: The rated current of phase 1, in Amperes.
        rated_current_phase_2: The rated current of phase 2, in Amperes.
        rated_current_phase_3: The rated current of phase 3, in Amperes.
    """

    rated_current_phase_1: Current
    rated_current_phase_2: Current
    rated_current_phase_3: Current

    def __hash__(self) -> int:
        current_phase_1 = self.rated_current_phase_1.as_amperes()
        current_phase_2 = self.rated_current_phase_2.as_amperes()
        current_phase_3 = self.rated_current_phase_3.as_amperes()
        return hash((current_phase_1, current_phase_2, current_phase_3))
