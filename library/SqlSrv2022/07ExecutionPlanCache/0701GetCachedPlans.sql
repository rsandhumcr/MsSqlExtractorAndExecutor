--- with results columns
SELECT decp.refcounts,
       decp.usecounts,
       decp.size_in_bytes,
       decp.cacheobjtype,
       decp.objtype,
       decp.plan_handle
FROM sys.dm_exec_cached_plans AS decp;