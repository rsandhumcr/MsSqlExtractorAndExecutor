----- Removing all information from Query Store
----- ALTER DATABASE AdventureWorks SET QUERY_STORE CLEAR;
----- ALTER DATABASE <Database name> SET QUERY_STORE CLEAR;

----- Removing a query or a plan from Query Store
----- EXEC sys.sp_query_store_remove_query @query_id = @QueryId;
----- EXEC sys.sp_query_store_remove_plan @plan_id = @PlanID;

----- Removing a query or a plan from Query Store
----- EXEC sys.sp_query_store_remove_query @query_id = @QueryId;
----- EXEC sys.sp_query_store_remove_plan @plan_id = @PlanID;

----- Flushing Query Store from memory to disk
----- EXEC sys.sp_query_store_flush_db;

----- Retrieving all current Query Store settings
----- SELECT * FROM sys.database_query_store_options AS dqso;

----- Changing the maximum storage size for the Query Store
----- ALTER DATABASE AdventureWorks SET QUERY_STORE (MAX_STORAGE_SIZE_MB = 200);
----- ALTER DATABASE <Database name> SET QUERY_STORE (MAX_STORAGE_SIZE_MB = 200);

----- Forcing an execution plan
----- EXEC sys.sp_query_store_force_plan 550, 339;
----- EXEC sys.sp_query_store_force_plan <query_id>, <plan_id>;

