DECLARE @database_name VARCHAR(100) = 'AdventureWorks';
CREATE EVENT SESSION [QueryAndRecompile]
ON SERVER
    ADD EVENT sqlserver.rpc_completed
    (WHERE ([sqlserver].[database_name] = @database_name)),
    ADD EVENT sqlserver.rpc_starting
    (WHERE ([sqlserver].[database_name] = @database_name)),
    ADD EVENT sqlserver.sp_statement_completed
    (WHERE ([sqlserver].[database_name] = @database_name)),
    ADD EVENT sqlserver.sp_statement_starting
    (WHERE ([sqlserver].[database_name] = @database_name)),
    ADD EVENT sqlserver.sql_batch_completed
    (WHERE ([sqlserver].[database_name] = @database_name)),
    ADD EVENT sqlserver.sql_batch_starting
    (WHERE ([sqlserver].[database_name] = @database_name)),
    ADD EVENT sqlserver.sql_statement_completed
    (WHERE ([sqlserver].[database_name] = @database_name)),
    ADD EVENT sqlserver.sql_statement_recompile
    (WHERE ([sqlserver].[database_name] = @database_name)),
    ADD EVENT sqlserver.sql_statement_starting
    (WHERE ([sqlserver].[database_name] = @database_name)),
    ADD TARGET package0.event_file
    (SET filename = N'QueryAndRecompile')
WITH
(
    TRACK_CAUSALITY = ON
);
GO