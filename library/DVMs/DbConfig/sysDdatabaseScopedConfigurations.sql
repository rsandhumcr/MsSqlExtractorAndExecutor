---- Get database scoped configuration values for current database (Query 3) (Database-scoped Configurations)
--- with results columns
-----SELECT configuration_id, [name], [value] AS [value_for_primary]
SELECT configuration_id, [name], convert(varchar(50), [value]) AS [value_for_primary]
FROM sys.database_scoped_configurations WITH (NOLOCK) OPTION (RECOMPILE);