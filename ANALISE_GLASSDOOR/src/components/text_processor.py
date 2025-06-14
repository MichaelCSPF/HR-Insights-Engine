# src/components/text_processor.py

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from transformers import pipeline
from collections import Counter

class TextProcessor:
    """Realiza todo o pré-processamento e análise de NLP."""

    def __init__(self, sentiment_model: str, sentiment_model_fallback: str):
        print("Inicializando TextProcessor...")
        self._load_nltk_resources()
        self.stop_words = stopwords.words('portuguese')
        self.sentiment_analyzer = self._load_sentiment_model(sentiment_model, sentiment_model_fallback)
        print("TextProcessor pronto.")

    def _load_nltk_resources(self):
        """Baixa recursos do NLTK, se necessário."""
        try:
            stopwords.words('portuguese')
        except LookupError:
            nltk.download('stopwords')

    def _load_sentiment_model(self, model, fallback):
        """Carrega o modelo de análise de sentimento da Hugging Face."""
        try:
            print(f"Carregando modelo de sentimento: {model}")
            return pipeline("sentiment-analysis", model=model)
        except Exception as e:
            print(f"Falha ao carregar modelo principal: {e}. Tentando fallback...")
            try:
                print(f"Carregando modelo de fallback: {fallback}")
                return pipeline("sentiment-analysis", model=fallback)
            except Exception as e2:
                print(f"Falha ao carregar modelo de fallback: {e2}. Análise de sentimento desativada.")
                return None

    def preprocess_text_for_lda(self, text: str) -> str:
        """Limpa o texto para modelagem de tópicos: minúsculas, remove pontuação e stopwords."""
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        words = text.split()
        words_no_stop = [word for word in words if word not in self.stop_words and len(word) > 2]
        return " ".join(words_no_stop)

    def analyze_sentiment(self, text: str) -> str:
        """Aplica o modelo de sentimento a uma string de texto."""
        if not self.sentiment_analyzer or not isinstance(text, str) or not text.strip():
            return "indefinido"
        try:
            # Truncamento é gerenciado pelo pipeline por padrão
            result = self.sentiment_analyzer(text)
            return result[0]['label']
        except Exception:
            return "erro_analise"

    def run_full_analysis(self, df: pd.DataFrame, text_cols: list) -> pd.DataFrame:
        """Executa todo o fluxo de análise de NLP no DataFrame."""
        print("Iniciando análise completa de NLP no DataFrame...")
        analyzed_df = df.copy()

        # Pré-processamento e Análise de Sentimento
        for col in text_cols:
            if col in analyzed_df.columns:
                print(f"Analisando sentimentos da coluna: {col}")
                # Garante que a coluna seja string para evitar erros
                analyzed_df[col] = analyzed_df[col].astype(str).fillna('')
                analyzed_df[f'{col}_sentiment'] = analyzed_df[col].apply(self.analyze_sentiment)

        # Topic Modeling e Keywords (exemplo na coluna 'CONS')
        if 'CONS' in analyzed_df.columns:
            print("Processando texto da coluna 'CONS' para Topic Modeling...")
            analyzed_df['CONS_processed'] = analyzed_df['CONS'].apply(self.preprocess_text_for_lda)
            
            # Extração de Palavras-Chave (aqui é melhor só retornar os dados)
            all_words = " ".join(analyzed_df['CONS_processed'].dropna()).split()
            if all_words:
                word_counts = Counter(all_words)
                print("Top 20 palavras-chave em 'CONS':", word_counts.most_common(20))
                # Em uma aplicação real, você poderia adicionar os tópicos ou keywords como uma nova coluna.

        print("Análise de NLP concluída.")
        return analyzed_df