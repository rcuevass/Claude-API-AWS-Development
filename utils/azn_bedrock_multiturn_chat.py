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
         system_prompt: str = None) -> str:
    
    params = {
        "modelId": model_id, # model selected 
        "messages": messages_lst, # list of messages
    }

    if system_prompt:
        params["system"] = [{"text": system_prompt}]  # self-explanatory

    # Make a request
    response = client_azn_bedrock.converse(**params)
    #
    return response["output"]["message"]["content"][0]["text"]
