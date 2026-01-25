--- parameters start
DECLARE @MinutesAgo INT = <value>;--- How many minutes ago [30] ?
--- parameters end
--- with results columns
SELECT top 100 sdest.DatabaseName,
    sdes.session_id,
    qs.last_execution_time,
    sdes.[host_name],
    sdes.[program_name],
    sdes.client_interface_name,
    sdes.login_name,
    sdes.login_time,
    sdes.nt_domain,
    sdes.nt_user_name,
    sdec.client_net_address,
    sdec.local_net_address,
    sdest.ObjName,
    sdest.Query
FROM sys.dm_exec_sessions AS sdes
    INNER JOIN sys.dm_exec_connections AS sdec ON sdec.session_id = sdes.session_id
    CROSS APPLY (
        SELECT db_name(dbid) AS DatabaseName,
            object_id(objectid) AS ObjName,
            ISNULL(
                (
                    SELECT TEXT AS [processing-instruction(definition)]
                    FROM sys.dm_exec_sql_text(sdec.most_recent_sql_handle) FOR XML PATH(''),
                        TYPE
                ),
                ''
            ) AS Query
        FROM sys.dm_exec_sql_text(sdec.most_recent_sql_handle)
    ) sdest
    CROSS APPLY sys.dm_exec_query_stats qs
where sdes.session_id <> @@SPID ---and sdes.nt_user_name like '%Your_User_Name%'   --UserName
    AND qs.last_execution_time >= DATEADD(minute, (-1 * @MinutesAgo), GETUTCDATE())
ORDER BY qs.last_execution_time DESC;