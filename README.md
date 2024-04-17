# Teradata Crystal Ball
This project aims to create SQL queries from natural language. 
This sample proof of concept (POC) is centered around tables that exist in the database of the logged-in user within the provided instance. 
It employs the OpenAI gpt-3.5-turbo language model to generate SQL queries based on human input. 
The process involves using the "show table" statement to retrieve the table structure, which is then utilized to construct prompts for the language model. 
The model generates SQL query statements, which are subsequently submitted to Teradata for execution. The results are then displayed as output.

Here are the steps for executing the project:

   1. Clone the project using the command "git clone".
   2. cd tera_crystalball
   3. create .evn file with below environment variables and modify values with relavent information.
      1. TERADATA_HOST=whomooz;
      2. TERADATA_USER=guest;
      3. TERADATA_PASSWORD=please;
      5. USER_QUERY=query.
      6. AZURE_OPENAI_ENDPOINT=azureendpointurl
      7. AZURE_OPENAI_API_KEY=azurere openai key
      8. AZURE_OPENAI_MODEL=modelname to use
      9. Run pip install -r requirements_dev.txt
     10. Run python main.py
 
 4. Set up slack bot configurations
	1. SLACK_APP_TOKEN=xapp-111111
	2. SLACK_BOT_TOKEN=xoxb-999999



