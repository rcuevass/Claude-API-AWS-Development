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
         max_num_tokens: int = 1000,) -> str:
    # Make a request
    message = client_anthropic.messages.create(
        model=model_selected, # model selected by user, setup in cell above
        max_tokens=max_num_tokens, # max budget on number of tokens that Claude can generate. 
        messages=messages_lst
        )
    return message.content[0].text
