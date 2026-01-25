--- parameters start
DECLARE @search_term VARCHAR(100) = <value>;--- Enter Table Name ?
--- parameters end
--- with results
SELECT *
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = @search_term
ORDER BY TABLE_NAME