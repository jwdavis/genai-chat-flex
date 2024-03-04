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
    subcollection_ref.set({
        "prompt": db_info["prompt"].content,
        "messages": convert_to_list(db_info["messages"]),
        "model": db_info["model"],
        "hash": db_info["hash"]
    })

def get_user_chat_metadata(email, model):
    db = firestore.Client()
    parent_ref = db.collection("users").document(email)
    subcollection_ref = parent_ref.collection("chats")
    chats = subcollection_ref.stream()
    chat_list = []
    for chat in chats:
        chat_list.append(chat.to_dict()["prompt"][:50])
    return chat_list