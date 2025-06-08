---   SELECT * FROM SalesLT.ProductCategory WHERE ProductCategoryID = 2 
---   USE AdventureWorksLT2019; 
IF NOT EXISTS( SELECT * FROM SalesLT.ProductCategory WHERE ProductCategoryID = 2)   
 BEGIN  
   SET IDENTITY_INSERT SalesLT.ProductCategory ON; 
--- INSERT INTO [AdventureWorksLT2019].SalesLT.ProductCategory (
    INSERT INTO SalesLT.ProductCategory (
   [ProductCategoryID]  ,[ParentProductCategoryID]  ,[Name]  ,[rowguid]  ,[ModifiedDate] 
    )
    VALUES 
      (2 ,NULL ,'Components' ,'C657828D-D808-4ABA-91A3-AF2CE02300E9' ,'2002-06-01 00:00:00'
    );

   SET IDENTITY_INSERT SalesLT.ProductCategory OFF; 
 END  

--- 2024-09-06 20:56:29  



---   SELECT * FROM SalesLT.ProductCategory WHERE ProductCategoryID = 18 
---   USE AdventureWorksLT2019; 
IF NOT EXISTS( SELECT * FROM SalesLT.ProductCategory WHERE ProductCategoryID = 18)   
 BEGIN  
   SET IDENTITY_INSERT SalesLT.ProductCategory ON; 
--- INSERT INTO [AdventureWorksLT2019].SalesLT.ProductCategory (
    INSERT INTO SalesLT.ProductCategory (
   [ProductCategoryID]  ,[ParentProductCategoryID]  ,[Name]  ,[rowguid]  ,[ModifiedDate] 
    )
    VALUES 
      (18 ,2 ,'Road Frames' ,'5515F857-075B-4F9A-87B7-43B4997077B3' ,'2002-06-01 00:00:00'
    );

   SET IDENTITY_INSERT SalesLT.ProductCategory OFF; 
 END  

--- 2024-09-06 20:56:29  



---   SELECT * FROM SalesLT.ProductModel WHERE ProductModelID = 6 
---   USE AdventureWorksLT2019; 
IF NOT EXISTS( SELECT * FROM SalesLT.ProductModel WHERE ProductModelID = 6)   
 BEGIN  
   SET IDENTITY_INSERT SalesLT.ProductModel ON; 
--- INSERT INTO [AdventureWorksLT2019].SalesLT.ProductModel (
    INSERT INTO SalesLT.ProductModel (
   [ProductModelID]  ,[Name]  ,[CatalogDescription]  ,[rowguid]  ,[ModifiedDate] 
    )
    VALUES 
      (6 ,'HL Road Frame' ,NULL ,'4D332ECC-48B3-4E04-B7E7-227F3AC2A7EC' ,'2002-05-02 00:00:00'
    );

   SET IDENTITY_INSERT SalesLT.ProductModel OFF; 
 END  

--- 2024-09-06 20:56:29  



---   SELECT * FROM [SalesLT].[Product] WHERE ProductId = 680 
---   USE AdventureWorksLT2019; 
IF NOT EXISTS( SELECT * FROM [SalesLT].[Product] WHERE ProductId = 680)   
 BEGIN  
   SET IDENTITY_INSERT [SalesLT].[Product] ON; 
--- INSERT INTO [AdventureWorksLT2019].[SalesLT].[Product] (
    INSERT INTO [SalesLT].[Product] (
   [ProductID]  ,[Name]  ,[ProductNumber]  ,[Color]  ,[StandardCost] 
     ,[ListPrice]  ,[Size]  ,[Weight]  ,[ProductCategoryID]  ,[ProductModelID] 
     ,[SellStartDate]  ,[SellEndDate]  ,[DiscontinuedDate]  ,[ThumbNailPhoto]  ,[ThumbnailPhotoFileName] 
     ,[rowguid]  ,[ModifiedDate] )
    VALUES 
      (680 ,'HL Road Frame - Black, 58' ,'FR-R92B-58' ,'Black' ,1059.3100
     ,1431.5000 ,'58' ,1016.04 ,18 ,6
     ,'2002-06-01 00:00:00' ,NULL ,NULL ,CONVERT(varbinary, 'b"b''GIF89aP\\x001\\x00\\xf7\\x00\\x00"') ,'no_image_available_small.gif'
     ,'43DD68D6-14A4-461F-9069-55309D90EA7E' ,'2008-03-11 10:01:36');

   SET IDENTITY_INSERT [SalesLT].[Product] OFF; 
 END  

--- 2024-09-06 20:56:29  



---   SELECT * FROM dbo.ReferenceTable01 WHERE id = 1 
---   USE testDb; 
IF NOT EXISTS( SELECT * FROM dbo.ReferenceTable01 WHERE id = 1)   
 BEGIN  
--- INSERT INTO [testDb].dbo.ReferenceTable01 (
    INSERT INTO dbo.ReferenceTable01 (
   [id]  ,[Reference01]  ,[Description]  ,[Other] )
    VALUES 
      (1 ,1 ,'Item One' ,'The Other 1');

 END  


