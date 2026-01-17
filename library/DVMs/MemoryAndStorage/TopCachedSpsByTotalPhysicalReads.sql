---- Top Cached SPs By Total Physical Reads.
---- Physical reads relate to disk read I/O pressure  (Query 4) (SP Physical Reads)
--- with results columns
SELECT TOP(25) p.name AS [SP Name],qs.total_physical_reads AS [TotalPhysicalReads],
qs.total_physical_reads/qs.execution_count AS [AvgPhysicalReads], qs.execution_count,
qs.total_logical_reads,qs.total_elapsed_time, qs.total_elapsed_time/qs.execution_count AS [avg_elapsed_time],
CASE WHEN CONVERT(nvarchar(max), qp.query_plan) LIKE N'%<MissingIndexes>%' THEN 1 ELSE 0 END AS [Has Missing Index],
FORMAT(qs.last_execution_time, 'yyyy-MM-dd HH:mm:ss', 'en-US') AS [Last Execution Time],
FORMAT(qs.cached_time, 'yyyy-MM-dd HH:mm:ss', 'en-US') AS [Plan Cached Time]
,qp.query_plan AS [Query Plan]
FROM sys.procedures AS p WITH (NOLOCK)
INNER JOIN sys.dm_exec_procedure_stats AS qs WITH (NOLOCK)
ON p.[object_id] = qs.[object_id]
CROSS APPLY sys.dm_exec_query_plan(qs.plan_handle) AS qp
WHERE qs.database_id = DB_ID()
AND qs.total_physical_reads > 0
ORDER BY qs.total_physical_reads DESC, qs.total_logical_reads DESC OPTION (RECOMPILE);