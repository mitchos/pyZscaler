from pyzscaler.utils import zdx_params


def test_zdx_params():
    @zdx_params
    def dummy_function(self, **kwargs):
        return kwargs

    result = dummy_function(
        None, since=10, search="test_search", location_id="test_loc", department_id="test_dept", geo_id="test_geo"
    )

    assert result["to"] is not None
    assert result["from"] is not None
    assert result["q"] == "test_search"
    assert result["loc"] == "test_loc"
    assert result["dept"] == "test_dept"
    assert result["geo"] == "test_geo"
