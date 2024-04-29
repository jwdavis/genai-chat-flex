from google.cloud import secretmanager
import os

project_id = os.environ['GOOGLE_CLOUD_PROJECT']
region = os.environ['GOOGLE_CLOUD_REGION']

# collect secrets from Secret Manager
secrets = {}
client = secretmanager.SecretManagerServiceClient()
parent = f"projects/{project_id}"
for secret in client.list_secrets(request={"parent": parent}):
    secret_name = client.parse_secret_path(secret.name)["secret"]
    version_path = f"{secret.name}/versions/latest"
    response = client.access_secret_version(request={"name": version_path})
    secrets[secret_name] = response.payload.data.decode("UTF-8")

# collect markdown files
dir_path = "./"
files = os.listdir(dir_path)
md_files = [f for f in files if f.endswith('.md')]
md_dict = {}
for f in md_files:
    key = os.path.splitext(f)[0]
    with open(os.path.join(dir_path, f), 'r') as file:
        md_dict[key] = file.read()

chat_models = {
    'Gemini-Pro 1.5': 'gemini-1.5-pro-preview-0409',
    'GPT-4 Turbo': 'gpt-4-0125-preview',
    'Claude 3 Sonnet': "claude-3-sonnet@20240229",
    'Gemini-Pro 1.0': 'gemini-1.0-pro-002',
    'PaLMv2': 'chat-bison',
    'PaLMv2 32K': 'chat-bison-32k@002',
    'Codey': 'codechat-bison@002',
    'Codey 32K': 'codechat-bison-32k@002',
    'GPT-3.5 Turbo': 'gpt-3.5-turbo-0125',
    'Claude 3 Haiku': 'claude-3-haiku@20240307',
}

text_models = {
    'Gemini-Pro 1.5': 'gemini-1.5-pro-preview-0409',
    'GPT-4 Turbo': 'gpt-4-0125-preview',
    'Claude 3 Sonnet': "claude-3-sonnet@20240229",
    'Gemini-Pro 1.0': 'gemini-1.0-pro-002',
    'PaLMv2': 'text-bison',
    'PaLMv2 32K': 'text-bison-32k@002',
    'Codey': 'code-bison@002',
    'Codey 32K': 'code-bison-32k@002',
    'GPT-3.5 Turbo': 'gpt-3.5-turbo-0125',
    'Claude 3 Haiku': 'claude-3-haiku@20240307',
}

gemini_models = [
    'Gemini-Pro 1.0',
    'Gemini-Pro 1.5'
]

non_gemini_google_models = [
    'PaLMv2',
    'PaLMv2 32K',
    'Codey',
    'Codey 32K'
]

openai_models = [
    'GPT-4 Turbo',
    'GPT-3.5 Turbo'
]

claude_models = [
    'Claude 3 Sonnet',
    'Claude 3 Haiku'
]

codey_models = [
    'Codey',
    'Codey 32K'
]

image_models = {
    "Imagen 2": "imagen@006",
    "Dall-E 3": "dall-e-3"
}

google_image_models = [
    "Imagen 2"
]

openai_image_models = [
    "Dall-E 3"
]