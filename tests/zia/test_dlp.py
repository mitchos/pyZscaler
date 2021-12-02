import pytest
import responses
from box import Box, BoxList
from responses import matchers


@pytest.fixture(name="dlp_dicts")
def dlp_dicts():
    yield [
        {
            "id": 1,
            "custom": True,
            "customPhraseMatchType": "MATCH_ALL_CUSTOM_PHRASE_PATTERN_DICTIONARY",
            "dictionaryType": "PATTERNS_AND_PHRASES",
            "name": "test",
            "nameL10nTag": False,
            "description": "test",
            "phrases": [
                {"action": "PHRASE_COUNT_TYPE_ALL", "phrase": "test"},
                {"action": "PHRASE_COUNT_TYPE_UNIQUE", "phrase": "test"},
            ],
            "patterns": [
                {"action": "PATTERN_COUNT_TYPE_ALL", "pattern": "test"},
                {"action": "PATTERN_COUNT_TYPE_UNIQUE", "pattern": "test"},
            ],
        },
        {
            "id": 2,
            "custom": True,
            "customPhraseMatchType": "MATCH_ANY_CUSTOM_PHRASE_PATTERN_DICTIONARY",
            "dictionaryType": "PATTERNS_AND_PHRASES",
            "name": "test",
            "nameL10nTag": False,
            "description": "test",
            "phrases": [
                {"action": "PHRASE_COUNT_TYPE_ALL", "phrase": "test"},
                {"action": "PHRASE_COUNT_TYPE_UNIQUE", "phrase": "test"},
            ],
            "patterns": [
                {"action": "PATTERN_COUNT_TYPE_ALL", "pattern": "test"},
                {"action": "PATTERN_COUNT_TYPE_UNIQUE", "pattern": "test"},
            ],
        },
    ]


@responses.activate
def test_dlp_update_dict_all(zia, dlp_dicts):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/dlpDictionaries/1",
        json=dlp_dicts[0],
        status=200,
    )

    responses.add(
        method="PUT",
        url="https://zsapi.zscaler.net/api/v1/dlpDictionaries/1",
        json={
            "id": 1,
            "custom": True,
            "customPhraseMatchType": "MATCH_ALL_CUSTOM_PHRASE_PATTERN_DICTIONARY",
            "dictionaryType": "PATTERNS_AND_PHRASES",
            "name": "test_updated",
            "nameL10nTag": False,
            "description": "test",
            "phrases": [{"action": "PHRASE_COUNT_TYPE_ALL", "phrase": "test_updated"}],
            "patterns": [{"action": "PATTERN_COUNT_TYPE_ALL", "pattern": "test_updated"}],
        },
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "id": 1,
                    "custom": True,
                    "customPhraseMatchType": "MATCH_ALL_CUSTOM_PHRASE_PATTERN_DICTIONARY",
                    "dictionaryType": "PATTERNS_AND_PHRASES",
                    "name": "test_updated",
                    "nameL10nTag": False,
                    "description": "test",
                    "phrases": [{"action": "PHRASE_COUNT_TYPE_ALL", "phrase": "test_updated"}],
                    "patterns": [{"action": "PATTERN_COUNT_TYPE_ALL", "pattern": "test_updated"}],
                }
            )
        ],
    )

    resp = zia.dlp.update_dict(
        "1",
        name="test_updated",
        match_type="all",
        phrases=[
            ("all", "test_updated"),
        ],
        patterns=[
            ("all", "test_updated"),
        ],
    )

    assert resp.name == "test_updated"
    assert resp.phrases[0].phrase == "test_updated"
    assert resp.patterns[0].pattern == "test_updated"


@responses.activate
def test_dlp_update_dict_any(zia, dlp_dicts):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/dlpDictionaries/1",
        json=dlp_dicts[0],
        status=200,
    )

    responses.add(
        method="PUT",
        url="https://zsapi.zscaler.net/api/v1/dlpDictionaries/1",
        json={
            "id": 1,
            "custom": True,
            "customPhraseMatchType": "MATCH_ANY_CUSTOM_PHRASE_PATTERN_DICTIONARY",
            "dictionaryType": "PATTERNS_AND_PHRASES",
            "name": "test_updated",
            "nameL10nTag": False,
            "description": "test",
            "phrases": [{"action": "PHRASE_COUNT_TYPE_ALL", "phrase": "test_updated"}],
            "patterns": [{"action": "PATTERN_COUNT_TYPE_ALL", "pattern": "test_updated"}],
        },
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "id": 1,
                    "custom": True,
                    "customPhraseMatchType": "MATCH_ANY_CUSTOM_PHRASE_PATTERN_DICTIONARY",
                    "dictionaryType": "PATTERNS_AND_PHRASES",
                    "name": "test_updated",
                    "nameL10nTag": False,
                    "description": "test",
                    "phrases": [{"action": "PHRASE_COUNT_TYPE_ALL", "phrase": "test_updated"}],
                    "patterns": [{"action": "PATTERN_COUNT_TYPE_ALL", "pattern": "test_updated"}],
                }
            )
        ],
    )

    resp = zia.dlp.update_dict(
        "1",
        name="test_updated",
        match_type="any",
        phrases=[
            ("all", "test_updated"),
        ],
        patterns=[
            ("all", "test_updated"),
        ],
    )

    assert resp.name == "test_updated"
    assert resp.phrases[0].phrase == "test_updated"
    assert resp.patterns[0].pattern == "test_updated"


