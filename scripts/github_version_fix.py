import os

if __name__ == "__main__":
    github_ref_type = os.environ.get('GITHUB_REF_TYPE')
    github_sha = os.environ.get("GITHUB_SHA")
    github_ref_name = os.environ.get("GITHUB_REF_NAME")
    github_event_name = os.environ.get("GITHUB_EVENT_NAME")
    github_head_ref = os.environ.get("GITHUB_HEAD_REF")

    if github_ref_type == "tag":
        # Use tag for version if it exists
        version = github_ref_name
    elif github_event_name == "pull_request":
        # For pull requests use the branch, short SHA and the ref (pr-#)
        version = f"{github_head_ref}_{github_sha[:8]}_{github_ref_name}"
    elif github_event_name != "pull_request" and github_ref_type == "branch":
        # For pushes to branch use branch and short SHA
        version = f"{github_ref_name}_{github_sha[:8]}"
    else:
        # For any other situations use the full SHA
        version = github_sha

    with open('flask_app/__version__.py', 'w') as f:
        print(f'__version__ = "{version}"', file=f)

    with open('webapp/app/utils/ui_version.js', 'w') as f:
        print(f'export default "{version}";', file=f)
