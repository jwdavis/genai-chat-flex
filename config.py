from google.cloud import secretmanager
import os

PROJECT_ID = os.environ['GOOGLE_CLOUD_PROJECT']
PROJECT_NUMBER = os.environ['GOOGLE_CLOUD_PROJECT_NUMBER']
secrets = {}

# get secret content from secret manager
client = secretmanager.SecretManagerServiceClient()
parent = f"projects/{PROJECT_ID}"
for secret in client.list_secrets(request={"parent": parent}):
    secret_name = client.parse_secret_path(secret.name)["secret"]
    version_path = f"{secret.name}/versions/latest"
    response = client.access_secret_version(request={"name": version_path})
    secrets[secret_name] = response.payload.data.decode("UTF-8")


def load_markdown_files():
    dir_path = "./"
    files = os.listdir(dir_path)
    md_files = [f for f in files if f.endswith('.md')]
    md_dict = {}
    for f in md_files:
        key = os.path.splitext(f)[0]
        with open(os.path.join(dir_path, f), 'r') as file:
            md_dict[key] = file.read()
    return md_dict
