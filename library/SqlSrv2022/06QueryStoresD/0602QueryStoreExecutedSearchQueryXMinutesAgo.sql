--- parameters start
DECLARE @MinutesAgo INT = <value>; --- How many minutes ago [30] ?
DECLARE @search_term VARCHAR(100) = <value>; --- What in the query to searching for ?
--- parameters end
--- with results columns
DECLARE @search_word  VARCHAR(102) = '%' + @search_term + '%' ;

SELECT qsq.query_id,
       qsq.object_id,
	   qsq.last_execution_time,
       qsqt.query_sql_text,
	   qsp.plan_id,
       CAST(qsp.query_plan AS XML) AS QueryPlan
  	   ----, qsq.*,	   *
FROM sys.query_store_query AS qsq
    JOIN sys.query_store_query_text AS qsqt
        ON qsq.query_text_id = qsqt.query_text_id
    JOIN sys.query_store_plan AS qsp
        ON qsp.query_id = qsq.query_id
WHERE qsq.last_execution_time <= DATEADD(minute, (-1 * @MinutesAgo), GETUTCDATE())
AND qsqt.query_sql_text LIKE @search_word;


