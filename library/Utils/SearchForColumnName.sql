--- parameters start
DECLARE @search_term VARCHAR(100) = <value>; --- How many column name are you searching for ?
--- parameters end
--- with results columns
DECLARE @search_word  VARCHAR(102) = '%' + @search_term + '%' ;

SELECT *
FROM INFORMATION_SCHEMA.COLUMNS
WHERE COLUMN_NAME like @search_word
ORDER BY TABLE_NAME