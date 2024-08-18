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
print(secrets)

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
    'Gemini 1.5 Flash': 'gemini-1.5-flash',
    'GPT-4o': 'gpt-4o',
    'Claude 3 Opus': "claude-3-opus@20240229",
    'Gemini 1.5 Pro': 'gemini-1.5-pro-preview-0409',
    'Gemini 1.0 Pro': 'gemini-1.0-pro-002',
    'PaLMv2': 'chat-bison',
    'Codey': 'codechat-bison@002',
    'GPT-4o mini': 'gpt-4o-mini',
    'GPT-4 Turbo': 'gpt-4-0125-preview',
    'GPT-3.5 Turbo': 'gpt-3.5-turbo-0125',
    'Claude 3.5 Sonnet': "claude-3-sonnet@20240229",
    'Claude 3 Haiku': 'claude-3-haiku@20240307',
}

text_models = {
    'Gemini 1.5 Flash': 'gemini-1.5-flash',
    'Gemini 1.5 Pro': 'gemini-1.5-pro-preview-0409',
    'Gemini 1.0 Pro': 'gemini-1.0-pro-002',
    'PaLMv2': 'text-bison',
    'Codey': 'code-bison@002',
    'GPT-4o': 'gpt-4o',
    'GPT-4o mini': 'gpt-4o-mini',
    'GPT-4 Turbo': 'gpt-4-0125-preview',
    'GPT-3.5 Turbo': 'gpt-3.5-turbo-0125',
    'Claude 3 Opus': "claude-3-opus@20240229",
    'Claude 3.5 Sonnet': "claude-3-sonnet@20240229",
    'Claude 3 Haiku': 'claude-3-haiku@20240307',
}

gemini_models = [
    'Gemini 1.5 Pro',
    'Gemini 1.5 Flash',
    'Gemini 1.0 Pro'
]

non_gemini_google_models = [
    'PaLMv2',
    'Codey',
]

openai_models = [
    'GPT-4 Turbo',
    'GPT-3.5 Turbo',
    'GPT-4o',
    'GPT-4o mini'
]

claude_models = [
    'Claude 3 Opus',
    'Claude 3.5 Sonnet',
    'Claude 3 Haiku'
]

codey_models = [
    'Codey'
]

image_models = {
    "Imagen 2": "imagegeneration@006",
    "Dall-E 3": "dall-e-3"
}

google_image_models = [
    "Imagen 2"
]

openai_image_models = [
    "Dall-E 3"
]