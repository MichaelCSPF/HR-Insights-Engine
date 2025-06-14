SELECT *
FROM {table_name}
WHERE CAST(REPLACE(NOTA_GERAL_TEXT, ',', '.') AS FLOAT) < {rating_threshold}