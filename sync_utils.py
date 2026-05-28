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

    # Stage and Commit
    subprocess.run(['git', '-C', repo_path, 'add', '.'], check=True)
    status = subprocess.run(['git', '-C', repo_path, 'status', '--porcelain'], capture_output=True, text=True)
    if status.stdout.strip():
        subprocess.run(['git', '-C', repo_path, 'commit', '-m', message], check=True)
    else:
        log_check = subprocess.run(['git', '-C', repo_path, 'log'], capture_output=True)
        if log_check.returncode != 0:
             subprocess.run(['git', '-C', repo_path, 'commit', '--allow-empty', '-m', message], check=True)

    # Explicit push using full authenticated URL
    if token:
        print('⌛ Synchronizing and pushing to GitHub via authenticated URL...')
        remote_url = f'https://{token}@github.com/celiaelazamey-arch/cela.pro2.git'
        result = subprocess.run(['git', '-C', repo_path, 'push', remote_url, 'HEAD:main', '--force'], capture_output=True, text=True)
    else:
        raise Exception('GITHUB_TOKEN missing. Cannot push to private repository.')

    if result.returncode != 0:
        raise Exception(f'Git Push Failed: {result.stderr}')
    print('✅ Push Successful.')
