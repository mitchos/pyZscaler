import pytest

from pyzscaler.zia import ZIA


@pytest.fixture
def zia():
    return ZIA()


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
