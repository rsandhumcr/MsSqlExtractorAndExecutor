--- parameters start
DECLARE @MinutesAgo INT = <value>; --- How many minutes ago [30] ?
--- parameters end
--- with results columns
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
FROM sys.dm_exec_trigger_stats AS deqs
    CROSS APPLY sys.dm_exec_query_plan(deqs.plan_handle) AS deqp
    CROSS APPLY sys.dm_exec_sql_text(deqs.sql_handle) AS dest
WHERE deqs.last_execution_time >= DATEADD(minute, (-1 * @MinutesAgo), GETUTCDATE());