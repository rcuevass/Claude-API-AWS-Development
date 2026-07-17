# module that captures functions that are to be used multiple times to consume
# Claude via API calls

from dotenv import load_dotenv
from anthropic import Anthropic

# load env. var
load_dotenv()
# create client 
client = Anthropic() 


def add_user_message(messages: list, text: str) -> None:
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages: list, text: str) -> None:
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def chat(messages_lst: list[str],
         client_anthropic = client,
         model_selected: str = "claude-sonnet-4-6",
         max_num_tokens: int = 1000,
         temperature: float = 1.0,
         system_prompt: str = None) -> str:
    
    params = {
        "model": model_selected, # model selected by user, setup by default
                                 # in function argument
        "max_tokens": max_num_tokens, # max budget on number of tokens that Claude can generate. 
        "messages": messages_lst, # list of messages,
        "temperature": temperature, # temperature parameter to control the "creativity" 
                                    # of responses. This values ranges between 0 and 1.
    }

    if system_prompt:
        params["system"] = system_prompt # self-explanatory

    # Make a request
    message = client_anthropic.messages.create(**params)
    #
    return message.content[0].text



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


def streaming_messages(text_msg: str, model_selected: str = "claude-sonnet-4-6",
                       num_max_tokens: int = 1000, print_message: bool = True):
    messages_lst = []
    add_user_message(messages_lst, text=text_msg)
    with client.messages.stream(
        model=model_selected,
        max_tokens=num_max_tokens,
        messages=messages_lst) as stream:
            for text in stream.text_stream:
                if print_message:
                    print(text, end="")
                else:
                    pass
    
    stored_events = stream.get_final_message()
    return stored_events
    