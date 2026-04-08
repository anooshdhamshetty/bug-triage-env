import os
from huggingface_hub import HfApi
from dotenv import load_dotenv

load_dotenv()

api = HfApi()

token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN") or None
repo_type = os.environ.get("HF_REPO_TYPE", "space")

try:
    username = api.whoami(token=token)["name"]
    repo_id = os.environ.get("HF_REPO_ID", f"{username}/bug")
except Exception as e:
    if "Token is required" in str(e) or "not logged in" in str(e):
        raise SystemExit(
            "No Hugging Face authentication found. Run 'hf auth login' first, or set HF_REPO_ID environment variable with your target repo (e.g. HF_REPO_ID=yourname/bug)."
        )
    raise

print(f"Uploading to HF Repository: {repo_id}...")
try:
    # Ensure the repo exists as a Space
    try:
        api.repo_info(repo_id=repo_id, repo_type=repo_type, token=token)
    except Exception:
        print(f"Space {repo_id} not found. Creating it...")
        api.create_repo(repo_id=repo_id, repo_type=repo_type, token=token, space_sdk="docker")

    api.upload_folder(
        folder_path=".",
        repo_id=repo_id,
        repo_type=repo_type,
        token=token,
        ignore_patterns=[
            "upload_out.txt",
            "upload_hf.py",
            ".git",
            "__pycache__",
            "outputs",
            "login_output.txt",
            ".env",
            "**/.env",
            "bug/.env",
        ]
    )
    print("Upload successful!")
except Exception as e:
    if "401" in str(e) or "Invalid username or password" in str(e):
        print(
            "Error: Hugging Face authentication failed. Use a valid HF token with write access, and make sure HF_REPO_ID points to a repo/space you own or can create.",
        )
    else:
        print("Error:", e)