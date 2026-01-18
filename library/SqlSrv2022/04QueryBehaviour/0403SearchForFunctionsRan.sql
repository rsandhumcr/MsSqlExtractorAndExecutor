--- parameters start
DECLARE @SearchText VARCHAR(100) = <value>; --- What is the search term ?
--- parameters end
--- with results columns
DECLARE @SearchData VARCHAR(102) = '%' + @SearchText + '%';
SELECT SUBSTRING(dest.text, 1, 30) AS [text],
       deqs.execution_count,
       deqs.min_logical_writes,
       deqs.max_logical_reads,
       deqs.total_logical_reads,
       deqs.total_elapsed_time,
       deqs.last_elapsed_time,
	   dest.text  AS [query_text],
	   deqp.query_plan AS [sqlplan],
	   deqs.last_execution_time
	   ---,deqs.*
FROM sys.dm_exec_function_stats AS deqs
    CROSS APPLY sys.dm_exec_query_plan(deqs.plan_handle) AS deqp
    CROSS APPLY sys.dm_exec_sql_text(deqs.sql_handle) AS dest
WHERE dest.text LIKE @SearchData;