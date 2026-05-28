import subprocess
import os

def git_smart_push(repo_path, message, token=None):
    subprocess.run(['git', 'config', '--global', '--add', 'safe.directory', repo_path], check=True)

    if not os.path.exists(os.path.join(repo_path, '.git')):
        subprocess.run(['git', '-C', repo_path, 'init'], check=True)

    # Explicitly set/rename branch to main
    subprocess.run(['git', '-C', repo_path, 'branch', '-M', 'main'], check=True)

    # Update remote URL with token if provided
    if token:
        remote_url = f'https://{token}@github.com/celiaelazamey-arch/cela.pro2.git'
        subprocess.run(['git', '-C', repo_path, 'remote', 'set-url', 'origin', remote_url], capture_output=True)
    
    subprocess.run(['git', '-C', repo_path, 'config', 'user.email', 'archive@cela.pro'], check=True)
    subprocess.run(['git', '-C', repo_path, 'config', 'user.name', 'Archive Agent'], check=True)

    subprocess.run(['git', '-C', repo_path, 'add', '.'], check=True)

    # Check for changes and commit
    status = subprocess.run(['git', '-C', repo_path, 'status', '--porcelain'], capture_output=True, text=True)
    if status.stdout.strip():
        subprocess.run(['git', '-C', repo_path, 'commit', '-m', message], capture_output=True)
    else:
        # Ensure at least one commit exists to push
        log_check = subprocess.run(['git', '-C', repo_path, 'log'], capture_output=True)
        if log_check.returncode != 0:
             subprocess.run(['git', '-C', repo_path, 'commit', '--allow-empty', '-m', message], capture_output=True)

    print('⌛ Synchronizing and pushing to GitHub...')
    result = subprocess.run(['git', '-C', repo_path, 'push', 'origin', 'main', '--force'], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f'Git Push Failed: {result.stderr}')
    print('✅ Push Successful.')
