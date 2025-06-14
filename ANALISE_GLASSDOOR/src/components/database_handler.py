# src/components/database_handler.py

import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv

class DatabaseHandler:
    """Gerencia a conexão e as operações com o banco de dados SQL Server."""
    
    def __init__(self):
        load_dotenv()
        self.server = os.getenv('DB_SERVER')
        self.database = os.getenv('DB_DATABASE')
        self.conn_str = f"Driver={{ODBC Driver 17 for SQL Server}};Server={self.server};Database={self.database};Trusted_Connection=yes;"
        self.connection = None
        self.cursor = None

    def connect(self):
        """Estabelece a conexão com o banco de dados."""
        try:
            self.connection = pyodbc.connect(self.conn_str)
            self.cursor = self.connection.cursor()
            print("Conexão com o banco de dados estabelecida com sucesso.")
        except pyodbc.Error as ex:
            print(f"Erro de conexão com o banco de dados: {ex}")
            raise # Lança a exceção para que a pipeline possa tratá-la

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Conexão com o banco de dados fechada.")

    def fetch_data(self, query: str) -> pd.DataFrame:
        """Executa uma query e retorna os resultados em um DataFrame."""
        if not self.connection:
            raise ConnectionError("Conexão não estabelecida. Chame o método connect() primeiro.")
        try:
            print("Executando query para carregar dados...")
            df = pd.read_sql(query, self.connection)
            print(f"Dados carregados: {df.shape[0]} linhas.")
            return df
        except pd.io.sql.DatabaseError as e:
            print(f"Erro ao executar a query: {e}")
            return pd.DataFrame() # Retorna DF vazio em caso de erro

    def write_dataframe(self, df: pd.DataFrame, table_name: str, if_exists: str = 'replace'):
        """
        Salva um DataFrame em uma tabela no banco de dados.
        if_exists: 'replace' (DROP/CREATE/INSERT), 'append', 'fail'
        """
        # Esta é uma implementação simplificada. Para produção, considere uma
        # biblioteca como a `to_sql` do pandas com um engine do SQLAlchemy
        # ou uma inserção mais robusta como a que você tinha.
        if not self.connection or not self.cursor:
            raise ConnectionError("Conexão não estabelecida.")

        if df.empty:
            print("DataFrame está vazio. Nenhuma operação de escrita realizada.")
            return

        print(f"Preparando para escrever dados na tabela '{table_name}'...")
        if if_exists == 'replace':
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"Tabela '{table_name}' antiga removida.")

        # Reutilizando sua lógica de criação de tabela (é ótima!)
        # (Esta parte pode ser movida para uma função helper se ficar muito grande)
        column_definitions = [f"[{col}] NVARCHAR(MAX) NULL" for col in df.columns] # Simplificado para NVARCHAR(MAX)
        create_table_query = f"CREATE TABLE {table_name} ({', '.join(column_definitions)})"
        self.cursor.execute(create_table_query)
        print(f"Tabela '{table_name}' criada.")

        # Inserção de dados
        data_to_insert = [tuple(row) for row in df.itertuples(index=False, name=None)]
        
        placeholders = ", ".join(["?"] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        
        print(f"Inserindo {len(data_to_insert)} linhas...")
        self.cursor.fast_executemany = True
        self.cursor.executemany(insert_query, data_to_insert)
        self.connection.commit()
        print("Dados inseridos com sucesso.")