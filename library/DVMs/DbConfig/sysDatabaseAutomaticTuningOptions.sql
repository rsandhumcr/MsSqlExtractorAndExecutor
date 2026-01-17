---- Get database automatic tuning options (Query 6) (Automatic Tuning Options)
--- with results columns
SELECT [name], desired_state_desc, actual_state_desc, reason_desc
FROM sys.database_automatic_tuning_options WITH (NOLOCK)
OPTION (RECOMPILE);