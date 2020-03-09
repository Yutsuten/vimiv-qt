# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

# This file is part of vimiv.
# Copyright 2017-2020 Christian Karl (karlch) <karlch at protonmail dot com>
# License: GNU GPL v3, see the "LICENSE" and "AUTHORS" files for details.

"""Tests for vimiv.imutils.imtransform."""

from functools import partial

from PyQt5.QtGui import QPixmap

import pytest

from vimiv.imutils import imtransform, pixmaps


ACTIONS = (
    imtransform.Transform.rotate_command,
    imtransform.Transform.flip,
    partial(imtransform.Transform.resize, width=400, height=400),
    partial(imtransform.Transform.rescale, dx=2, dy=2),
)


@pytest.fixture(scope="function")
def transform(qtbot, mocker):
    """Fixture to retrieve a clean Transform instance."""
    pixmap = QPixmap(300, 300)
    current_pixmap = pixmaps.CurrentPixmap()
    transform = imtransform.Transform(current_pixmap)
    current_pixmap.pixmap = transform.original = pixmap
    return transform


@pytest.fixture(params=ACTIONS)
def action(transform, request):
    action = request.param
    return partial(action, self=transform)


def test_change_and_reset(action, transform):
    """Ensure every action leads to a change and is appropriately reset."""
    action()
    assert transform.changed
    transform.reset()
    assert not transform.changed


@pytest.mark.parametrize("angle", range(0, 360, 15))
def test_rotate_angle(transform, angle):
    transform.rotate(angle)
    assert transform.angle == pytest.approx(angle)
