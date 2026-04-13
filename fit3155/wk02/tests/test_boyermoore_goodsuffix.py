from fit3155.wk02.src.boyermoore_goodsuffix import process_gs, process_z_suffix


def test_z_suffix_array_from_notes():
    z_suffix = process_z_suffix("acababacaba")
    assert z_suffix == [1, 0, 1, 0, 5, 0, 3, 0, 1, 0, None, None]


def test_gs_array_from_notes():
    pat = "acababacaba"
    z_suffix = process_z_suffix(pat)
    gs_array = process_gs(pat, z_suffix)
    assert gs_array == [0, 0, 0, 0, 0, 0, 4, 0, 6, 0, 8, 10]
