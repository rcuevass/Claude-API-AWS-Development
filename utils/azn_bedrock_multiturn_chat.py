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


def azn_streaming_messages(text_msg: str, model_id: str = "us.anthropic.claude-sonnet-4-6",
                           print_event: bool = True, loop_over_stream: bool = True):
    messages_lst = []
    add_user_message(messages=messages_lst, text=text_msg)
    # notice the signature below for model identification: modelId
    response = client.converse_stream(messages=messages_lst, modelId=model_id)

    # printing this response takes place almost immediately (~ 1 sec),
    # this response does not include any genearated text, instead it generates stream as an
    # event stream object - it is a generates that we can iterate over ("stream" key)
    if print_event:
        print(response)

    print("======"*7)

    if loop_over_stream:
        for event in response["stream"]:
            print(event)

    print("======"*7)

    text = ""
    for event in response["stream"]:
        if "contentBlockDelta" in event:
            chunk_txt = event["contentBlockDelta"]["delta"]["text"]
            print(chunk_txt, end="")
            text += chunk_txt

    return "\n\nTotal Message:\n" + text