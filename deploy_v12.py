import os
from huggingface_hub import HfApi, upload_folder

token = os.environ.get("HF_TOKEN", "")
repo_id = "MTSE2026/mtse-ai-platform"
local_dir = "d:/engicost-ai/mtse-ai-platform-dev"

api = HfApi(token=token)

try:
    print(f"Deploying MTSE v12.0 to {repo_id}...")
    upload_folder(
        folder_path=local_dir,
        repo_id=repo_id,
        repo_type="space",
        token=token,
        ignore_patterns=[".git*", "__pycache__*", "*.pyc"]
    )
    print("Deployment Successful!")
except Exception as e:
    print(f"Deployment Error: {e}")
