---   SELECT * FROM [SalesLT].[Product] WHERE ProductID = 741 
---   USE AdventureWorksLT2019; 
IF NOT EXISTS( SELECT * FROM [SalesLT].[Product] WHERE ProductID = 741)   
 BEGIN  
   SET IDENTITY_INSERT [SalesLT].[Product] ON; 
--- INSERT INTO   [AdventureWorksLT2019].[SalesLT].[Product] (
    INSERT INTO   [SalesLT].[Product] 
      ( [ProductID]  ,[Name]  ,[ProductNumber]  ,[Color]  ,[StandardCost] 
     ,[ListPrice]  ,[Size]  ,[Weight]  ,[ProductCategoryID]  ,[ProductModelID] 
     ,[SellStartDate]  ,[SellEndDate]  ,[DiscontinuedDate]  ,[ThumbNailPhoto]  ,[ThumbnailPhotoFileName] 
     ,[rowguid]  ,[ModifiedDate] )
    VALUES 
      (741 ,'HL Mountain Frame - Silver, 48' ,'FR-M94S-52' ,'Silver' ,706.8110
     ,1364.5000 ,'48' ,1270.05 ,16 ,5
     ,'2005-07-01 00:00:00' ,'2006-06-30 00:00:00' ,NULL ,CONVERT(varbinary, 'b''GIF89aP\x001\x00\xf7\x00\x00\xc1\xc3\xbd\xf4\xf4\xf4\xbb\xcc\xc9\xec\xea\xea\xc2\xd4\xd1\xac\xc2\xbb\xb5\xb8\xb4\xda\xda\xda\xb8\xba\xb5\xab\xb8\xb4\xaa\xb5\xb2\xe8\xe6\xe6\xd6\xd5\xd5\xa8\xb4\xad\xea\xea\xea\xc7\xc8\xc4\xb0\xb2\xac\xa6\xb3\xb3\xe2\xe2\xe2\xdf\xde\xde\xe1\xe0\xe0\xec\xec\xec\xb3\xbd\xbb\xf0\xf0\xf0\xcd\xd2\xcc\xd4\xd9\xd4\xf4\xf2\xf3\xc2\xd2\xcd\xea\xe8\xe8\xe4\xe2\xe2\xe6\xf3\xf3\xdc\xdc\xdc\xca\xdb\xd9\xf2\xf2\xf2\xa4\xa5\xa3\xf0\xee\xee\xad\xad\xac\xab\xbd\xbb\xb4\xc9\xc3\xa5\xb1\xad\xce\xcd\xcd\xe5\xe4\xe4\xd1\xd2\xcd\xdf\xdd\xdd\xd8\xd8\xd8\xee\xec\xec\xcd\xcf\xca\xd9\xe9\xe9\xf5\xf3\xf3\xe6\xe5\xe6\xbe\xbf\xbd\xee\xee\xee\xd9\xd6\xd6\xb4\xb6\xb0\xd8\xda\xd6\xbc\xbd\xb9\xe0\xe1\xde\xc8\xca\xc4\xe7\xe4\xe4\xc6\xc5\xc5\xf2\xf0\xf1\xf7\xf4\xf4\x9d\x9c\x9a\xb4\xc2\xbb\xe8\xe7\xe8\xe3\xe0\xe1\xdc\xde\xda\xbd\xc0\xba\xc2\xc1\xc1\xf9\xf2\xf1\xb9\xbd\xb9\xb9\xba\xb8\xe4\xe3\xe4\xa5\xad\xab\xfb\xfc\xfc\xe9\xe8\xe8\xd8\xd6\xd8\xad\xaf\xaa\xdc\xdb\xdc\xfa\xf8\xf8\xe4\xe5\xe2\xe0\xde\xe0\xa9\xaa\xa9\xed\xec\xec\xcb\xd8\xd5\xda\xd9\xda\xaa\xad\xa6\xde\xdc\xde\xbf\xc1\xbc\xa6\xb8\xb9\xf8\xf7\xf7\xda\xdc\xd8\xd4\xd2\xd1\xc9\xc9\xc9\xe8\xe8\xe7\xc4\xc4\xc1\xba\xc9\xc7\xec\xea\xec\xb5\xb6\xb4\xd3\xd5\xd2\xb0\xc2\xc2\xdd\xdc\xdd\xe3\xd9\xd9\xb1\xb2\xb0\xb4\xc6\xc5\xae\xc0\xc0\xcc\xca\xcb\xf2\xee\xee\xb5\xc5\xc2\xb2\xb6\xb3\xf1\xef\xef\xca\xcd\xc8\xe2\xe0\xe2\xe6\xdb\xdb\xbf\xc2\xc1\xda\xdf\xdd\xbe\xd0\xce\xbf\xc5\xc2\xd4\xd3\xd4\xc4\xc9\xc8\xfc\xfb\xfb\xe6\xe4\xe6\xe3\xe4\xe2\xc1\xc6\xc0\xb3\xc4\xc3\xca\xc7\xc8\xbd\xc7\xc6\xee\xed\xed\xc0\xce\xce\xd6\xe1\xe1\xdc\xda\xdb\xfc\xfb\xfc\xc7\xce\xcd\xf6\xef\xef\xca\xd5\xd4\xc5\xd8\xd5\xfc\xfc\xfb\xfa\xfa\xf9\xc2\xcd\xcb\xf4\xf0\xf1\xbb\xc2\xc1\xeb\xea\xe8\xde\xe1\xdd\xdb\xda\xdb\xb2\xc6\xc6\xa6\xab\xa6\xe1\xe0\xe1\xdd\xde\xdc\xde\xdd\xde\xd9\xd8\xd9\xdf\xdd\xe0\xd1\xd2\xd1\xb5\xc3\xc3\xfd\xfd\xfd\xfc\xfc\xfc\xfb\xfb\xfb\xf8\xf8\xf8\xfb\xfa\xfa\xf7\xf7\xf7\xfa\xfa\xfa\xf9\xf9\xf9\xfe\xfd\xfd\xf9\xf8\xf8\xf7\xf6\xf6\xf6\xf6\xf6\xfd\xfc\xfc\xfb\xfa\xfb\xfb\xfb\xfa\xfd\xfc\xfd\xf8\xf7\xf8\xf8\xf8\xf7\xfe\xfd\xfe\xf0\xed\xed\xf2\xf1\xf1\xfe\xfe\xfd\xfd\xfe\xfe\xf7\xf7\xf8\xf7\xf7\xf6\xf7\xf6\xf7\xfd\xfd\xfe\xf4\xf4\xf3\xea\xe9\xe9\xf9\xf8\xf9\xf2\xf2\xf1\xfa\xfa\xfb\xf0\xef\xed\xf3\xf3\xf3\xfc\xfc\xfd\xe1\xe2\xe0\xfd\xfd\xfc\xf6\xf6\xf5\xf8\xf9\xf9\xf0\xf0\xef\xeb\xeb\xeb\xed\xee\xed\xf8\xf8\xf9\xf6\xf5\xf5\xda\xe2\xe2\xf8\xf9\xf8\xe4\xdd\xdd\xf8\xfe\xfe\xf1\xf1\xf1\xf9\xf9\xf8\xe2\xe7\xe6\xe3\xe3\xe3\xe0\xeb\xeb\xf2\xec\xec\xbb\xc0\xbb\xef\xef\xef\xb8\xc2\xbf\xe3\xe3\xe0\xe7\xe7\xe7\xf3\xf4\xf3\xf6\xf6\xf7\xc3\xc9\xc9\xf7\xf2\xf3\xc5\xc3\xc4\xf4\xf1\xf1\xfc\xfd\xfc\xbe\xc4\xbe\xc0\xc0\xbe\xef\xf4\xf4\xfc\xfd\xfd\xf5\xf6\xf5\xfa\xfb\xfb\xae\xaf\xaf\xd8\xcf\xd0\xcf\xdf\xe0\x8d\x97\x96\x81\x80\x80\xea\xd9\xd9\xfd\xfe\xfd\xc0\xc6\xc5\xd5\xdd\xd9\xb9\xbe\xbc\xb9\xb8\xb7\xf0\xeb\xeb\xf0\xeb\xec\xf1\xec\xeb\xcf\xcf\xce\xe1\xdc\xdc\xee\xee\xed\xc1\xc0\xc0\xe9\xea\xe8\xe9\xea\xea\xfa\xf9\xf9\x9a\xae\xae\xc3\xd0\xd0\xe4\xe7\xe7\xe6\xd4\xd4\xe7\xe7\xe4\xd7\xd6\xd7\xac\xac\xac\xa7\xaf\xae\xfe\xfe\xfe\xff\xff\xff!\xf9\x04\x00\x00\x00\x00\x00,\x00\x00\x00\x00P\x001\x00\x00\x08\xff\x00\xff\t\x1cH\xb0\xa0\xc1\x83\x08\x13*\\\xc8\xb0\xe1\xc0L\x0e#\n\xf47j\x04;g\x85\n\x15\xd9\xb8\xd1\x9d\x06\x89\x12\xfd\x05\x90\xc0\x89\xa0\xa6\x003>\t\x0c\x05R 1x\xf0\x8e\x991\x13\x87\xa6\xb9|\xf9\x8e\x8dj\xe9\xd0\x1f\xb4G\xcc<)\xd1\xb5\x80\x12\x8b}\x12\xdc\\\x08\xb2\xa6\xa5\xbfL\x99^\xa1"6\x05\x08\r\x1a\xf0F\xf8\xe3\x19\x91\x18\x03;U\x9c\xd8\xb1C\t\x88\x84GQ(=\xd2\xc1u\xa0\xa6`\xccR\\\xd0\xd66"8h\x94\x180\x80\xb3S\xe0\x14l;\xec\xf0\xa8\xfb\x8f\xd3\x1f\r\xb3\x08GTY\xeaQ%\x88\x03\xbb\xa1\x13\xd1G15`\x8a%\x12\x0b\xf1/\xca\x95\x82\x1e\x0c\x88@\x01\xaa\xae\xbf\x11\xba2G\xd4\xf51\x06\x83T\x03\xfd\xbd\x10Ab\xcc\x1c\x1c\x03\xb4\xf0\xdc\x14L\x95\xea\x86\xfe\x86m\x95\xc5\x80R\''\x81\xc8\x08\xf0;\xd3\x84\x0f\x01\x10\xe9\x1cq\xf0\x15\xd1_\xab\x01\x90\x7f+\xdc\xf5j`2\x06U\x82\xf5\xff\xf0`\xe1\xc6\x9e1_\xdaDHC\x87J\x06!\xfa`l\x15\xf8*\xd3\xfc\x81\x14\xd6\xa9\xc9\xae\xdd\xa1\x16\t\xfb\x88s\xc7\x19D\xf4#\x04)\x9e0\xa3\x06\x02\n\x94 \x00\x01T\xd8 M.\x9a\x1c\xb4\xc9%\xeb\xc8\x80K\x7f-m2\xc2=b\xdc\x90\x04\x1a8\x10#\x10\x1eS0 C\x83h\xd0a\xc8{\x8d\xf8\xe6]\x172\xbc\xc1!O\xc8\x08 C\r5\x9c\x00\x06\x05\x01\x14\xa4\xc1\n\x0f\x18\x90\x00\x19\x02l\x80A\x06z\xd0\xf2O-; 0\xc9\x8d\t\x9d\xf4G-K\xd4\x12L+Z4c\x017\x08P`\xc0\t\x80\xec\x00\xcdA\xf5L\xf3\x8e\x11\t\xa4a\x02\x1bu\xbc\xf1\x06\x11C8i\xd0 \x01T\xe0\xc54\xd3\xd0\x93L*\xf7\xb5DL\nNTQ\x05%\x948\xf1H\x15\x82\xd0q\x04\x02.\xfc\xe3\x00\x04\x11(\x82\r)\t\xb9\x12\x0f\rr$\xa0\x80\x14R\xc8\x80\x85\x04\x05\xe9\xc2\x8c\x13N\x94Q\x86\x13\x82T\xc1B%\x13T\xff\xc0_C\x9cH\xc0\x82\x13Ax1\x80\x1b\xd9\xb8\xd1\xc2\x00\x1f\xf0\xc1M\x13\x07\x08\xc4\x8b\x15Y(\x82B\x85\x0b\x11\x83\xc3\x03g\xc8\xf0\xc3\xa8\x02\xc9"\xc9\x01\x12\xec\xbaH60h\xb0\xc6\x00\x0bDQ\xc5\x01g:\xf4\x07\x0b\x8fH\xd0\xc2(\xb3\xe2Q\x0c\x1b24a\x07\x12\x15\xda`E\tw\xd8\xe1\x10\x14\x06`\xa1@\x01X,\xa0A\x15\x1d\xb4\x00\x83(\xae\x18\x84\x07\x0cS\xe8P\x85\x04\xcc*\x04\x04\x03\x13\x0cP\xdaA\xa1\xbc\xc0\x88\x01(,\xc0\xc2\x07\xa5\xa9\x10I\x1auL\xd0\x90\x0b\x06<\xa0B\x03&4\x81\xc2\x1fk\x1c\xa7P&\xd7\xb40\xc1\x07*%4\xcd>p\xb4"P&\x11\x0fT\x0f\x082 \x00\x8a&\xd3TR\xc5\''\xbb\xb8\x10\t\x19\xea\x00\xb1\x90&C\x1c\xa1\xc2,c\x9cP\x00\tH$\xe4\xcfS\x03\x892\x05\x05N\x04M\xd0\x1f\xfb\xa4`\xe2D\xb3\xfe\xd3\x8d\xa3\xef\xac\xc4\xc1>\x94\xf8\x03\xca\x17Ida\x84\xcf\t\x01\xff#\xc6\x108\xfc\x03D\x8f&\xec\x80\xe9D`\xffc\x1fD\xf3\xd9R\x0b\x05&\x1b\xe4\t\x0b\x14\xc0\x10\xdbA\xfe4\xe3\x07\x02\xc2\xfc\xb3U&y0\x10\xc3?\x01\xdc\xd0O\t\x0f\xe8\x86\xd0$g\xec\x91\x0c,\x95P\x00\xc0\t&\xacc\xf9S`\x7fm\xdfV`sR\xcb\x07\xb5\x18D\xf6\x08\x04\x05:\x10\x0c\xe30\xf2@A\x9dL\xc0@\x90\xc2\x8c\x89\x06\x17f\x0f\xf4\x86\x18.\x98bI\x19\xad|\xf2\x80\xd6\xe1x\xa2\xf8\xd7\x9e?\xb5{\xc4\x1aLSEI\xde\xb1\x10\x03K\x9e\''T\xc1!F\xf0b\xd0\x05\x95D!\xd0<\x94\x92\xc1\xc0A\xbf\xa8\x9a\x10\xdc\xc0\x84\x01l\x85\x13\x00h@\x01\xc4`\x8a\xddy.\x13\x9b\xd0\x84?$\xb8\x92\x7f\x8c\x8dT\x03I\x0bg~\xd6\xb6\x7f\xe0a\x19\x80\x00\xc0\x13\xe6C>\x7f a\x1f\x96\xfb\x07/\x9a\x10\x81\x04P\xc0 \xc1\xa8\x01\x16\xbc\x10\x85\x15\xac\xed\x1f\xc4\xb8\x81\x02\x8f0\x08\xfbxN\x13\x9f\x80\n\t\xff\x05"\n \x1c\xe0b\x9e\xa8B\x0c\xf8c\xbc\xadh!\x10~`\x01B.\xc0\x82\x14\x0cd\x0b\xc8J@\xf0\x08\xb2\x853\xbca\x00\x95\x18@An\xc1\xa0\x12\xc8#b@\xf3a\xfc\x062\x85\t\x04C \xc1\xa8\xc2\x1f\x1a\xc2\x03\x10lc\x8e\xc6\xfb\xc7&(\xf0\x08f\xf9C\x05\x08\xc8B4T\''\x90\x1c\xd4 \x03H\x10D\n\t\x12\x83\x1a$\xa0\x00N\xb8\x1c\t\xcd\''\x90\x00 \xe1\x85\xff\x90\xc0\x04nX\xbc\x89\xfcc\x15\xcc \x80\x0b\x06\xa1\x84<>\xa9\x12A\x12\x08.00\x04H\xd4Af\xc60\x82\x11\xa0\x00\x07\t\xd4\xe3 8\x80@\x026\xc0\x81\x07\x16O\x88\x02\xf9\x04\x10(q\nMP"\x05\x9b\xf0\xe4A4\x91\nB\xb0a\x05\xe4;\x88\x1b\xaa0\x05\x82x\xe2\x01\xcf\xc8\xc2\x1d\x04\xa2\x07\x11\xec\xe1\x0fU\x00\x82)\xff1\t]\x12\x00\x8f\x04\x11\xe2}XQ\x06]p\xc2\t\xe2\xc4\xdc@:\x11\x046X\xa0\x07\x08\xd9\n\x0c\xca\xb0\xff\x80\x82\x84\x00\x00\xea\xb0G\x06\xfe\x01\x01\x1f\xbc\xe3,\x03\xd0\x84BQ\xa1\x89Rd\x82\xa1\xa8`A\x13\x12 \x80\xd1\x95\x0f!n\x98\xc0\x1f\x02\xf0\x88-z-\x17}H\x00\x06\xc6\xb7F\x82\x8c"\n]+H\x05\x10\x90\x04\x13L\xa0\x1c\xfc@\x01\x12\xf2\xc0\x8aMt\xa2\x98\n]\xc5*4Q\x8f\x16`\xc1\n\x11\xc0\x04[\xb2\x13M\x81\xf0`\x02\x0e\xd0\xc5#\xc4\xa8\x90N\\B\x0e\xdcH\x01\x0fL\x91\x10-H\x02\x83\x05\xd1\xc3:\xd0a\x01\x1f\xc8\xe3\x1dS\x08\xc3G\x14\xd7\t\x18\x8c\x00\n[\xc0\xc0\x1e~`\x01\x11\xf8\xe0\x04\x98\x10\x05(\xd8g\x10\r 5\x00N`j>\x031\x0e9p\xe1\t\xa5\xc8\''\x0e%\x91\xd2\x82\xd8\xa2\x0fg\xe0\x87\x14\xd6\xb1\x83J\xa8\x81\x06\x14\xa8\xc4\x180\xb0\x01\x01\xbc\x89\x0cd\xb0@\x02Dp\x03\x17\x90C\x0e\x99\xf8D\xf5\xfe\xd1\nJ\x04\xc3\x13NX\x82B\xfc\x81\x8f\x00\xd0\xe0\x0f\xbfh\x96$\xf2`\x90U\xffh\x00\x06D\xe0G8d\x10\x0ekX\xe0\x1e\x878\x04\x01\xe8\x00\x86\x1f\x18\xa0\r<\xba\x01\x00  \x05\xe90\x00\x829+\x08\x0f\xae0\x82M\x1c3\xb0\x82\xc5\x83$P\xb1\x89q\n\x04\x06Q\xf0\xe8@6\xf1\xa7\x10t\x81\x08\xf7@\xc3=\x0cA\x88=l\x03\x0b\x00x\x80\x0bl\xc0\x8bZ\xb8\x81\x13\xbe\xc0\x007Pp&\x7fxb\xb4<p\x82\xe5$A\x01\xba^.~@C\\BF@\x89\x0b\x18\xe4\x13\x01\xd0\xc4&\x06\xb0\x83\xafr\xa1\x0fj\xa0@\x05t\xf1\x89<~#\x18\xc18@-\xe6\x9a\xcc\xa2z\xae\x16WPI-\xb8W\x90!\x96\xd4\xc4\x04)\x05\x07\x9cp1\x82l\xa2\x15\xb0\xf0\x04(b0\rb\xc0b\x00\xb5\x80M\x8b\xdd"\x81%h\x02*\xca\xbc\x0f\'':\x00\x87J\x1e \x9eCVpI\r2\xa8&\x1b\xc4\x1f\x17 \x86\xc1t\xa1\x05Nh\xe2\x0f\x0bxcB2\xe1\x80\t\x102\xc9\x02I\x86i\''B\t\n\x88\xaf\xff\x93\x07^m\x1b\xaby\x10U\x04@\x0b\x1a\xd0@\x00Z \x0bRD\x81$\x08\x01\xda\x00$\xe0\x1b&\x0e\xa4\x14\xc1xD\x8d+\xe0\x84\x16\x04\xea\xd1\x0c\x19\x05\x10\xca0\xdaJ\xba\xa1\x150\x08@\''\xb4\xd0\t\t8\xc1\r_Sh\''Lq\x8aN\xd8\xe2\x14\xa2U\xe6\x81\xb3!\x01f\xa4\xf3\x03)\xc0\xa7\xaa\xa7Lk\xc5\r\xa0b\x0b\x19E\xa6Q\xe3\tD\x04\xa0b0\xd0D1}\x08c\x18\xffC\x14\x1c8\xc0\x9b\xe3\x97\x8cGp\xe08x\x80\xb4\xb1\x07\xf2\x87\x14P\x02~\n\xe1\xc4&\xf0\xd0\x0b\xf2\xc5\xa0\xd1\xd8\x962\x9c\x07b\n\x0eL\xc0\x0b\x07\x89A\xc5:\xe1\x8d\x820.!\xc9X\xc0#8\x19\xe8j\x18/\x13NH\xca}\xbef\xca\xfb\x84\x82\x15\x1d\x98@\x073\x11\x05\n\xb0\xe3\x96\x0fi\xdb}.\x00\x84G\xcc\xa0!\x9e\xb8@\xc2\n\xa2\x85*\x8e\x00\x11\xf1\xcbc\xa0z\n\x04\x1a\''d\x13\x13\x90@;\xe43k\xe6U\xe5\x11\x15\xc3hH&*\x80\x04R\xe41\x00U\xacE\ny\xc7\xbb\xe2\xb5\xa2\x16)P\xf6B2\xc1\x0cJ\x0c\xa0\x05\xb1H\x0c\x9a\xdc0\x00$8\xc1\xc1\x0e\x81\xe08I\xf1\x08Jp\x80\x15\xa2\x188\x0c\x16\x90\x82\xb4(\xa3\xd6\x06\xf9C\x19\xd45\x82\x11\xdc\xf9\t\xa4\xa0\x85\x1b\x82\xc1\x81\x18PB\x12\x06V\x8c7R\xc0\x82\t\xc4`\t^\x17\xc5\''8q\x8b\xa2w\x80l\xd38\x87D6Q\xe6(\xa4\x80\x03\x1c\x18\x00\x10\xa6\x91\x02IL@\x12\xc9\xe8O\x82\x89!\x81\xb0L\x80\x02\x14@\x82\x0e&@\x892\xc0:\x16\\\xd1\xc4-\xa6\x91\x16D\x9d\xdd\x01\x98\x177a&x\nD\xf4\xc2\x13\x0e \xdb\x01\x1eq\x80\x0fH \x18\xbaH\x04\x1e(h\x90\x80\x00\x00;''') ,'frame_silver_small.gif'
     ,'B181EC1F-CA20-4724-B2EB-15F3E455142E' ,'2008-03-11 10:01:36');

   SET IDENTITY_INSERT [SalesLT].[Product] OFF; 
 END  

 ---   SELECT * FROM SalesLT.ProductCategory WHERE ProductCategoryID = 1 
IF EXISTS( SELECT * FROM SalesLT.ProductCategory WHERE ProductCategoryID = 1 ) 
BEGIN  

--- UPDATE [AdventureWorksLT2019].SalesLT.ProductCategory (
   UPDATE SalesLT.ProductCategory 
    SET    ParentProductCategoryID = NULL , Name = 'Bikes' , rowguid = 'CFBDA25C-DF71-47A7-B81B-64EE161AA37C' , ModifiedDate = '2002-06-01 00:00:00'
    WHERE ProductCategoryID = 1;
END  

---   SELECT * FROM SalesLT.ProductCategory WHERE ProductCategoryID = 1 
---   USE AdventureWorksLT2019; 
IF NOT EXISTS( SELECT * FROM SalesLT.ProductCategory WHERE ProductCategoryID = 1)   
 BEGIN  
   SET IDENTITY_INSERT SalesLT.ProductCategory ON; 
--- INSERT INTO   [AdventureWorksLT2019].SalesLT.ProductCategory (
    INSERT INTO   SalesLT.ProductCategory 
      ( [ProductCategoryID]  ,[ParentProductCategoryID]  ,[Name]  ,[rowguid]  ,[ModifiedDate] 
    )
    VALUES 
      (1 ,NULL ,'Bikes' ,'CFBDA25C-DF71-47A7-B81B-64EE161AA37C' ,'2002-06-01 00:00:00'
    );

   SET IDENTITY_INSERT SalesLT.ProductCategory OFF; 
 END  

 ---   SELECT * FROM SalesLT.ProductCategory WHERE ProductCategoryID = 6 
IF EXISTS( SELECT * FROM SalesLT.ProductCategory WHERE ProductCategoryID = 6 ) 
BEGIN  

--- UPDATE [AdventureWorksLT2019].SalesLT.ProductCategory (
   UPDATE SalesLT.ProductCategory 
    SET    ParentProductCategoryID = 1 , Name = 'Road Bikes' , rowguid = '000310C0-BCC8-42C4-B0C3-45AE611AF06B' , ModifiedDate = '2002-06-01 00:00:00'
    WHERE ProductCategoryID = 6;
END  

---   SELECT * FROM SalesLT.ProductCategory WHERE ProductCategoryID = 6 
---   USE AdventureWorksLT2019; 
IF NOT EXISTS( SELECT * FROM SalesLT.ProductCategory WHERE ProductCategoryID = 6)   
 BEGIN  
   SET IDENTITY_INSERT SalesLT.ProductCategory ON; 
--- INSERT INTO   [AdventureWorksLT2019].SalesLT.ProductCategory (
    INSERT INTO   SalesLT.ProductCategory 
      ( [ProductCategoryID]  ,[ParentProductCategoryID]  ,[Name]  ,[rowguid]  ,[ModifiedDate] 
    )
    VALUES 
      (6 ,1 ,'Road Bikes' ,'000310C0-BCC8-42C4-B0C3-45AE611AF06B' ,'2002-06-01 00:00:00'
    );

   SET IDENTITY_INSERT SalesLT.ProductCategory OFF; 
 END  

 ---   SELECT * FROM SalesLT.ProductModel WHERE ProductModelID = 30 
IF EXISTS( SELECT * FROM SalesLT.ProductModel WHERE ProductModelID = 30 ) 
BEGIN  

--- UPDATE [AdventureWorksLT2019].SalesLT.ProductModel (
   UPDATE SalesLT.ProductModel 
    SET    Name = 'Road-650' , CatalogDescription = NULL , rowguid = '42E1C597-6DD9-4071-B1A5-1DC5CDCBDBCA' , ModifiedDate = '2005-06-01 00:00:00'
    WHERE ProductModelID = 30;
END  

---   SELECT * FROM SalesLT.ProductModel WHERE ProductModelID = 30 
---   USE AdventureWorksLT2019; 
IF NOT EXISTS( SELECT * FROM SalesLT.ProductModel WHERE ProductModelID = 30)   
 BEGIN  
   SET IDENTITY_INSERT SalesLT.ProductModel ON; 
--- INSERT INTO   [AdventureWorksLT2019].SalesLT.ProductModel (
    INSERT INTO   SalesLT.ProductModel 
      ( [ProductModelID]  ,[Name]  ,[CatalogDescription]  ,[rowguid]  ,[ModifiedDate] 
    )
    VALUES 
      (30 ,'Road-650' ,NULL ,'42E1C597-6DD9-4071-B1A5-1DC5CDCBDBCA' ,'2005-06-01 00:00:00'
    );

   SET IDENTITY_INSERT SalesLT.ProductModel OFF; 
 END  

 ---   SELECT * FROM [SalesLT].[Product] WHERE ProductID = 761 
IF EXISTS( SELECT * FROM [SalesLT].[Product] WHERE ProductID = 761 ) 
BEGIN  

--- UPDATE [AdventureWorksLT2019].[SalesLT].[Product] (
   UPDATE [SalesLT].[Product] 
    SET    Name = 'Road-650 Red, 62' , ProductNumber = 'BK-R50R-62' , Color = 'Red' , StandardCost = 486.7066 , ListPrice = 782.9900
     , Size = '62' , Weight = 9071.80 , ProductCategoryID = 6 , ProductModelID = 30 , SellStartDate = '2005-07-01 00:00:00'
     , SellEndDate = '2007-06-30 00:00:00' , DiscontinuedDate = NULL , ThumbNailPhoto = CONVERT(varbinary, 'b''GIF89aP\x001\x00\xf7\x00\x00\x92\x04\x07\xc6\xbc\xc394:XTY\xd0\x16-\xf9\xf9\xfd\xf9\xf9\xf9\xdc\xdb\xdb\xdb\xe4\xe8\xa9.7\xf9x\x88[!)\xd3\xca\xce\xc4\xc1\xc5\xf9\xeb\xec\x87joHCI\xa8EM\xf4\xf4\xfa\xed\xed\xf5\xf1\xf1\xf1\xe3\xe3\xe4\xee\xed\xf8\xc6jvf]d\x83}\x83\xf0\xee\xf4\xe0\xde\xe4\xbd\xc5\xce\xe7\x00\x0fp\x85\x9f\xe9\xf3\xf6\xa09F\xd4\xd2\xd4\xf5\xf5\xfc\xcc\xc9\xd5\xcd5O*$*\xb2\xad\xb2\xfe\xf3\xf6\xee\xed\xedC=C\xc1$2\xb5\xb1\xb2\xb8\xb6\xc1\xd3\xd2\xdb\xcd\xca\xcb\xfe\xfe\xfe\xbd\xbb\xbd\xb1\xaa\xad\xe3\xe1\xf4\x92\x8e\x91\x92\x91\x93\xa5\xa2\xa5\xfd\xdc\xde\xcc\xcf\xd9\xe8\xca\xca\xf7\xf7\xfc\xf3\xfb\xfe\xc6\x9a\xaekel\xfd\x88\x92\xe9\xe7\xe8\x9d\x9a\x9d\xd0\xce\xd2\xba\xb3\xb5\xdc\xda\xed\xc8\x00\x05\xcav\x83\xdf\xdd\xde\xf1\xf1\xf6\xc9\xc5\xcbllw\xdd\xdc\xe0}uz\xfbgy\xf8+F\xb7\x00\x16\xa6\x01\x15\xf0\xef\xef\xa5\x1e$\xfd\xa2\xa9\xb0bg\x8b\x89\x8c\xf9\xfe\xfe\xd4\x8a\x8bqmr\xfb\xfc\xfe\x7f|\x80\x9a\x94\x99\xa9\xa4\xad\xfc\xfc\xfc\xe4\xe3\xea\xf3\xf2\xfa\xac\xaa\xac\xf0\xf0\xf8\xa8\x9b\x9c\xac\xb2\xb5\xda\xa9\xa9\xab\xa8\xb1\x88\x84\x8a\xfaVi\x8a\x8b\x92\xc1LW\xee\xee\xf1\xe9\xe9\xea\xe4\x00$\xe2\xe0\xdd\xb9\x8e\x92\xc6\xc5\xc5\xd8So\xfd\xc8\xc9\xe9\xe8\xee[YcTNStrt\xcb\x83\x86=9?\xa9V^\x89LV\xf2\xf1\xfd\xc2\x01\x13\xf7\xf6\xf7\xe8\xe4\xe1\xf5\xf4\xf5\xe8\xe6\xf3\xfb\x98\xa2\xed\xeb\xf2\xfd\xb6\xb9\xc5\xc3\xcc\xfc\xfb\xfc\xcb\xa1\xa6\x82\x80\x86\xab\x8e\x98\xeb\xea\xf2mik\xbb\x00\x05\xda\xd7\xderjo\xf3\xf2\xf3\xd1\x03\x15\xbc\x80\x8c\xb5\xb3\xb9\x8a\x16(\xbd\xb5\xbc\xde\xb5\xb4ns{\xe7Ea\xed\xea\xed\x88\x83\x85tt~\xe0\xba\xba\xde\xd9\xd6\xf6\xf4\xf5\xf4\xf3\xf9\x8f\x95\x98\xeb\xd4\xd3\xed\x146\xea\xe8\xf6\xe4\xd2\xd1\xc2\xbe\xc1\xf8\xf1\xf0\xf5\xf9\xf7c_d\xfd\xa9\xb3\xa6\xa6\xa8,2@\x9e\x9e\xa0\xd6\x00\t2.2\xfd\xff\xfe\x90\x8d\x8e\xf8\xf7\xf7\xf7\xf6\xf4\xf6\xf4\xf8\xf0\xef\xfb|y}\xfb\xfa\xfa\xf2\xf2\xf7\xec\xea\xf5\xeb\xea\xeb\xd5\xd2\xe1\xd7\xd5\xd7gcg~\x80\x8b\xff\xfe\xfd\xfc\xfc\xfa\xe1\xe9\xe9\xd8\xd9\xd9\xf2\xf0\xf9$ $\xa4\x00\x03\xa3\x9d\xa2\xed\xec\xeb\x97\x94\x97hbk\xf2\xf1\xfa\xfd\xfd\xfdOKP\xf4\xf3\xfd.)-\xf6\x197\xda\xd7\xe6\xbd\x14"\xf5\xf5\xf5\xef\x08+!\x1c\x1f\xd6\xd0\xc8\x9f\xa0\xaa\xb7\xb7\xb7\xf3\xf6\xf8ysx\xef\xdc\xdc\xda\x9d\xa2\xc5\x8b\x8e\xce\x95\x96\xc3;=\xe2Mx\xe2Zf\xde\xc0\xc1\xfe\xd3\xdfhij`Y_MTW3Ib\xf6\xf5\xf5\xf0\xf2\xfa\xe1\x007PEM\xa0}\x88\xbf\xc0\xc4\xee\xae\xb4\x9b\xa9\xc1\x86\x9d\xc5\x9f\x11\x15\xac\xa8\xa7\xf1P{\xad\xa2\xa8\xd4\xe1\xe7\xfa>W\xeb\xec\xef\xf9\''?\xe3\xd7\xda\xf9\xfb\xfb\xdd\x1eH\xdf\xde\xed\xf4\xf3\xf2\x7f8G\xcd\x0c\x1e\x97\x90\x96\x96\x99\x9d\xc0\xd3\xe0\xfd\xfd\xff\x99\x99\x99\xf1\xf1\xf8\xff\xff\xff!\xf9\x04\x00\x00\x00\x00\x00,\x00\x00\x00\x00P\x001\x00\x00\x08\xff\x00\xff\t\x1cH\xb0\xa0\xc1\x83\x08\x13*\\\xc8\xb0\xa1\xc3\x87\x10#J\\\xc8\xec\xc9\xc4\x8b\x18%z\xc1\xc2\''\xa3\xc0-\x05\xaf\x88\xbb\xa1\xaf\x98G\x89E\x06\xf0X\xe4\xb1\x01\x16,fh\x9cB\x97\xce\x03\xb8S\''#n\xa1Q\x02\xc3\x9cS&/\x1aH\xd2\xc6\x9c$\x01\xa6\x92\xe2\xcc\t1\x96\x0b\x08)\x0e\xd5\xb0\x97\xd3E\nE&V0\x9d8#j>\x13\xabV\xb1\xc4\x08jE\xc7\xad\x13\xed\xf12\x00\x04\x96\x00\x08\xb40\xb2\n\xb2\x06\xed\xc9\x15\x02\xc2d\xacPj\xac\xdd\x89F8\xa8Xv\xee\x04\xc6h5\xfebtW\xa8\x83\xe3de\xa2\xd8\x88Xl\x14\x0c\xc5\x13\xe7\xed;\xd3\x01D\x82&C:4{\xd7\xe3M\xac\x86\xbbx\x04\xc3,q\x02\x0b\x02\x88\xb4\xb5\xfad-\x82\x13D\xa8\xd40Y\x02\xc8AB\x07R\xda\x89b\x1d\xd1]#TN\xd4\x94\x19\xb8g\x90\x1d(\x88BC\xf63\xb9  T\x8d\x88C\xbc\xb2\x8f\x04"\x00\xc9\x97\xe4\xff"\x18\xea\xd2\x85\xcf\xa1G+xc\xf8\x9f\x02F8\xb4?\xfc`\x82\xd1/(P\x00\xa8YrP\x10\x0e:P\xfc\x92\x07#j\xc4\xb3\x04)L\xa80\x9c|\r\xb9s\xc1w8P\x03Er\n\xa8\x82\x105\xd8 \x92G\x13\xa0\xa9\xa1\xc6\x05\x0c\x1aDA\x11.\xb4\x01\xc4\x01\xb4\x18 \xd8/b\x08\xc4\x89:\xc9\xf5\x90P1U\xe0\xa3\x86\x1b\x17\x10\xc0H$\x07Q\xe0B\r\xab\x901\x850+\xd4\xe5\xd1\x130\xcc0\xc7(q\x0c\x10G\x1c\xa3\x98\xb1\xc3\x10U\x10\x84\x03\x8cj\xf8a\x90*/\x08\xf4\t6\xa8,1\xc92\xa1\x14dK>\xde\xa4 @\x1dl\xa6\x92J\x1d\xb7\xac`\xc0D\xb1\x942\n9u\x0c0\x0c\x12\x96X2\xcc\x00\x1e\xb8\xf1\xc8&q\rterQ(DE\x15C\xa8A\xc2\x07\x03\xd12\x039n\x0e`\x05\x19B\x122\xcd\x00\xc8\xf82@\x1b\x02\x05\xc5\xd0\x06V\xb0\xe9\xcd\x14^\xc0\xd0@ \r8r\x8a\x16\x04,\xffP\x07\x06\rX\tc3\xa4,T\rn$\x84\xf0O\x08\xb7\xa4\x82\x8c\x1c4DSD\x12E\x1c\xb0\x06&AT\x02\x81/\xc8\xf4\xf3\xcf\x16\xa2&\x14\x82\x1c\x02\xc8\x91\xcf\x11\x15\xd0\x12\x8b\x1e\x16t\xa1"\x11\xeaH2@\n\xe4\x04A\xd06\xb7\x02\xa2\x90\x02MH\xc1\x08>\x8d|\xf3&\x16\xa0,bQ\x0e\xff\xe4P@E\x07\xc4\xc0\x032\xce\x90\xf1\xcf<]&T\x841\x02`\x10\xc4\x069\x1cc\x80\x1e\x1aX \x01+\x1c\x90`\x07\x02+\xdc\x82.(\x04]\x02^\''o \x94K<*\xa8\xc2\x89\n\xa8<\x02\xc1&>\xf0#B+\xac\x88\xf0\xcf\x04\xac<1\x0f\n\x14\x802M*\xceH\x0b\x12B\xcc\xdc"\xc00\x01\xf8\xe0\xca?]\x18\xd1\x8a,\xafH J\x00\xcb\x04\xf0\x8f,m\xcc\x91\x82\x1c\x07\x10\x14\xc9\xc8%\x1bdC\x07D\xfc#\xcd\x00\x0b\x0cA\xc0\x0e\x90\x12\xe3\xb4&\xfc\xe0\xfc\x04\n\xcc\\!A\x1bV\xa4R\x82\x0b\xff$\xfflP?\xa9\x0c\x00\xc9\x06\xff\xc4\xb2H1\x16,"\x01\x1e\x12\xe8PE\x02T\x10#A1\r\x0c#\x80"\x82\x10$\xc6\xc8\x93(@\n7\x86\xa9\xe2\x07*\xdb\xfc3C\t\x02(\x81\xcd\x10\x17$\xa1\xca+\x8b\xf8S\x80\x06\xcc\xf8\xf0D\x01_\xfcsE\x0c\xde\x940\x80\x1e\x08U\x00A\x1dYlp\x85\x05/\x18\x90I\x0e\x86\x18q\x8c\x1e\x1f`\xc3\x86\x0e\x120\r\x87\t\x0c_\xa69x\xe34! \x01\x9d\x93\xa0B(\xbb\xd4\x81\x8c7\xbb\xccC\x84\xda\x83\xb8\xb3\x81,\xff\x14\x10L\x05"\x88\xa3J\x0e\x16\xf01\xc3\xb3z\x1d\xf4C*<8\x02\x1f\x8a\x81\xbf\xe4\xe9a\x16}\x10\x81\x0e\xb6\x01\x85\x16\\\xe1\x1f\xb3\xf8\xc3?\x92@\x08\x01\xf0`h\x03\xd9\\\x13\xe8\xd1\x08)$@\x1d\xbfhB\x1e\xe8A\x82G,\xa0\x10\xc7\xa0\x82*\x18\x80\rF\x10\xe1\x06\xe68\x82-\x8a\x00\x87.\xa8\xa2\x00\x13\x10\x04+\x1ap\x8b\x12x\xa3Z\x021\xc0\x00\xff\x04\x90\x8f\n\xbc \x1c\xb1\xc8\xc1+\xfea\x00Z\xc8 \x07\x1f\xb8@\x04 \xd5\x074\x08\xc2\x02\x1a\x80\x811R\x90\x08\x83T\x03\x00y`\x87@\x16\xc1\x06\x00H!\x02\x00\xe0\x10>H\xe0\x06?p\xa3\x0ft\xc0G\x19\xca1\n9\x98\xc3f9\x98E\xce\x98\xc1\x0c2\x98\xafk\x05I\x82\x00\xc8\x01\x89Ed"\x13\x8b\xb0G\x17\x88\xf1\x0f\x14\xb4\xa0\x16\xa0P\xc1\x03\x1a`\x014H\xc0\x029\xd8\x82-\xac \x80v\x1c\xe4\x1ai\xcc\x86\x06*\x00\x86\x07T\xc0\x1djz@#\xec\xf0\xc1&\x80O\x05C\xc0\x079\x04\xe0\x05\xdd\xcd\x82\x12\\\xf8\xc3\x17\xfc1\x06r8#\x1a\x06\x81\x012\x86\xe1\x82b\x14C\x10\xdf\xa2\xc0\x1ff\xb1\x86Dp\xc0\x83\x96\xc8@\x12&\xf0\x87p\x84\x83\x15iX\x85\x002\x80\x10k\x00\xe0\x1e\x96\xc0\x82"$a\x82\x18\xd4\xc1\x18\xa7\xd8E\x05x\xd1\x80v\x94\xc3\x0e \x80\x02\x08\x1e\xf1\x80R\xb4\xe1\x06\\\x80\x83,\xf4p\xff\x1a\x17\x0c\xc0\x17?0H)J0\r t\xe1\x0b\x13\xb0\x80\x05&\x00\x87Z\x00\x81\x05\x92\x80\xc2\x1dR\x80\x81z\xf4\xa2\x0b"\xf0\x17\x1ajP\x07E$\xa4\x10O\xc2\x02\x18j@\x082\x94 \x050h\x05\x1f\xf50\x0f*\x88"\x0c3\xb8\x877\xee`\x8eh\x00\x01\x08_\xf8B\x17\xba\xe0\x0f \x8c\xa2\x04X0\xc8)\x90\x01\x0b[\x10\x84\x1fH\xdd@-`\x01\x81{(\x02\x03\xbe\x12D\x01\n\xe0/x\x94\xa2\x0e\xc3\x18\x8fA\x04A\x83,(\x01\x03\x18P\x820F\x81\x0c\x08\x00\xc1 \xc5`A\x18\xb2p\x87{h\xc1Wi0\x92@\x0e\xf0S+\x08\x14\x19J\x18A\x17\x8e!\x02\tH\x80\x18\xaf\x10\x82\x10\xa6\x80\xd5\x06@B\x10WH,b\xaf@\x81\xab\xf2\xc0o\x04AA\x06\xf2\x01\x0b\x0c\x9c*\x1f\x03(\x811\x8e`\x04b\xecT\x04\x13\xa8\x87#XP\x8aU(b\x0c\x81\x98E\x17\x12\xd1\xd7.H\xc0\xa7\xbe\x98C0S\xa1\x08\x06\xff\xfc\xe3\x989\xf8B\x1fd\xd0\x07e\x8c@\x0b\x81H\x842\x84\xe0\t<\x88\xe0\xb8\x9a\xe0\xc2\x0fR\x87\x90p\xd0`\x15\x96\xc0E\x1cVP\x03\x1e\xa4\x02\x02\xa0\xda\xc2\xc4(\xb1\x81z\xb4\xc0\x11&\x80\xc1)\xcc\x01\x07!l@\xaf"(\xc0\x0b\x1a0\x00g\xd0\xc0 \xbc\x10\x807\x020\x81\x83\xf6a\x16\n\xfdG\x1fFp\xde\n\xfc\xc3\x02\x86\xd0\x0012\xca\x8f"`\x81\x88\t1\xc14\xa0\x81\x0bET\x02_lr\x04\xcf\x9e\xc0\x05C|\xe1\x18\x94\xa8\x04\rjP\t\x13\xd8\xe3\x0f@\xd8\x00\x1c&0\x81/\x9c\x82\x1c\xbe\x00fA\xf4 \x87\x14\xb4\x83\x12\x05\xb0@\x01$\x90\xbb\x1c\x98\xf7\x1f2\xe0B\x97,\xe0\x8aL\xb8\xa2\x00\xc4h\xc0(\xea\x002\x84\x18\xe0\x07\xb8\xb0\xc24\xcc\xe0\xab\xcc\xd2\xe0v\x13\xc8\xc1"\xff\x01\x84[\x80\x82\x02@\xc8\x82#\xd6\x00\x87\x1c\x18\x80\x02\xba\xa0\x04\x16\xea \x00\xff\x1ad\x15\xa9\xc8\xc0\x08DP\x8c]\xfe\xe3\xff\x92\xf50\xc4\x7f\xb9\x90\x89-\xbc@\xc6z0@\x1aj\xb05\n(\x84\x17H\x10\x86\tla\x8fp\xe4\xc3w#\xd0\xc4?^\x91;V\xac`\x15\xa7\xf9\x82!^\xc1/\x8cnA\x0f\xa0\x18\x98]\x0fr\x80\xad\x99\xc0\x07\xc7P\xb48z\x81\x06O\x18\xe1\x1f\xfe0D/\xc2Q\x0c~X\xe0\n\x06\xc0\x9b\x00f\xb0\x90R\x10\xa2K\x06x\x02-\x80\xe0\r9\xfc\xa0\x02}\x80\xc3\x16\x9e\x10\x8cQ(\x82*\x08\xd5\x80\x06\x14M\x8c\x02P\xc2\x0c\x10@\x06\xa8\x10R\x89\xd4\x05@\x03\xff\xf5\x07+\xb8\xa0\x89\xdc}\x81\x02\x9e\x10\x04\x1f^p\x05<\xd8"\x0b)0\x86\x0f\x14b\x0f$\xd4\xb2 d@\x861`\xb0\x81``\xa2\x08\x988\x84\x15x\xf1\x0f\r\x88\x00\x0eWT\xb4\x06\xc60\xb0C\x00\x91 ihq>\x18\xf0\x07\t\xe8"\x18\xfe\xc8-\xd3Xa\x04<\x14\x83%\xb6\xd0\x82\x1c\xea\xf0n\x84<a\x1dVX\x01+\nB\x0br\x94\xe0\x10!\xff\xa0\x053\xb6@\x8b`\xb0\xc2\xcf\x13(\x80?(\xf0\x82.\xa0\x01\x14\x15\xacC\x11\x16\xd2\x06te\xe1\x08(@\x83\x01\xbe s\xa6\xc5\xa2\x15"\xe0G8\\\xe0\x05ol\xf3\xe0\x04a\x86\x0b6`\x8b\x83\x1fA\x00\xc8\xb0\x02\xd0\x9f\x90\xeb\x17\xb0d\x02W\xf8\xc2\xc4|\xc0\x82)\xa4\x00\x19*^H4R\x00\x012\x04\xa0\x08\xad\xc8\x9d\xcd\xf0\xf0\x8fp\x18 \x11\r\xc8\xc2\x10\xe7\xc0\x0c\x8fDC\x00\xbe3A\x08\x9e`\x91\x8e\xf8\xe3f\x0e`\x80#2P\x87T\x94\xe2!\xe60\x06V\x81\xe1\x02y\xf8\x00\x1e\x06@\xc3\x13B\xd0\x00-\xccax\x95\xe8\xfbI\x1a\xf0,\x01L#\x06\xcf\xd8\xc3\x1a\xf6\xd0\x02L0 \x083\xc8l\x1d\xd2\xee\x905\xc0\xa2\x0e)\x18E\x06~\x10\x03H\xac\x00\x18d\xe0\x01\x04\xb2\xe5\x08\xb4T\xe0g\xceH\x851\xacP\tL)a\x14\x10(\x012\x0e\xb1\xf3\x89\xb4\x81\xa9k\x82\x80\xf6\xd5\x94\xa7\x1f\x14\xca.m\x89\xb6A/|Q\x82\xf1\xfb\xa2\x0es\xe0[\xdf"\xf2\x82.m\x81\x17^\xc8@7n\xd1\x8d9\xac\x02\x14\xabY?Z,\xf4\x0fZ\x80\xa2\x1fS\x10\x80\xab\xe0\x05\xbc\xa0\x07\xac\xc0\n\xb1`g!\xb2\x80\x0c\xd8\x80\t\x11\x10\x00;''') , ThumbnailPhotoFileName = 'superlight_red_small.gif' , rowguid = '1DA14E09-6D71-4E2A-9EE9-1BDFDFD8A109'
     , ModifiedDate = '2008-03-11 10:01:36'
    WHERE ProductID = 761;
END  

---   SELECT * FROM [SalesLT].[Product] WHERE ProductID = 761 
---   USE AdventureWorksLT2019; 
IF NOT EXISTS( SELECT * FROM [SalesLT].[Product] WHERE ProductID = 761)   
 BEGIN  
   SET IDENTITY_INSERT [SalesLT].[Product] ON; 
--- INSERT INTO   [AdventureWorksLT2019].[SalesLT].[Product] (
    INSERT INTO   [SalesLT].[Product] 
      ( [ProductID]  ,[Name]  ,[ProductNumber]  ,[Color]  ,[StandardCost] 
     ,[ListPrice]  ,[Size]  ,[Weight]  ,[ProductCategoryID]  ,[ProductModelID] 
     ,[SellStartDate]  ,[SellEndDate]  ,[DiscontinuedDate]  ,[ThumbNailPhoto]  ,[ThumbnailPhotoFileName] 
     ,[rowguid]  ,[ModifiedDate] )
    VALUES 
      (761 ,'Road-650 Red, 62' ,'BK-R50R-62' ,'Red' ,486.7066
     ,782.9900 ,'62' ,9071.80 ,6 ,30
     ,'2005-07-01 00:00:00' ,'2007-06-30 00:00:00' ,NULL ,CONVERT(varbinary, 'b''GIF89aP\x001\x00\xf7\x00\x00\x92\x04\x07\xc6\xbc\xc394:XTY\xd0\x16-\xf9\xf9\xfd\xf9\xf9\xf9\xdc\xdb\xdb\xdb\xe4\xe8\xa9.7\xf9x\x88[!)\xd3\xca\xce\xc4\xc1\xc5\xf9\xeb\xec\x87joHCI\xa8EM\xf4\xf4\xfa\xed\xed\xf5\xf1\xf1\xf1\xe3\xe3\xe4\xee\xed\xf8\xc6jvf]d\x83}\x83\xf0\xee\xf4\xe0\xde\xe4\xbd\xc5\xce\xe7\x00\x0fp\x85\x9f\xe9\xf3\xf6\xa09F\xd4\xd2\xd4\xf5\xf5\xfc\xcc\xc9\xd5\xcd5O*$*\xb2\xad\xb2\xfe\xf3\xf6\xee\xed\xedC=C\xc1$2\xb5\xb1\xb2\xb8\xb6\xc1\xd3\xd2\xdb\xcd\xca\xcb\xfe\xfe\xfe\xbd\xbb\xbd\xb1\xaa\xad\xe3\xe1\xf4\x92\x8e\x91\x92\x91\x93\xa5\xa2\xa5\xfd\xdc\xde\xcc\xcf\xd9\xe8\xca\xca\xf7\xf7\xfc\xf3\xfb\xfe\xc6\x9a\xaekel\xfd\x88\x92\xe9\xe7\xe8\x9d\x9a\x9d\xd0\xce\xd2\xba\xb3\xb5\xdc\xda\xed\xc8\x00\x05\xcav\x83\xdf\xdd\xde\xf1\xf1\xf6\xc9\xc5\xcbllw\xdd\xdc\xe0}uz\xfbgy\xf8+F\xb7\x00\x16\xa6\x01\x15\xf0\xef\xef\xa5\x1e$\xfd\xa2\xa9\xb0bg\x8b\x89\x8c\xf9\xfe\xfe\xd4\x8a\x8bqmr\xfb\xfc\xfe\x7f|\x80\x9a\x94\x99\xa9\xa4\xad\xfc\xfc\xfc\xe4\xe3\xea\xf3\xf2\xfa\xac\xaa\xac\xf0\xf0\xf8\xa8\x9b\x9c\xac\xb2\xb5\xda\xa9\xa9\xab\xa8\xb1\x88\x84\x8a\xfaVi\x8a\x8b\x92\xc1LW\xee\xee\xf1\xe9\xe9\xea\xe4\x00$\xe2\xe0\xdd\xb9\x8e\x92\xc6\xc5\xc5\xd8So\xfd\xc8\xc9\xe9\xe8\xee[YcTNStrt\xcb\x83\x86=9?\xa9V^\x89LV\xf2\xf1\xfd\xc2\x01\x13\xf7\xf6\xf7\xe8\xe4\xe1\xf5\xf4\xf5\xe8\xe6\xf3\xfb\x98\xa2\xed\xeb\xf2\xfd\xb6\xb9\xc5\xc3\xcc\xfc\xfb\xfc\xcb\xa1\xa6\x82\x80\x86\xab\x8e\x98\xeb\xea\xf2mik\xbb\x00\x05\xda\xd7\xderjo\xf3\xf2\xf3\xd1\x03\x15\xbc\x80\x8c\xb5\xb3\xb9\x8a\x16(\xbd\xb5\xbc\xde\xb5\xb4ns{\xe7Ea\xed\xea\xed\x88\x83\x85tt~\xe0\xba\xba\xde\xd9\xd6\xf6\xf4\xf5\xf4\xf3\xf9\x8f\x95\x98\xeb\xd4\xd3\xed\x146\xea\xe8\xf6\xe4\xd2\xd1\xc2\xbe\xc1\xf8\xf1\xf0\xf5\xf9\xf7c_d\xfd\xa9\xb3\xa6\xa6\xa8,2@\x9e\x9e\xa0\xd6\x00\t2.2\xfd\xff\xfe\x90\x8d\x8e\xf8\xf7\xf7\xf7\xf6\xf4\xf6\xf4\xf8\xf0\xef\xfb|y}\xfb\xfa\xfa\xf2\xf2\xf7\xec\xea\xf5\xeb\xea\xeb\xd5\xd2\xe1\xd7\xd5\xd7gcg~\x80\x8b\xff\xfe\xfd\xfc\xfc\xfa\xe1\xe9\xe9\xd8\xd9\xd9\xf2\xf0\xf9$ $\xa4\x00\x03\xa3\x9d\xa2\xed\xec\xeb\x97\x94\x97hbk\xf2\xf1\xfa\xfd\xfd\xfdOKP\xf4\xf3\xfd.)-\xf6\x197\xda\xd7\xe6\xbd\x14"\xf5\xf5\xf5\xef\x08+!\x1c\x1f\xd6\xd0\xc8\x9f\xa0\xaa\xb7\xb7\xb7\xf3\xf6\xf8ysx\xef\xdc\xdc\xda\x9d\xa2\xc5\x8b\x8e\xce\x95\x96\xc3;=\xe2Mx\xe2Zf\xde\xc0\xc1\xfe\xd3\xdfhij`Y_MTW3Ib\xf6\xf5\xf5\xf0\xf2\xfa\xe1\x007PEM\xa0}\x88\xbf\xc0\xc4\xee\xae\xb4\x9b\xa9\xc1\x86\x9d\xc5\x9f\x11\x15\xac\xa8\xa7\xf1P{\xad\xa2\xa8\xd4\xe1\xe7\xfa>W\xeb\xec\xef\xf9\''?\xe3\xd7\xda\xf9\xfb\xfb\xdd\x1eH\xdf\xde\xed\xf4\xf3\xf2\x7f8G\xcd\x0c\x1e\x97\x90\x96\x96\x99\x9d\xc0\xd3\xe0\xfd\xfd\xff\x99\x99\x99\xf1\xf1\xf8\xff\xff\xff!\xf9\x04\x00\x00\x00\x00\x00,\x00\x00\x00\x00P\x001\x00\x00\x08\xff\x00\xff\t\x1cH\xb0\xa0\xc1\x83\x08\x13*\\\xc8\xb0\xa1\xc3\x87\x10#J\\\xc8\xec\xc9\xc4\x8b\x18%z\xc1\xc2\''\xa3\xc0-\x05\xaf\x88\xbb\xa1\xaf\x98G\x89E\x06\xf0X\xe4\xb1\x01\x16,fh\x9cB\x97\xce\x03\xb8S\''#n\xa1Q\x02\xc3\x9cS&/\x1aH\xd2\xc6\x9c$\x01\xa6\x92\xe2\xcc\t1\x96\x0b\x08)\x0e\xd5\xb0\x97\xd3E\nE&V0\x9d8#j>\x13\xabV\xb1\xc4\x08jE\xc7\xad\x13\xed\xf12\x00\x04\x96\x00\x08\xb40\xb2\n\xb2\x06\xed\xc9\x15\x02\xc2d\xacPj\xac\xdd\x89F8\xa8Xv\xee\x04\xc6h5\xfebtW\xa8\x83\xe3de\xa2\xd8\x88Xl\x14\x0c\xc5\x13\xe7\xed;\xd3\x01D\x82&C:4{\xd7\xe3M\xac\x86\xbbx\x04\xc3,q\x02\x0b\x02\x88\xb4\xb5\xfad-\x82\x13D\xa8\xd40Y\x02\xc8AB\x07R\xda\x89b\x1d\xd1]#TN\xd4\x94\x19\xb8g\x90\x1d(\x88BC\xf63\xb9  T\x8d\x88C\xbc\xb2\x8f\x04"\x00\xc9\x97\xe4\xff"\x18\xea\xd2\x85\xcf\xa1G+xc\xf8\x9f\x02F8\xb4?\xfc`\x82\xd1/(P\x00\xa8YrP\x10\x0e:P\xfc\x92\x07#j\xc4\xb3\x04)L\xa80\x9c|\r\xb9s\xc1w8P\x03Er\n\xa8\x82\x105\xd8 \x92G\x13\xa0\xa9\xa1\xc6\x05\x0c\x1aDA\x11.\xb4\x01\xc4\x01\xb4\x18 \xd8/b\x08\xc4\x89:\xc9\xf5\x90P1U\xe0\xa3\x86\x1b\x17\x10\xc0H$\x07Q\xe0B\r\xab\x901\x850+\xd4\xe5\xd1\x130\xcc0\xc7(q\x0c\x10G\x1c\xa3\x98\xb1\xc3\x10U\x10\x84\x03\x8cj\xf8a\x90*/\x08\xf4\t6\xa8,1\xc92\xa1\x14dK>\xde\xa4 @\x1dl\xa6\x92J\x1d\xb7\xac`\xc0D\xb1\x942\n9u\x0c0\x0c\x12\x96X2\xcc\x00\x1e\xb8\xf1\xc8&q\rterQ(DE\x15C\xa8A\xc2\x07\x03\xd12\x039n\x0e`\x05\x19B\x122\xcd\x00\xc8\xf82@\x1b\x02\x05\xc5\xd0\x06V\xb0\xe9\xcd\x14^\xc0\xd0@ \r8r\x8a\x16\x04,\xffP\x07\x06\rX\tc3\xa4,T\rn$\x84\xf0O\x08\xb7\xa4\x82\x8c\x1c4DSD\x12E\x1c\xb0\x06&AT\x02\x81/\xc8\xf4\xf3\xcf\x16\xa2&\x14\x82\x1c\x02\xc8\x91\xcf\x11\x15\xd0\x12\x8b\x1e\x16t\xa1"\x11\xeaH2@\n\xe4\x04A\xd06\xb7\x02\xa2\x90\x02MH\xc1\x08>\x8d|\xf3&\x16\xa0,bQ\x0e\xff\xe4P@E\x07\xc4\xc0\x032\xce\x90\xf1\xcf<]&T\x841\x02`\x10\xc4\x069\x1cc\x80\x1e\x1aX \x01+\x1c\x90`\x07\x02+\xdc\x82.(\x04]\x02^\''o \x94K<*\xa8\xc2\x89\n\xa8<\x02\xc1&>\xf0#B+\xac\x88\xf0\xcf\x04\xac<1\x0f\n\x14\x802M*\xceH\x0b\x12B\xcc\xdc"\xc00\x01\xf8\xe0\xca?]\x18\xd1\x8a,\xafH J\x00\xcb\x04\xf0\x8f,m\xcc\x91\x82\x1c\x07\x10\x14\xc9\xc8%\x1bdC\x07D\xfc#\xcd\x00\x0b\x0cA\xc0\x0e\x90\x12\xe3\xb4&\xfc\xe0\xfc\x04\n\xcc\\!A\x1bV\xa4R\x82\x0b\xff$\xfflP?\xa9\x0c\x00\xc9\x06\xff\xc4\xb2H1\x16,"\x01\x1e\x12\xe8PE\x02T\x10#A1\r\x0c#\x80"\x82\x10$\xc6\xc8\x93(@\n7\x86\xa9\xe2\x07*\xdb\xfc3C\t\x02(\x81\xcd\x10\x17$\xa1\xca+\x8b\xf8S\x80\x06\xcc\xf8\xf0D\x01_\xfcsE\x0c\xde\x940\x80\x1e\x08U\x00A\x1dYlp\x85\x05/\x18\x90I\x0e\x86\x18q\x8c\x1e\x1f`\xc3\x86\x0e\x120\r\x87\t\x0c_\xa69x\xe34! \x01\x9d\x93\xa0B(\xbb\xd4\x81\x8c7\xbb\xccC\x84\xda\x83\xb8\xb3\x81,\xff\x14\x10L\x05"\x88\xa3J\x0e\x16\xf01\xc3\xb3z\x1d\xf4C*<8\x02\x1f\x8a\x81\xbf\xe4\xe9a\x16}\x10\x81\x0e\xb6\x01\x85\x16\\\xe1\x1f\xb3\xf8\xc3?\x92@\x08\x01\xf0`h\x03\xd9\\\x13\xe8\xd1\x08)$@\x1d\xbfhB\x1e\xe8A\x82G,\xa0\x10\xc7\xa0\x82*\x18\x80\rF\x10\xe1\x06\xe68\x82-\x8a\x00\x87.\xa8\xa2\x00\x13\x10\x04+\x1ap\x8b\x12x\xa3Z\x021\xc0\x00\xff\x04\x90\x8f\n\xbc \x1c\xb1\xc8\xc1+\xfea\x00Z\xc8 \x07\x1f\xb8@\x04 \xd5\x074\x08\xc2\x02\x1a\x80\x811R\x90\x08\x83T\x03\x00y`\x87@\x16\xc1\x06\x00H!\x02\x00\xe0\x10>H\xe0\x06?p\xa3\x0ft\xc0G\x19\xca1\n9\x98\xc3f9\x98E\xce\x98\xc1\x0c2\x98\xafk\x05I\x82\x00\xc8\x01\x89Ed"\x13\x8b\xb0G\x17\x88\xf1\x0f\x14\xb4\xa0\x16\xa0P\xc1\x03\x1a`\x014H\xc0\x029\xd8\x82-\xac \x80v\x1c\xe4\x1ai\xcc\x86\x06*\x00\x86\x07T\xc0\x1djz@#\xec\xf0\xc1&\x80O\x05C\xc0\x079\x04\xe0\x05\xdd\xcd\x82\x12\\\xf8\xc3\x17\xfc1\x06r8#\x1a\x06\x81\x012\x86\xe1\x82b\x14C\x10\xdf\xa2\xc0\x1ff\xb1\x86Dp\xc0\x83\x96\xc8@\x12&\xf0\x87p\x84\x83\x15iX\x85\x002\x80\x10k\x00\xe0\x1e\x96\xc0\x82"$a\x82\x18\xd4\xc1\x18\xa7\xd8E\x05x\xd1\x80v\x94\xc3\x0e \x80\x02\x08\x1e\xf1\x80R\xb4\xe1\x06\\\x80\x83,\xf4p\xff\x1a\x17\x0c\xc0\x17?0H)J0\r t\xe1\x0b\x13\xb0\x80\x05&\x00\x87Z\x00\x81\x05\x92\x80\xc2\x1dR\x80\x81z\xf4\xa2\x0b"\xf0\x17\x1ajP\x07E$\xa4\x10O\xc2\x02\x18j@\x082\x94 \x050h\x05\x1f\xf50\x0f*\x88"\x0c3\xb8\x877\xee`\x8eh\x00\x01\x08_\xf8B\x17\xba\xe0\x0f \x8c\xa2\x04X0\xc8)\x90\x01\x0b[\x10\x84\x1fH\xdd@-`\x01\x81{(\x02\x03\xbe\x12D\x01\n\xe0/x\x94\xa2\x0e\xc3\x18\x8fA\x04A\x83,(\x01\x03\x18P\x820F\x81\x0c\x08\x00\xc1 \xc5`A\x18\xb2p\x87{h\xc1Wi0\x92@\x0e\xf0S+\x08\x14\x19J\x18A\x17\x8e!\x02\tH\x80\x18\xaf\x10\x82\x10\xa6\x80\xd5\x06@B\x10WH,b\xaf@\x81\xab\xf2\xc0o\x04AA\x06\xf2\x01\x0b\x0c\x9c*\x1f\x03(\x811\x8e`\x04b\xecT\x04\x13\xa8\x87#XP\x8aU(b\x0c\x81\x98E\x17\x12\xd1\xd7.H\xc0\xa7\xbe\x98C0S\xa1\x08\x06\xff\xfc\xe3\x989\xf8B\x1fd\xd0\x07e\x8c@\x0b\x81H\x842\x84\xe0\t<\x88\xe0\xb8\x9a\xe0\xc2\x0fR\x87\x90p\xd0`\x15\x96\xc0E\x1cVP\x03\x1e\xa4\x02\x02\xa0\xda\xc2\xc4(\xb1\x81z\xb4\xc0\x11&\x80\xc1)\xcc\x01\x07!l@\xaf"(\xc0\x0b\x1a0\x00g\xd0\xc0 \xbc\x10\x807\x020\x81\x83\xf6a\x16\n\xfdG\x1fFp\xde\n\xfc\xc3\x02\x86\xd0\x0012\xca\x8f"`\x81\x88\t1\xc14\xa0\x81\x0bET\x02_lr\x04\xcf\x9e\xc0\x05C|\xe1\x18\x94\xa8\x04\rjP\t\x13\xd8\xe3\x0f@\xd8\x00\x1c&0\x81/\x9c\x82\x1c\xbe\x00fA\xf4 \x87\x14\xb4\x83\x12\x05\xb0@\x01$\x90\xbb\x1c\x98\xf7\x1f2\xe0B\x97,\xe0\x8aL\xb8\xa2\x00\xc4h\xc0(\xea\x002\x84\x18\xe0\x07\xb8\xb0\xc24\xcc\xe0\xab\xcc\xd2\xe0v\x13\xc8\xc1"\xff\x01\x84[\x80\x82\x02@\xc8\x82#\xd6\x00\x87\x1c\x18\x80\x02\xba\xa0\x04\x16\xea \x00\xff\x1ad\x15\xa9\xc8\xc0\x08DP\x8c]\xfe\xe3\xff\x92\xf50\xc4\x7f\xb9\x90\x89-\xbc@\xc6z0@\x1aj\xb05\n(\x84\x17H\x10\x86\tla\x8fp\xe4\xc3w#\xd0\xc4?^\x91;V\xac`\x15\xa7\xf9\x82!^\xc1/\x8cnA\x0f\xa0\x18\x98]\x0fr\x80\xad\x99\xc0\x07\xc7P\xb48z\x81\x06O\x18\xe1\x1f\xfe0D/\xc2Q\x0c~X\xe0\n\x06\xc0\x9b\x00f\xb0\x90R\x10\xa2K\x06x\x02-\x80\xe0\r9\xfc\xa0\x02}\x80\xc3\x16\x9e\x10\x8cQ(\x82*\x08\xd5\x80\x06\x14M\x8c\x02P\xc2\x0c\x10@\x06\xa8\x10R\x89\xd4\x05@\x03\xff\xf5\x07+\xb8\xa0\x89\xdc}\x81\x02\x9e\x10\x04\x1f^p\x05<\xd8"\x0b)0\x86\x0f\x14b\x0f$\xd4\xb2 d@\x861`\xb0\x81``\xa2\x08\x988\x84\x15x\xf1\x0f\r\x88\x00\x0eWT\xb4\x06\xc60\xb0C\x00\x91 ihq>\x18\xf0\x07\t\xe8"\x18\xfe\xc8-\xd3Xa\x04<\x14\x83%\xb6\xd0\x82\x1c\xea\xf0n\x84<a\x1dVX\x01+\nB\x0br\x94\xe0\x10!\xff\xa0\x053\xb6@\x8b`\xb0\xc2\xcf\x13(\x80?(\xf0\x82.\xa0\x01\x14\x15\xacC\x11\x16\xd2\x06te\xe1\x08(@\x83\x01\xbe s\xa6\xc5\xa2\x15"\xe0G8\\\xe0\x05ol\xf3\xe0\x04a\x86\x0b6`\x8b\x83\x1fA\x00\xc8\xb0\x02\xd0\x9f\x90\xeb\x17\xb0d\x02W\xf8\xc2\xc4|\xc0\x82)\xa4\x00\x19*^H4R\x00\x012\x04\xa0\x08\xad\xc8\x9d\xcd\xf0\xf0\x8fp\x18 \x11\r\xc8\xc2\x10\xe7\xc0\x0c\x8fDC\x00\xbe3A\x08\x9e`\x91\x8e\xf8\xe3f\x0e`\x80#2P\x87T\x94\xe2!\xe60\x06V\x81\xe1\x02y\xf8\x00\x1e\x06@\xc3\x13B\xd0\x00-\xccax\x95\xe8\xfbI\x1a\xf0,\x01L#\x06\xcf\xd8\xc3\x1a\xf6\xd0\x02L0 \x083\xc8l\x1d\xd2\xee\x905\xc0\xa2\x0e)\x18E\x06~\x10\x03H\xac\x00\x18d\xe0\x01\x04\xb2\xe5\x08\xb4T\xe0g\xceH\x851\xacP\tL)a\x14\x10(\x012\x0e\xb1\xf3\x89\xb4\x81\xa9k\x82\x80\xf6\xd5\x94\xa7\x1f\x14\xca.m\x89\xb6A/|Q\x82\xf1\xfb\xa2\x0es\xe0[\xdf"\xf2\x82.m\x81\x17^\xc8@7n\xd1\x8d9\xac\x02\x14\xabY?Z,\xf4\x0fZ\x80\xa2\x1fS\x10\x80\xab\xe0\x05\xbc\xa0\x07\xac\xc0\n\xb1`g!\xb2\x80\x0c\xd8\x80\t\x11\x10\x00;''') ,'superlight_red_small.gif'
     ,'1DA14E09-6D71-4E2A-9EE9-1BDFDFD8A109' ,'2008-03-11 10:01:36');

   SET IDENTITY_INSERT [SalesLT].[Product] OFF; 
 END  

 ---   SELECT * FROM [dbo].[TableD]  
IF EXISTS( SELECT * FROM [dbo].[TableD]  ) 
BEGIN  

--- UPDATE [testDb].[dbo].[TableD] (
   UPDATE [dbo].[TableD] 
    SET    ColumnD1 = 1 , ColumnD2 = '2001-02-03 04:05:00' , ColumnD3 = '5FEDD0FD-A626-428A-B3EE-BF25A2780003' , ColumnD4 = 1 , ColumnD5 = '2001-02-03 04:05:00+00:00'
     , ColumnD6 = NULL
    WHERE ;
   UPDATE [dbo].[TableD] 
    SET    ColumnD1 = 2 , ColumnD2 = '2001-02-04 05:06:00' , ColumnD3 = '36F016A5-3171-4D65-910B-CB80A3BF7EBB' , ColumnD4 = 1 , ColumnD5 = '2001-02-04 06:07:00+00:00'
     , ColumnD6 = NULL
    WHERE ;
   UPDATE [dbo].[TableD] 
    SET    ColumnD1 = 3 , ColumnD2 = '2001-02-06 06:07:00' , ColumnD3 = '5E38E470-0FB2-4605-A392-5CBB574A294D' , ColumnD4 = 1 , ColumnD5 = '2001-02-06 07:08:00+00:00'
     , ColumnD6 = NULL
    WHERE ;
END  

---   SELECT * FROM [dbo].[TableD]  
---   USE testDb; 
IF NOT EXISTS( SELECT * FROM [dbo].[TableD] )   
 BEGIN  
--- INSERT INTO   [testDb].[dbo].[TableD] (
    INSERT INTO   [dbo].[TableD] 
      ( [ColumnD1]  ,[ColumnD2]  ,[ColumnD3]  ,[ColumnD4]  ,[ColumnD5] 
     ,[ColumnD6] )
    VALUES 
      (1 ,'2001-02-03 04:05:00' ,'5FEDD0FD-A626-428A-B3EE-BF25A2780003' ,1 ,'2001-02-03 04:05:00+00:00'
     ,NULL), 
        (2 ,'2001-02-04 05:06:00' ,'36F016A5-3171-4D65-910B-CB80A3BF7EBB' ,1 ,'2001-02-04 06:07:00+00:00'
     ,NULL), 
        (3 ,'2001-02-06 06:07:00' ,'5E38E470-0FB2-4605-A392-5CBB574A294D' ,1 ,'2001-02-06 07:08:00+00:00'
     ,NULL);

 END  

 ---   SELECT * FROM SalesLT.ProductModel WHERE ProductModelID = 12 
IF EXISTS( SELECT * FROM SalesLT.ProductModel WHERE ProductModelID = 12 ) 
BEGIN  

--- UPDATE [AdventureWorksLT2019].SalesLT.ProductModel (
   UPDATE SalesLT.ProductModel 
    SET    Name = 'Men''s Bib-Shorts' , CatalogDescription = NULL , rowguid = '219E2F87-26A9-483B-B968-04578E943096' , ModifiedDate = '2006-06-01 00:00:00'
    WHERE ProductModelID = 12;
END  

---   SELECT * FROM SalesLT.ProductModel WHERE ProductModelID = 12 
---   USE AdventureWorksLT2019; 
IF NOT EXISTS( SELECT * FROM SalesLT.ProductModel WHERE ProductModelID = 12)   
 BEGIN  
   SET IDENTITY_INSERT SalesLT.ProductModel ON; 
--- INSERT INTO   [AdventureWorksLT2019].SalesLT.ProductModel (
    INSERT INTO   SalesLT.ProductModel 
      ( [ProductModelID]  ,[Name]  ,[CatalogDescription]  ,[rowguid]  ,[ModifiedDate] 
    )
    VALUES 
      (12 ,'Men''s Bib-Shorts' ,NULL ,'219E2F87-26A9-483B-B968-04578E943096' ,'2006-06-01 00:00:00'
    );

   SET IDENTITY_INSERT SalesLT.ProductModel OFF; 
 END  

