--- parameters start
DECLARE @THETABLE varchar(100) = <value>; --- What is the table name with schema ?
--- parameters end
--- with results columns
select i.*
  from sys.indexes i
 where i.object_id = OBJECT_ID(@THETABLE)
   and i.name is not NULL;