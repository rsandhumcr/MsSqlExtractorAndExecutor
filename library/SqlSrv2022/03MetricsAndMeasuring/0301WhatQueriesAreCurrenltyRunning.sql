--- with results columns
SELECT
    s.login_name,
    r.command,
    r.status,
    r.start_time,
    r.total_elapsed_time,
    r.cpu_time,
    r.logical_reads,
    r.writes,
    r.reads,
    r.text_size,
    r.statement_start_offset,
    r.statement_end_offset,
    q.text AS [query_text],
    r.database_id,
    r.user_id,
    r.blocking_session_id,
    r.wait_type,
    r.wait_time,
    r.last_wait_type
FROM
    sys.dm_exec_requests r
INNER JOIN
    sys.dm_exec_sessions s ON r.session_id = s.session_id
CROSS APPLY
    sys.dm_exec_sql_text(r.sql_handle) AS q
WHERE
    r.start_time >= DATEADD(DAY, -1, GETDATE()) -- Queries executed in the last 24 hours
ORDER BY
    r.start_time DESC;