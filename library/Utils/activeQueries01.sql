--- with results columns
SELECT Qry.last_execution_time,
    Txt.query_text_id,
    Txt.query_sql_text,
    Pl.plan_id,
    Qry.*,
    txt.*,
    pl.*
FROM sys.query_store_plan AS Pl
    INNER JOIN sys.query_store_query AS Qry ON Pl.query_id = Qry.query_id
    INNER JOIN sys.query_store_query_text AS Txt ON Qry.query_text_id = Txt.query_text_id
WHERE Qry.last_execution_time >= DATEADD(Day, -1, Getdate())
ORDER BY 1 DESC;