# tests/test_text_processor.py
from src.components.text_processor import TextProcessor

def test_preprocess_text_for_lda():
    # Inicializa sem os modelos, pois só vamos testar uma função
    processor = TextProcessor(sentiment_model="", sentiment_model_fallback="")
    text = "Este é um ÓTIMO TEXTO, com pontuação!"
    expected = "ótimo texto pontuação"
    assert processor.preprocess_text_for_lda(text) == expected