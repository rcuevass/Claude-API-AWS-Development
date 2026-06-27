# module that captures functions that are to be used multiple times to consume
# Claude via Amazon Bedrock

from dotenv import load_dotenv
import boto3

# load env. var
load_dotenv()
# create Amazon Bedrock client 
client = boto3.client("bedrock-runtime", region_name="us-west-2")


def add_user_message(messages: list, text: str) -> None:
    user_message = {
        "role": "user", 
        "content": [
            {"text": text}
        ]
    }    
    messages.append(user_message)


def add_assistant_message(messages: list, text: str) -> None:
    assistant_message = {
        "role": "assistant", 
        "content": [
            {"text": text}
        ]
    }
    messages.append(assistant_message)


def chat(messages_lst: list[str],
         client_azn_bedrock = client,
         model_id: str = "us.anthropic.claude-sonnet-4-6" ,
         temperature: float = 0.3,
         system_prompt: str = None) -> str:
    
    params = {
        "modelId": model_id, # model selected 
        "messages": messages_lst, # list of messages
        "inferenceConfig": {"temperature": temperature}, # value of temp. parameter. It ranges between 0 and 1}
    }

    if system_prompt:
        params["system"] = [{"text": system_prompt}]  # self-explanatory

    # Make a request
    response = client_azn_bedrock.converse(**params)
    #
    return response["output"]["message"]["content"][0]["text"]


def trigger_interactive_chat(temperature_value: float = 1.0):
    # initialize list of messages
    messages = []

    # start the while loop until an interruption takes place
    while True:
        # get user input
        user_input = input("> ")
        print(">", user_input)
        print('-'*10)
        # 
        add_user_message(messages=messages, text=user_input)
        #
        answer = chat(messages_lst=messages, temperature=temperature_value)
        print(answer.replace("**"," "))
        print('-'*10)
        #
        add_assistant_message(messages=messages, text=answer)

