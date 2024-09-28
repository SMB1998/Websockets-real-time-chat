from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Components 

@registry.register_document
class ComponentDocument(Document):
    proveedor = fields.TextField(attr='proveedor_identification')

    class Index:
        name = "components"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Components
        fields = ["url", "nombre", "search_index_provider", "referencia", "precio", "image_url", "datasheet_url"]
