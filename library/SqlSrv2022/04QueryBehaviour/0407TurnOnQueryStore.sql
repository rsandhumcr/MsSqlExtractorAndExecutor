----- Enabling query store for db. ALTER DATABASE not allowed here.
----- In SSMS go to the DB right click, select 'Properties', select option 'Query Store', set option 'Operation Mode' 'Read write'
----- ALTER DATABASE <database_name> SET QUERY_STORE = ON (OPERATION_MODE = READ_WRITE);
--- with results columns
SELECT 'Execute ''ALTER DATABASE <database_name> SET QUERY_STORE = ON (OPERATION_MODE = READ_WRITE);'' in SSMS' AS Text