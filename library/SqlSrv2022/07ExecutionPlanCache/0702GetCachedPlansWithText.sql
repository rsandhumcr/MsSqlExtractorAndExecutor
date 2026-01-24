--- with results columns
SELECT c.usecounts,
       c.cacheobjtype,
       c.objtype,
	    t.text
FROM sys.dm_exec_cached_plans AS c
    CROSS APPLY sys.dm_exec_sql_text(c.plan_handle) AS t