--- parameters start
DECLARE @SearchText VARCHAR(100) = <value>; --- What is the search term ?
--- parameters end
--- with results columns
DECLARE @SearchData VARCHAR(102) = '%' + @SearchText + '%';
SELECT qsq.query_id,
	   SUBSTRING(qsqt.query_sql_text, 1, 30) AS [text],
       qsq.query_hash,
	   qsqt.query_sql_text,
       CAST(qsp.query_plan AS XML) AS [sqlplan]
	   ---,qsqt.*
FROM sys.query_store_query AS qsq
    JOIN sys.query_store_plan AS qsp
        ON qsp.query_id = qsq.query_id
    JOIN sys.query_store_query_text AS qsqt
        ON qsqt.query_text_id = qsq.query_text_id
WHERE qsqt.query_sql_text LIKE @SearchData;