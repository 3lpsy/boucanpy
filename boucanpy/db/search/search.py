from elasticsearch import Elasticsearch


class Search:
    def __init__(self, elasticsearch=None):
        self.elasticsearch = elasticsearch

    def register(self, el_url):
        self.elasticsearch = Elasticsearch([url])

    def add_to_index(self, index, model):
        if not self.elasticsearch:
            return
        payload = {}
        for field in model.__searchable__:
            payload[field] = getattr(model, field)
        self.elasticsearch.index(index=index, doc_type=index, id=model.id, body=payload)

    def remove_from_index(self, index, model):
        if not self.elasticsearch:
            return
        self.elasticsearch.delete(index=index, doc_type=index, id=model.id)

    def query_index(self, index, query, page, per_page):
        if not self.elasticsearch:
            return [], 0
        search = self.elasticsearch.search(
            index=index,
            doc_type=index,
            body={
                "query": {"multi_match": {"query": query, "fields": ["*"]}},
                "from": (page - 1) * per_page,
                "size": per_page,
            },
        )
        ids = [int(hit["_id"]) for hit in search["hits"]["hits"]]
        return ids, search["hits"]["total"]


search = Search()
