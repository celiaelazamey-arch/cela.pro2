import subprocess
import os

def git_smart_push(repo_path, message, token=None):
    # Ensure safe directory
    subprocess.run(['git', 'config', '--global', '--add', 'safe.directory', '*'], check=True)

    if not os.path.exists(os.path.join(repo_path, '.git')):
        subprocess.run(['git', '-C', repo_path, 'init'], check=True)

    # Set identity
    subprocess.run(['git', '-C', repo_path, 'config', 'user.email', 'archive@cela.pro'], check=True)
    subprocess.run(['git', '-C', repo_path, 'config', 'user.name', 'Archive Agent'], check=True)

    # Explicitly set/rename branch to main
    subprocess.run(['git', '-C', repo_path, 'branch', '-M', 'main'], check=True)

    # Robust Remote Handling
    if token:
        remote_url = f'https://{token}@github.com/celiaelazamey-arch/cela.pro2.git'
        # Check if remote exists using a more reliable check
        check_remote = subprocess.run(['git', '-C', repo_path, 'remote', 'get-url', 'origin'], capture_output=True, text=True)
        
        if check_remote.returncode == 0:
            print('Updating existing origin remote...')
            subprocess.run(['git', '-C', repo_path, 'remote', 'set-url', 'origin', remote_url], check=True)
        else:
            print('Adding new origin remote...')
            subprocess.run(['git', '-C', repo_path, 'remote', 'add', 'origin', remote_url], check=True)

    # Stage and Commit
    subprocess.run(['git', '-C', repo_path, 'add', '.'], check=True)
    status = subprocess.run(['git', '-C', repo_path, 'status', '--porcelain'], capture_output=True, text=True)
    if status.stdout.strip():
        subprocess.run(['git', '-C', repo_path, 'commit', '-m', message], check=True)
    else:
        log_check = subprocess.run(['git', '-C', repo_path, 'log'], capture_output=True)
        if log_check.returncode != 0:
             subprocess.run(['git', '-C', repo_path, 'commit', '--allow-empty', '-m', message], check=True)

    print('⌛ Synchronizing and pushing to GitHub...')
    # Note: Using origin main explicitly
    result = subprocess.run(['git', '-C', repo_path, 'push', 'origin', 'main', '--force'], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f'Git Push Failed: {result.stderr}')
    print('✅ Push Successful.')
