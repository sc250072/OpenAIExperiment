import logging
import re

from openai.lib.azure import AzureOpenAI

from com.teradata.openai.apihandler.APIHandler import APIHandler, Environment


class AzureOpenAIHandler(APIHandler):
    def __init__(self, env: Environment, li_table: list, user_query: str):
        super().__init__(env, li_table, user_query)
        if env.model_name is None:
            env.model_name = "gpt-35-turbo"
        self.client = AzureOpenAI(
            api_key=self.env.key,
            api_version="2024-02-01",
            azure_endpoint=self.env.endpoint
        )

    def get_query(self):
        message = self._get_NTS_msg()
        try:
            response = self.client.chat.completions.create(model=self.env.model_name,
                                                           messages=message,
                                                           temperature=0,
                                                           max_tokens=256)
            sql = response.choices[0].message.content
            if sql is not None and len(sql) > 0:
                # Extracting sql from response got from Azure OpenAI using regular expression. Query is embedded
                # between ```
                try:
                    pattern = r"```(.*?)```"
                    sql = re.findall(pattern, sql, re.DOTALL)[0]
                    logging.info("SQL - %s", sql)
                except Exception as ex:
                    logging.error(str(ex))
                    print(str(ex))
                return sql
            else:
                return None
        except Exception as ex:
            logging.error(str(ex))
            print(str(ex))
            return None

    def get_final_msg(self, output: str, user_query: str):
        content = f"User Question: {user_query}\n\nDatabase Data:\n{output}\n\nAnswer:"
        message = self._get_msg(content)
        try:
            response = self.client.chat.completions.create(model=self.env.model_name,
                                                           messages=message,
                                                           temperature=0,
                                                           max_tokens=256)
            response = response.choices[0].message.content
            return response
        except Exception as ex:
            logging.error(str(ex))
            print(str(ex))
            return None
