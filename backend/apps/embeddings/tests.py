from django.test import SimpleTestCase
from .embedding_service import embed_text


class EmbeddingTests(SimpleTestCase):
    def test_embed_text(self):
        self.assertTrue(embed_text('abc'))
