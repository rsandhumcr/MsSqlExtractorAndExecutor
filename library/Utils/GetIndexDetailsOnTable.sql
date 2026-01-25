--- parameters start
DECLARE @THETABLE varchar(100) = <value>;--- What is the table name ?
--- parameters end
--- with results columns
;
WITH MyCTE AS (
        SELECT T = t.[name],
                A = 'ALTER TABLE [' + schema_name(t.schema_id) + '].[' + t.[name] + '] ADD CONSTRAINT [' + i.[name] + '] PRIMARY KEY CLUSTERED (' + substring(column_names, 1, len(column_names) -1) + isnull(
                        'INCLUDE(' + substring(column_names2, 1, len(column_names2) -1) + ')',
                        ''
                ),
                B = ') WITH (PAD_INDEX = ' + CASE
                        WHEN i.[is_padded] = 0 THEN 'OFF'
                        WHEN i.[is_padded] = 1 THEN 'ON'
                END,
                C = ', STATISTICS_NORECOMPUTE = OFF' + ', SORT_IN_TEMPDB = OFF' + ', IGNORE_DUP_KEY = ' + CASE
                        WHEN i.[IGNORE_DUP_KEY] = 0 THEN 'OFF'
                        WHEN i.[IGNORE_DUP_KEY] = 1 THEN 'ON'
                END,
                D = ', ONLINE = OFF' + ', ALLOW_ROW_LOCKS = ' + CASE
                        WHEN i.[ALLOW_ROW_LOCKS] = 0 THEN 'OFF'
                        WHEN i.[ALLOW_ROW_LOCKS] = 1 THEN 'ON'
                END,
                E = ', ALLOW_PAGE_LOCKS = ' + CASE
                        WHEN i.[ALLOW_PAGE_LOCKS] = 0 THEN 'OFF'
                        WHEN i.[ALLOW_PAGE_LOCKS] = 1 THEN 'ON'
                END,
                F = CASE
                        WHEN i.[fill_factor] = 0 THEN ''
                        WHEN i.[fill_factor] > 0 THEN ', FILLFACTOR = ' + CAST(i.[fill_factor] AS varchar(3))
                END,
                G = ') ON [PRIMARY]'
        FROM sys.objects t
                INNER JOIN sys.indexes i ON t.object_id = i.object_id
                CROSS APPLY(
                        SELECT col.[name] + iif(ic.is_descending_key = 1, ' DESC', ' ASC') + ', '
                        FROM sys.index_columns ic
                                INNER JOIN sys.columns col ON ic.object_id = col.object_id
                                AND ic.column_id = col.column_id
                        WHERE ic.object_id = t.object_id
                                AND ic.index_id = i.index_id
                                and ic.is_included_column = 0
                        ORDER by key_ordinal for xml path ('')
                ) D (column_names)
                CROSS APPLY(
                        SELECT col.[name] + ', '
                        FROM sys.index_columns ic
                                INNER JOIN sys.columns col ON ic.object_id = col.object_id
                                AND ic.column_id = col.column_id
                        WHERE ic.object_id = t.object_id
                                AND ic.index_id = i.index_id
                                and ic.is_included_column = 1
                        ORDER by key_ordinal for xml path ('')
                ) Dinclided (column_names2)
        WHERE i.[is_primary_key] = 1
                AND t.is_ms_shipped <> 1
                AND index_id > 0
        UNION
        SELECT T = t.[name],
                A = 'CREATE ' + CASE
                        WHEN i.[type] = 1 THEN 'CLUSTERED'
                        WHEN i.[type] = 2 THEN 'NONCLUSTERED'
                        WHEN i.[type] = 3 THEN 'XML'
                        WHEN i.[type] = 4 THEN 'Spatial '
                        WHEN i.[type] = 5 THEN 'Clustered columnstore'
                        WHEN i.[type] = 6 THEN 'Nonclustered columnstore'
                        WHEN i.[type] = 7 THEN 'Nonclustered hash'
                END,
                B = ' INDEX  [' + i.[name] + '] ON [' + schema_name(t.schema_id) + '].[' + t.[name] + '] (' + substring(column_names, 1, len(column_names) -1) + ')' + isnull(
                        'INCLUDE(' + substring(column_names2, 1, len(column_names2) -1) + ')',
                        ''
                ) + + ' WITH (PAD_INDEX = ' + CASE
                        WHEN i.[is_padded] = 0 THEN 'OFF'
                        WHEN i.[is_padded] = 1 THEN 'ON'
                END,
                C = ', STATISTICS_NORECOMPUTE = OFF' + ', SORT_IN_TEMPDB = OFF' + ', IGNORE_DUP_KEY = ' + CASE
                        WHEN i.[IGNORE_DUP_KEY] = 0 THEN 'OFF'
                        WHEN i.[IGNORE_DUP_KEY] = 1 THEN 'ON'
                END,
                D = ', ONLINE = OFF' + ', ALLOW_ROW_LOCKS = ' + CASE
                        WHEN i.[ALLOW_ROW_LOCKS] = 0 THEN 'OFF'
                        WHEN i.[ALLOW_ROW_LOCKS] = 1 THEN 'ON'
                END,
                E = ', ALLOW_PAGE_LOCKS = ' + CASE
                        WHEN i.[ALLOW_PAGE_LOCKS] = 0 THEN 'OFF'
                        WHEN i.[ALLOW_PAGE_LOCKS] = 1 THEN 'ON'
                END,
                F = CASE
                        WHEN i.[fill_factor] = 0 THEN ''
                        WHEN i.[fill_factor] > 0 THEN ', FILLFACTOR = ' + CAST(i.[fill_factor] AS varchar(3))
                END,
                G = ') ON [PRIMARY]'
        FROM sys.objects t
                INNER JOIN sys.indexes i ON t.object_id = i.object_id
                CROSS APPLY(
                        SELECT col.[name] + iif(ic.is_descending_key = 1, ' DESC', ' ASC') + ', '
                        FROM sys.index_columns ic
                                INNER JOIN sys.columns col ON ic.object_id = col.object_id
                                AND ic.column_id = col.column_id
                        WHERE ic.object_id = t.object_id
                                AND ic.index_id = i.index_id
                                and ic.is_included_column = 0
                        ORDER by key_ordinal for xml path ('')
                ) D (column_names)
                CROSS APPLY(
                        SELECT col.[name] + ', '
                        FROM sys.index_columns ic
                                INNER JOIN sys.columns col ON ic.object_id = col.object_id
                                AND ic.column_id = col.column_id
                        WHERE ic.object_id = t.object_id
                                AND ic.index_id = i.index_id
                                and ic.is_included_column = 1
                        ORDER by key_ordinal for xml path ('')
                ) Dinclided (column_names2)
        WHERE i.[is_primary_key] = 0
                AND substring(i.[name], 1, 1) != '_'
                AND t.is_ms_shipped <> 1
                AND index_id > 0
)
SELECT T,
        A + B + C + D + E + F + G
FROM MyCTE
WHERE T = @THETABLE
ORDER BY T