from google.cloud import firestore
from config import secrets, PROJECT_ID

def convert_to_list(messages):
    """
    Convert a list of messages to a list of dictionaries.

    Args:
        messages (list): A list of messages.

    Returns:
        list: A list of dictionaries.
    """
    return [{"content": message.content, "role": message.role} for message in messages]

def store_chat(email, db_info):
    db = firestore.Client()
    parent_ref = db.collection("users").document(email)
    subcollection_ref = parent_ref.collection("chats").document(db_info["hash"])
    res = subcollection_ref.set({
        "messages": convert_to_list(db_info["messages"]),
        "model": db_info["model"],
        "hash": db_info["hash"]
    })
    print(res)

def get_user_chat_metadata(email, model):
    db = firestore.Client()
    parent_ref = db.collection("users").document(email)
    subcollection_ref = parent_ref.collection("chats")
    chats = subcollection_ref.stream()
    chat_prompts = []
    chat_hashes = []
    for chat in chats:
        chat_prompts.append(chat.to_dict()['messages'][1]['content'][:50])
        chat_hashes.append(chat.to_dict()["hash"])
    return {
        "prompts": chat_prompts, 
        "hashes": chat_hashes
    }
