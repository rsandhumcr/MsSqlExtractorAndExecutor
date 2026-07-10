--- with results rows

SELECT TOP (10) [ProductCategoryID]
      ,[ParentProductCategoryID]
      ,[Name]
      ,[rowguid]
      ,[ModifiedDate]
  FROM [AdventureWorksLT2019].[SalesLT].[ProductCategory]
