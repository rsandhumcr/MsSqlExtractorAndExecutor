# Ms Sql Extractor And Executor
A python utility to extract local Ms Sql data and execute database scripts

I created this utility as a developer, if I reset my developement database, I would loose existing test data and database related application settings.

The idea is to generate script with the extracted data and create you own scripts to re-create data without going through the front apps.


## Extracting data
To extract data you will need to execute the following script:
py .\extract_data.py

This script has two modes of operation, an interactive command line or process arguments passed as parameters.

## Extracting data with interactive mode

When you execute the script without parameters, it will search for a local database and ask the user to select a database you wish to extract data from. 

The next question is to ask the name of the table you wish to extract data from.

The next question request a where clause from the user, this is optional, but if you don't provide a where clause you will not be able to extract related data defined by the database relationships (this is the logic after the WHERE keyword in SQL).

The next question is dependent upon if the user has entered a WHERE condition, the user is asked if they want to extract the related data.

The final question is related to the type of script they wish to generate, insert, update or update and insert.

All outputs are placed into the file .\output\testfile.sql

## Extracting data with arguments 

py extract_data.py &lt;db name&gt; &lt;table name with schema&gt; &lt;where clause&gt; &lt;insert/update/update and insert&gt; &lt;Include related tables True/False&gt; [output file]
 
If an output file is not passed as an argument, then all outputs are placed into the file .\output\testfile.sql 

e.g

py extract_data.py AdventureWorksLT2019  SalesLT.SalesOrderHeader 'SalesOrderID = 71774' insert True
 
### Show table info

extract_data.py &lt;db name&gt; &lt;table name with schema&gt;

e.g

py extract_data.py AdventureWorksLT2019  SalesLT.SalesOrderHeader

The user is given help if you have typo in the database or table names in useful error responses.
 
## Executing scripts
py .\library_executor.py

This is an interactive executor, which will look in the .\library fold and present them to the user to select and execute.

Users can create there own scripts and related directories and place them into the .\library fold .

The user can create script with parameters which can be defined by the author.

Parameter which you require interactive input must be defined between the lines :

--- parameters start and --- parameters end (on seperate lines between the input DECLARE parameters)

Values which are replaced with user input/s require them to be marked with '&lt;value&gt;'

e.g.

--- parameters start

DECLARE @ProductId INT = &lt;value&gt;; --- Enter product Id ?

DECLARE @Description VARCHAR(30) = &lt;value&gt;; --- Enter description ?

--- parameters end

--- with results


Note, that after the DECLARE statements, the remark section (after the '---') will be used to create the prompt response to the user, but this is optional.

If you require the output of the script then you must include '--- with results' in the script on a seperate line and the output will be printed to the console.
Please include a question mark at the end of the prompt '?' for parsing of the parameter type.

The output is show in two modes, columns and rows.

Column mode will show the column name and python type on the same line.

Row mode will show the list collection of the python data structor, which saves space.

You can select the output by including '--- with results columns' for columns and '--- with results rows' for rows. 