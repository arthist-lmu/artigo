import logging

from artigo_search.plugins import DownloaderPluginManager

logger = logging.getLogger(__name__)


def get_result(query, plugin):
    manager = DownloaderPluginManager(
        configs=[{'type': plugin}],
    )

    return manager.run([query], [plugin])


def test_wikidata_Q22083984():
    result = get_result('Q22083984', 'WikidataDownloader')

    assert result[0]['id'] == 'Q22083984'
    assert result[0]['year_min'] == 1600
    assert result[0]['year_max'] == 1625


def test_wikidata_Q29975604():
    result = get_result('Q29975604', 'WikidataDownloader')

    assert result[0]['id'] == 'Q29975604'
    assert result[0]['year_min'] == 1
    assert result[0]['year_max'] == 100


def test_wikidata_Q107664088():
    result = get_result('Q107664088', 'WikidataDownloader')

    assert result[0]['id'] == 'Q107664088'
    assert result[0]['year_min'] == 1801
    assert result[0]['year_max'] == 1900


def test_wikidata_Q107011200():
    result = get_result('Q107011200', 'WikidataDownloader')

    assert result[0]['id'] == 'Q107011200'
    assert result[0]['year_min'] == 1801
    assert result[0]['year_max'] == 1900
