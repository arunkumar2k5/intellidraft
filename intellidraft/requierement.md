Create an application : Name of the application is intellidraft.        

Phase 1 :

TEchnology : Python / React as front end and uvicorn as server with fast API implementation ( check the validdity of this combiniation )
API based access to the OpenAI . use env file to store the api key . 
IF required you can change technogy as requied. 

Requirement : 
1. The opening screen has a browse option to select a template file.  In this template , we need to update the section called FUcntional Descriton 
2. There should be two tabs one is single component and second tab is batch processing. 
3. Requirement for single component. 
    A text box to enter the part number and a search button. 
    first task is to use openAI API to find the type of the component.
    Based on the type of the component , the script shall choose the  parameter from a JSON file. 
    E.g IF resistor what parameters to be extracted from web . ( this json file will be in the library folder )
    Next use the digikey API to extract the parameters. using the file @digikey.py in the library folder. 
    Now display the parameters in the main screen for the user to see . Have the value field editable for the user. 
    once the user is done . there is a button in the bottom to generate a document. What we need to do is open template document in that we need to update the functional description section with the parameters extracted from the web.  Need to form a neat table. The name of the file is same as that of the component . 

Before you start the coding do the following . 

Tell me the brief of what you are going to do and also create this parameter json file first for the basic components like resistor, capacitor, inductor, diode, transistor. to begin with we can expand it later. 


Phase 2 : Batch Mode. 

Phase 3 : Active components which calls the extractAI for performace . 
 

