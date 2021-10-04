import pytest

from model import Volume, Vector3

def test_pos_inside():
    vol = Volume(
        Vector3(5, 10, 20),
        Vector3(3,  4,  5)
    )
    for x in [5, 7, 8]:
        for y in [10, 12, 14]:
            for z in [20, 22, 25]:
                assert vol.pos_inside(Vector3(x, y, z))

def test_not_pos_inside():
    vol = Volume(
        Vector3(5, 10, 20),
        Vector3(3,  4,  5)
    )
    for x in [0, 50]:
        for y in [0, 50]:
            for z in [0, 50]:
                assert not vol.pos_inside(Vector3(x, y, z))
    for x in [4, 9]:
        for y in [9, 15]:
            for z in [19, 26]:
                assert not vol.pos_inside(Vector3(x, y, z))

def test_dim_inside():
    vol = Volume(
        Vector3(5, 10, 20),
        Vector3(3,  4,  5)
    )
    assert vol.dim_inside(Vector3(1, 1, 1))
    assert vol.dim_inside(Vector3(3, 0, 0))
    assert vol.dim_inside(Vector3(0, 4, 0))
    assert vol.dim_inside(Vector3(0, 0, 5))
    assert vol.dim_inside(Vector3(3, 4, 5))

def test_not_dim_inside():
    vol = Volume(
        Vector3(5, 10, 20),
        Vector3(3,  4,  5)
    )
    assert not vol.dim_inside(Vector3(4, 0, 0))
    assert not vol.dim_inside(Vector3(0, 5, 0))
    assert not vol.dim_inside(Vector3(0, 0, 6))
    assert not vol.dim_inside(Vector3(4, 5, 6))

def test_vol_inside():
    pos = Vector3(5, 10, 20)
    dim = Vector3(3, 4, 5)
    vol = Volume(pos, dim)
    assert vol.vol_inside(vol)
    
    unit = Vector3(1, 1, 1)
    for x in [pos.x, pos.x + dim.x - 1]:
        for y in [pos.y, pos.y + dim.y - 1]:
            for z in [pos.z, pos.z + dim.z - 1]:
                p = Vector3(x, y, z)
                assert vol.vol_inside(Volume(p, unit))

def test_not_vol_inside():
    pos = Vector3(5, 10, 20)
    dim = Vector3(3, 4, 5)
    vol = Volume(pos, dim)
    unit = Vector3(1, 1, 1)
    assert not vol.vol_inside(Volume(pos + unit, dim))
    assert not vol.vol_inside(Volume(pos, dim + unit))
    assert not vol.vol_inside(Volume(pos + unit, dim + unit))
    
    for x in [pos.x - 1, pos.x + dim.x]:
        for y in [pos.y - 1, pos.y + dim.y]:
            for z in [pos.z - 1, pos.z + dim.z]:
                p = Vector3(x, y, z)
                assert not vol.vol_inside(Volume(p, unit))    

def test_intersect():
    pos = Vector3(5, 10, 20)
    dim = Vector3(3, 4, 5)
    vol = Volume(pos, dim)
    unit = Vector3(1, 1, 1)

    assert vol.vol_intersect(vol)
    assert vol.vol_intersect(Volume(pos - unit, dim))
    assert vol.vol_intersect(Volume(pos - unit - unit, dim))
    assert vol.vol_intersect(Volume(pos + unit - dim, dim))
    assert vol.vol_intersect(Volume(pos + dim - unit, dim))
    assert vol.vol_intersect(Volume(Vector3(5, 10, 22), unit))
    for x in [pos.x, pos.x + dim.x - 1]:
        for y in [pos.y, pos.y + dim.y - 1]:
            for z in [pos.z, pos.z + dim.z - 1]:
                p = Vector3(x, y, z)
                assert vol.vol_intersect(Volume(p, unit))

def test_not_intersect():
    pos = Vector3(5, 10, 20)
    dim = Vector3(3, 4, 5)
    vol = Volume(pos, dim)
    unit = Vector3(1, 1, 1)

    assert not vol.vol_intersect(Volume(pos - dim, dim))
    assert not vol.vol_intersect(Volume(pos - unit - unit - unit, dim))
    assert not vol.vol_intersect(Volume(pos + dim, dim))
    for x in [pos.x - 1, pos.x + dim.x]:
        for y in [pos.y - 1, pos.y + dim.y]:
            for z in [pos.z - 1, pos.z + dim.z]:
                p = Vector3(x, y, z)
                assert not vol.vol_intersect(Volume(p, unit))