@responses.activate
def test_dlp_update_dict_error(zia, dlp_dicts):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/dlpDictionaries/1",
        json=dlp_dicts[0],
        status=200,
    )
    with pytest.raises(Exception) as e_info:
        resp = zia.dlp.update_dict("1", match_type="test")


@responses.activate
def test_dlp_list_dicts(zia, dlp_dicts):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/dlpDictionaries",
        json=dlp_dicts,
        status=200,
    )

    resp = zia.dlp.list_dicts()
    assert isinstance(resp, BoxList)
    assert resp[0].id == 1


@responses.activate
def test_dlp_delete(zia):
    responses.add(
        method="DELETE",
        url="https://zsapi.zscaler.net/api/v1/dlpDictionaries/1",
        body="",
        status=204,
    )

    resp = zia.dlp.delete_dict("1")
    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
def test_dlp_get(zia, dlp_dicts):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/dlpDictionaries/1",
        json=dlp_dicts[0],
        status=200,
    )

    resp = zia.dlp.get_dict("1")
    assert isinstance(resp, Box)
    assert resp.id == 1


@responses.activate
def test_dlp_add_type_all(zia, dlp_dicts):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/dlpDictionaries",
        json=dlp_dicts[0],
        match=[
            matchers.json_params_matcher(
                {
                    "name": "test",
                    "dictionaryType": "PATTERNS_AND_PHRASES",
                    "description": "test",
                    "customPhraseMatchType": "MATCH_ALL_CUSTOM_PHRASE_PATTERN_DICTIONARY",
                    "patterns": [
                        {
                            "action": "PATTERN_COUNT_TYPE_ALL",
                            "pattern": "test",
                        }
                    ],
                    "phrases": [
                        {
                            "action": "PHRASE_COUNT_TYPE_ALL",
                            "phrase": "test",
                        }
                    ],
                }
            )
        ],
        status=200,
    )
    resp = zia.dlp.add_dict(
        name="test",
        description="test",
        match_type="all",
        patterns=[("all", "test")],
        phrases=[("all", "test")],
    )

    assert isinstance(resp, Box)
    assert resp.id == 1


@responses.activate
def test_dlp_add_type_any(zia, dlp_dicts):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/dlpDictionaries",
        json=dlp_dicts[0],
        match=[
            matchers.json_params_matcher(
                {
                    "name": "test",
                    "dictionaryType": "PATTERNS_AND_PHRASES",
                    "description": "test",
                    "customPhraseMatchType": "MATCH_ANY_CUSTOM_PHRASE_PATTERN_DICTIONARY",
                    "patterns": [
                        {
                            "action": "PATTERN_COUNT_TYPE_ALL",
                            "pattern": "test",
                        }
                    ],
                    "phrases": [
                        {
                            "action": "PHRASE_COUNT_TYPE_ALL",
                            "phrase": "test",
                        }
                    ],
                }
            )
        ],
        status=200,
    )
    resp = zia.dlp.add_dict(
        name="test",
        description="test",
        match_type="any",
        patterns=[("all", "test")],
        phrases=[("all", "test")],
    )

    assert isinstance(resp, Box)
    assert resp.id == 1


def test_dlp_add_error(zia):
    with pytest.raises(Exception) as e_info:
        resp = zia.dlp.add_dict(name="test", description="test", match_type="test")


@responses.activate
def test_dlp_validate_dict(zia):
    api_response = {
        "err_msg": "Valid regular expression",
        "err_parameter": None,
        "err_position": 0,
        "err_suggestion": None,
        "id_list": None,
        "status": 0,
    }
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/dlpDictionaries/validateDlpPattern",
        json=api_response,
        match=[
            matchers.json_params_matcher(
                {
                    "data": "test",
                }
            )
        ],
        status=200,
    )

    resp = zia.dlp.validate_dict("test")
    assert isinstance(resp, Box)
    assert resp.status == 0
