import logging
import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from com.teradata.openai.apihandler.APIHandler import Environment
from com.teradata.openai.apihandler.AzureOpenAIHandler import AzureOpenAIHandler
from com.teradata.openai.teradataapi.teradata_api import TeradataApi
from com.teradata.openai.util.Logging import Logging

load_dotenv()

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
app = App(token=SLACK_BOT_TOKEN, name="Slack Bot")
key = os.getenv("AZURE_OPENAI_API_KEY")
db_name = os.getenv("TERADATA_USER")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_model_name = os.getenv("AZURE_OPENAI_MODEL")


class Main(Logging):

    @app.event("message")
    def promt_for_sql(message, say):
        dm_channel = message["channel"]
        user_id = message["user"]
        user_query = message["text"]
        logging.info(f"Sent request < {user_query} ")
        main = Main()
        response = main.executeQ(user_query)  # add logic
        if response is not None and len(response) > 0:
            list_string = ''
            for row in response:
                if row is not None:
                    logging.info("Response type is " + str(type(row)))
                    list_string = list_string + (str(row))+"\n"
                    print(list_string)
                    logging.info(f"Sent response < {list_string} > to user {user_id}")
            say(text=list_string, channel=dm_channel)
        else:
            say(text='No response found for given question', channel=dm_channel)

    def validate(self, user_query):
        if key is None or user_query is None or azure_endpoint is None:
            raise Exception("Please provide Azure OpenAI API key, end point and user question")

    def executeQ(self, user_query):
        mainObj = Main()
        mainObj.validate(user_query)
        tapi = TeradataApi()
        env = Environment(key, azure_endpoint, azure_model_name)
        if db_name is not None:
            tbl_list = tapi.get_table_names(db_name)
            api = AzureOpenAIHandler(env, tbl_list, user_query)
            query = api.get_query()
            if query is not None:
                con = tapi.get_con()
                try:
                    with con.cursor() as cur:
                        cur.execute(query)
                        rows = cur.fetchall()
                        if len(rows) > 0:
                            for row in rows:
                                self.log.info(row)
                                print(row)
                            return rows
                        else:
                            self.log.info("No data exists")
                            print("No data exists")
                except Exception as ex:
                    self.log.error(str(ex))
            else:
                self.log.error("OpenAI API failed to return SQL query for specified query : %s ", user_query)
        else:
            raise Exception("Please provider a valid username")


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()
