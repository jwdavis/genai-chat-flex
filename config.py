from google.cloud import secretmanager
import os

PROJECT_ID = os.environ['GOOGLE_CLOUD_PROJECT']
PROJECT_NUMBER = os.environ['GOOGLE_CLOUD_PROJECT_NUMBER']

# collect secrets from Secret Manager
secrets = {}
client = secretmanager.SecretManagerServiceClient()
parent = f"projects/{PROJECT_ID}"
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

text_gen_models = {
    'Gemini 1.0 Pro': 'gemini-1.0-pro',
    'PaLM': 'text-bison',
    'PaLM 32K': 'text-bison-32k',
    'Palm Unicorn': 'text-unicorn',
    'Codey': 'code-bison',
    'GPT-3.5 Turbo': 'gpt-3.5-turbo',
    'GPT-4 Turbo': 'gpt-4-turbo-preview',
    # 'Gemini 1.0 Pro Vision (soon)': 'gemini-1.0-pro-vision',
    # 'GPT-4 Turbo Vision (soon)': 'gpt-4-vision-preview',
}

image_gen_models = {
    "Imagen 2": "imagegeneration@005",
    "DALL-E": "dalle-e-3",
}

default_model_args = {
    'compare': {
        "temperature": 0.2,
        "max_tokens": 2048,
        "top_p": 1,
        "candidate_count": 1,
        "logprobs": False,
    },
    'PaLM': {
        "temperature": 0.2,
        "max_tokens": 2048,
        "candidate_count": 1,
        "top_p": 1,
    },
    'PaLM 32K': {
        "temperature": 0.2,
        "max_tokens": 2048,
        "candidate_count": 1,
        "top_p": 1,
    },
    'PaLM Unicorn': {
        "temperature": 0.2,
        "max_tokens": 1024,
        "candidate_count": 1,
        "top_k": 40,
    },
    'Gemini 1.0 Pro': {
        "temperature": 0.2,
        "max_tokens": 2048,
        "top_p": 1,
    },
    'GPT-3.5 Turbo': {
        "temperature": 0.2,
        "max_tokens": 2048,
        "logprobs": False,
    },
    'GPT-4 Turbo': {
        "temperature": 0.2,
        "max_tokens": 2048,
        "logprobs": False,
    },
    'Codey': {
        "temperature": 0.2,
        "max_tokens": 2048,
        "top_p": 1,
        "candidate_count": 1,
    },
    'Gemini 1.0 Pro Vision (soon)': {
        "temperature": 0.2,
        "max_tokens": 2048,
    },
    'GPT-4 Turbo Vision (soon)': {
        "temperature": 0.2,
        "max_tokens": 2048,
    },
    'Imagen 2': {
        "temperature": 0.2,
        "max_tokens": 2000,
    },
    'DALL-E': {
        "temperature": 0.2,
        "max_tokens": 2000,
    },
}