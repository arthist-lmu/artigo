from opensearch_dsl import (
    Document,
    Nested,
    Text,
    Keyword,
    Long,
    Float,
    Boolean,
    RankFeature,
)


class Resource(Document):
    hash_id = Text(fields={'keyword': Keyword()})
    path = Text(fields={'keyword': Keyword()})

    metadata = Nested(
        properties={
            'name': Text(
                fields={'keyword': Keyword()},
            ),
            'value_str': Text(
                fields={'keyword': Keyword()},
                copy_to=['all_text', 'all_metadata'],
            ),
            'value_int': Long(),
            'value_float': Float(),
        },
    )

    tags = Nested(
        properties={
            'id': Text(
                fields={'keyword': Keyword()},
            ),
            'name': Text(
                fields={'keyword': Keyword()},
                copy_to=['all_text'],
            ),
            'count': Long(),
            # TODO: currently not supported
            # 'count': RankFeature(),
        },
    )

    collection = Nested(
        properties={
            'id': Text(
                fields={'keyword': Keyword()},
            ),
            'name': Text(
                fields={'keyword': Keyword()},
            ),
            'url': Text(
                fields={'keyword': Keyword()},
            ),
            'is_public': Boolean(),
        },
    )

    all_text = Text()
    all_metadata = Text()

    def add_metadata(self, data):
        self.metadata.append(data)

    def add_tag(self, data):
        self.tags.append(data)

    def add_collection(self, data):
        self.collection = data
