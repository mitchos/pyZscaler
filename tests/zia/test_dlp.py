import pytest
import responses
from box import BoxList


@pytest.fixture
def dlp_dicts():
    return [
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
            "name": "test2",
            "phrases": [],
            "customPhraseMatchType": "MATCH_ALL_CUSTOM_PHRASE_PATTERN_DICTIONARY",
            "patterns": [{"action": "PATTERN_COUNT_TYPE_ALL", "pattern": "tester"}],
            "nameL10nTag": False,
            "dictionaryType": "PATTERNS_AND_PHRASES",
            "exactDataMatchDetails": [],
            "idmProfileMatchAccuracyDetails": [],
            "custom": True,
        },
    ]


@responses.activate
def test_dlp_add_dicts(zia, dlp_dicts):
    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/dlpDictionaries",
        status=200,
        json=dlp_dicts[0],
        match=[
            responses.json_params_matcher(
                {
                    "name": "test",
                    "description": "test",
                    "dictionaryType": "PATTERNS_AND_PHRASES",
                    "customPhraseMatchType": "MATCH_ANY_CUSTOM_PHRASE_PATTERN_DICTIONARY",
                    "phrases": [
                        {"action": "PHRASE_COUNT_TYPE_ALL", "phrase": "test"},
                        {"action": "PHRASE_COUNT_TYPE_UNIQUE", "phrase": "test"},
                    ],
                    "patterns": [
                        {"action": "PATTERN_COUNT_TYPE_ALL", "pattern": "test"},
                        {"action": "PATTERN_COUNT_TYPE_UNIQUE", "pattern": "test"},
                    ],
                }
            )
        ],
    )

    resp = zia.dlp.add_dict(
        name="test",
        description="test",
        match_type="any",
        phrases=[("all", "test"), ("unique", "test")],
        patterns=[("all", "test"), ("unique", "test")],
    )

    assert isinstance(resp, dict)
    assert resp.id == 1


@responses.activate
def test_dlp_update_dict(zia, dlp_dicts):
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
            "patterns": [
                {"action": "PATTERN_COUNT_TYPE_ALL", "pattern": "test_updated"}
            ],
        },
        status=200,
        match=[
            responses.json_params_matcher(
                {
                    "id": 1,
                    "custom": True,
                    "customPhraseMatchType": "MATCH_ALL_CUSTOM_PHRASE_PATTERN_DICTIONARY",
                    "dictionaryType": "PATTERNS_AND_PHRASES",
                    "name": "test_updated",
                    "nameL10nTag": False,
                    "description": "test",
                    "phrases": [
                        {"action": "PHRASE_COUNT_TYPE_ALL", "phrase": "test_updated"}
                    ],
                    "patterns": [
                        {"action": "PATTERN_COUNT_TYPE_ALL", "pattern": "test_updated"}
                    ],
                }
            )
        ],
    )

    resp = zia.dlp.update_dict(
        "1",
        name="test_updated",
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
