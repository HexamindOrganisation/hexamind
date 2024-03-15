import os

from elasticsearch import Elasticsearch

from .AbstractDb import IDbClient

# TODO : MUST BE INTENSIVELY TESTED BECAUSE NOT SURE OF THE IMPLEMENTATION


class ElasticSearchAdapter(IDbClient):
    def __init__(
        self,
        host=None,
        port=None,
        cloud_id=None,
        api_key=None,
        ca_certs=None,
        ssl_assert=None,
        password=None,
    ):

        self.env_params = {
            "host": host or os.getenv("API_DB_HOST"),
            "port": port or os.getenv("API_DB_PORT"),
            "cloud_id": cloud_id or os.getenv("ES_CLOUD_ID"),
            "api_key": api_key or os.getenv("ES_API_KEY"),
            "ca_certs": ca_certs or os.getenv("ES_CA_CERTS"),
            "ssl_assert": ssl_assert or os.getenv("ES_SSL_ASSERT"),
            "password": password or os.getenv("API_DB_PASSWORD"),
        }

        if (
            self.env_params["cloud_id"] is not None
            and self.env_params["api_key"] is not None
        ):
            self.client = Elasticsearch(
                cloud_id=self.env_params["cloud_id"], api_key=self.env_params["api_key"]
            )
        else:
            connection_opts = {
                "hosts": [f"{self.env_params['host']}:{self.env_params['port']}"]
            }

            if (
                self.env_params["ca_certs"] is not None
                and self.env_params["ssl_assert"] is not None
            ):
                raise ValueError(
                    "You can't use both ca_certs and ssl_assert at the same time"
                )
            elif (
                self.env_params["ssl_assert"] is not None
                and self.env_params["ca_certs"] is None
            ):
                connection_opts["ssl_assert_fingerprint"] = self.env_params[
                    "ssl_assert"
                ]
            elif (
                self.env_params["ca_certs"] is not None
                and self.env_params["ssl_assert"] is None
            ):
                connection_opts["ca_certs"] = self.env_params["ca_certs"]
            else:
                connection_opts["use_ssl"] = False

            if self.env_params["password"]:
                connection_opts["basic_auth"] = ("elastic", self.env_params["password"])

            self.client = Elasticsearch(**connection_opts)

        if not self.client.ping():
            raise ValueError("Connection to ElasticSearch failed")

    def add_document(self, document, embedding, block):
        self.client.index(
            index="rag",
            document={
                "document": document,
                "embedding": embedding,
                "id": block.index,
                "block": block.to_dict(),
            },
        )

    def get_document(self, document_id):
        return self.client.get(index="rag", id=document_id)

    def delete_document(self, document_id):
        self.client.delete(index="rag", id=document_id)

    def update_document(self, document, embedding, block):
        self.client.index(
            index="rag",
            document={
                "document": document,
                "embedding": embedding,
                "id": block.index,
                "block": block.to_dict(),
            },
        )
