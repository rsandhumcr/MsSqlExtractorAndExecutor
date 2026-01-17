---- Look at UDF execution statistics (Query 2) (UDF Statistics)
--- with results columns
SELECT OBJECT_NAME(object_id) AS [Function Name], total_worker_time,
       execution_count, total_elapsed_time,
       total_elapsed_time/execution_count AS [avg_elapsed_time],
       last_elapsed_time, last_execution_time, cached_time
FROM sys.dm_exec_function_stats WITH (NOLOCK)
WHERE database_id = DB_ID()
ORDER BY total_worker_time DESC OPTION (RECOMPILE);