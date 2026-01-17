---- Get QueryStore Options for this database (Query 5) (QueryStore Options)
--- with results columns
SELECT actual_state_desc, desired_state_desc,
       current_storage_size_mb, [max_storage_size_mb],
	   query_capture_mode_desc, size_based_cleanup_mode_desc,
	   wait_stats_capture_mode_desc, [flush_interval_seconds]
FROM sys.database_query_store_options WITH (NOLOCK) OPTION (RECOMPILE);