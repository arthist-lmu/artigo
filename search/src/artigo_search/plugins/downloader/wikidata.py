import json
import logging

from collections import defaultdict
from artigo_search.plugins import (
    DownloaderPlugin,
    DownloaderPluginManager,
)

logger = logging.getLogger(__name__)


@DownloaderPluginManager.export('WikidataDownloader')
class WikidataDownloader(DownloaderPlugin):
    default_config = {
        'endpoint': 'https://www.wikidata.org/wiki/' + 
                    'Special:EntityData/{}.jsonld',
        'mapper': {
            'P1319': 'year_min',
            'P580': 'year_min',
            'P1326': 'year_max',
            'P582': 'year_max',
            'P571': 'date',
            'P276': 'location',
            'P195': 'institution',
            'P186': 'medium',
            'P180': 'depicts',
            'P170': 'creators',
            'P135': 'movement',
            'P136': 'genre',
            'P31': 'object_type',
        },
        'lang': [
            'de',
            'en',
        ],
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.endpoint = self.config['endpoint']
        self.mapper = self.config['mapper']
        self.lang = self.config['lang']

    def __call__(self, queries):
        urls = [self.endpoint.format(q) for q in queries]

        for _, entry in self.harvest(urls):
            yield entry

    def extract(self, url, response):
        idx, result = {}, defaultdict(list)

        for x in json.loads(response)['@graph']:
            if x.get('@type'):
                if x['@type'] == 'schema:Dataset':
                    result['id'] = x['@id'].rsplit(':', 1)[-1]
                elif x['@type'] == 'wikibase:TimeValue':
                    if x['timeValue'] == result.get('date'):
                        if result.get('year_min'):
                            for field in ('year_min', 'year_max'):
                                if result.get(field):
                                    date = result[field].rsplit('-', 2)
                                    result[field] = int(date[0])

                            if not result.get('year_max'):
                                result['year_max'] = result['year_min']
                        else:
                            year = int(result['date'].rsplit('-', 2)[0])

                            if x['timePrecision'] == 7:  # centuries
                                if year % 100 == 0:
                                    if year >= 0:
                                        result['year_min'] = year - 99
                                        result['year_max'] = year
                                    else:
                                        result['year_min'] = year
                                        result['year_max'] = year + 99
                                else:
                                    year = int(year / 100) * 100

                                    if year >= 0:
                                        result['year_min'] = year + 1
                                        result['year_max'] = year + 100
                                    else:
                                        result['year_min'] = year - 100
                                        result['year_max'] = year - 1
                            elif x['timePrecision'] == 8:  # decades
                                year = int(year / 10) * 10

                                if year >= 0:
                                    result['year_min'] = year
                                    result['year_max'] = year + 9
                                else:
                                    result['year_min'] = year - 9
                                    result['year_max'] = year
                            elif x['timePrecision'] > 8:
                                result['year_min'] = year
                                result['year_max'] = year

                        result.pop('date')

            if result.get('id'):
                if x['@id'] == f'wd:{result["id"]}':
                    for key, values in x.items():
                        ref_key = key.rsplit(':', 1)[-1]

                        if self.mapper.get(key):
                            field = self.mapper[key]

                            if not isinstance(values, list):
                                values = [values]

                            for value in values:
                                if field in ('date', 'year_min', 'year_max'):
                                    result[field] = value
                                elif isinstance(value, str):
                                    if value.startswith('wd:'):
                                        idx[value] = key
                        elif self.mapper.get(ref_key):
                            if isinstance(values, str):
                                if values.startswith('s:'):
                                    idx[values] = ref_key
                        elif key == 'label':
                            if not isinstance(values, list):
                                values = [values]

                            for value in values:
                                if not isinstance(value, dict):
                                    continue

                                if value.get('@language') in self.lang:
                                    result['titles'].append({
                                        'lang': value['@language'],
                                        'value': value['@value'],
                                    })

            if idx.get(x['@id']):
                field = self.mapper[idx[x['@id']]]

                if field in ('date', 'year_min', 'year_max'):
                    for key, value in x.items():
                        if self.mapper.get(key):
                            result[self.mapper[key]] = value
                elif x.get('label'):
                    if not isinstance(x['label'], dict):
                        continue

                    if x['label'].get('@language') in self.lang:
                        result[field].append({
                            'lang': x['label']['@language'],
                            'value': x['label']['@value'],
                        })

        return url, dict(result)
