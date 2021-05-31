import pdm_packer


def test_import_package():
    assert isinstance(pdm_packer.__all__, list)
