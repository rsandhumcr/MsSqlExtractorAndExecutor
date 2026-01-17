---- Get input buffer information for the current database (Query 3) (Input Buffer)
--- with results columns
SELECT es.session_id, DB_NAME(es.database_id) AS [Database Name],
       es.login_time, es.cpu_time, es.logical_reads,
       es.[status], ib.event_info AS [Input Buffer]
FROM sys.dm_exec_sessions AS es WITH (NOLOCK)
CROSS APPLY sys.dm_exec_input_buffer(es.session_id, NULL) AS ib
WHERE es.database_id = DB_ID()
AND es.session_id > 50
AND es.session_id <> @@SPID OPTION (RECOMPILE);