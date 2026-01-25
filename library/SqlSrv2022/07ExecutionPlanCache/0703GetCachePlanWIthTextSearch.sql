--- parameters start
DECLARE @search_term VARCHAR(100) = <value>; --- What word are you searching for ?
--- parameters end
--- with results columns
DECLARE @search_word  VARCHAR(102) = '%' + @search_term + '%' ;

SELECT c.usecounts,
       c.cacheobjtype,
       c.objtype,
	    t.text
FROM sys.dm_exec_cached_plans AS c
    CROSS APPLY sys.dm_exec_sql_text(c.plan_handle) AS t
WHERE t.text LIKE  @search_word