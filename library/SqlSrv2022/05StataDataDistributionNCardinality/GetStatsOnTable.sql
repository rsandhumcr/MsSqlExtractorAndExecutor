--- parameters start
DECLARE @table_name VARCHAR(100) = <value>; --- What is the table name with schema int square brackets ?
--- parameters end
--- with results

SELECT s.name,
       s.auto_created,
       s.user_created,
       s.filter_definition,
       sc.column_id,
       c.name AS ColumnName
FROM sys.stats AS s
    JOIN sys.stats_columns AS sc
        ON sc.stats_id = s.stats_id
           AND sc.object_id = s.object_id
    JOIN sys.columns AS c
        ON c.column_id = sc.column_id
           AND c.object_id = s.object_id
WHERE s.object_id = OBJECT_ID(@table_name);

----- Retrieving statistics from the Sales.SalesOrderDetail table
----- DBCC SHOW_STATISTICS(Test1, FirstIndex);

----- Determining the status of statistics on a table
----- EXEC sp_autostats 'HumanResources.Department';

----- Using CREATE STATISTICS on a column
----- CREATE STATISTICS Stats1 ON Test1(C2);
----- CREATE STATISTICS Stats1 ON <table>>(<column>>);

----- Updating the statistics on iFirstIndex
----- UPDATE STATISTICS Test1 iFirstIndex WITH FULLSCAN;


