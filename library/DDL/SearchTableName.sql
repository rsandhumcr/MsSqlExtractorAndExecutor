--- parameters start
DECLARE @search_term VARCHAR(100) = <value>;--- What table name are you searching for ?
--- parameters end
--- with results
DECLARE @search_word VARCHAR(102) = '%' + @search_term + '%';
SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME like @search_word
ORDER BY TABLE_NAME