# License: MIT
# Copyright © 2023 Frequenz Energy-as-a-Service GmbH

"""
Tests for the GridConnection module.
"""

from frequenz.sdk import microgrid
from frequenz.sdk.microgrid.component import Component, ComponentCategory, GridMetadata
from frequenz.sdk.microgrid.fuse import Fuse
from frequenz.sdk.microgrid.grid_connection import GridConnection
from frequenz.sdk.timeseries import Current


async def test_grid_connection() -> None:
    """Test the grid connection module."""

    # The tests here need to be in this exact sequence, because the grid connection
    # is a singleton. Once it gets created, it stays in memory for the duration of
    # the tests, unless we explicitly delete it.

    # validate islands with no grid connection
    components = [
        Component(2, ComponentCategory.METER),
    ]

    microgrid.grid_connection.initialize(components)

    grid_connection = microgrid.grid_connection.get()
    assert grid_connection is None

    # validate error when there are multiple grid connections
    components = [
        Component(1, ComponentCategory.GRID, None, GridMetadata(123.0)),
        Component(2, ComponentCategory.GRID, None, GridMetadata(345.0)),
        Component(3, ComponentCategory.METER),
    ]

    try:
        microgrid.grid_connection.initialize(components)
    except RuntimeError:
        pass

    grid_connection = microgrid.grid_connection.get()
    assert grid_connection is None

    # validate when there is one grid connection
    components = [
        Component(1, ComponentCategory.GRID, None, GridMetadata(123.0)),
        Component(2, ComponentCategory.METER),
    ]

    microgrid.grid_connection.initialize(components)

    grid_connection = microgrid.grid_connection.get()

    # Each phase should have the same fuse current
    expected_fuse_current = Current.from_amperes(123.0)
    expected_fuse = Fuse(
        expected_fuse_current, expected_fuse_current, expected_fuse_current
    )

    assert grid_connection == GridConnection(fuse=expected_fuse)
