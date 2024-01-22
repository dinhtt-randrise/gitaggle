import os
import argparse

def pat_dir():
    return os.environ.get('GGS_DIR', '/kaggle/input/gitaggle-settings/gitaggle-settings')

def debug_on():
    v = os.environ.get('DEBUG_ON', 'no')
    if v == 'yes':
        return True
    else:
        return False
    
def pat():
    return read_text_file(pat_dir() + '/GitHub-PAT.txt').lstrip().rstrip()

def read_text_file(filename):
    text = ''
    with open(filename, 'r') as f:
        text = f.read()
    return text

def write_text_file(filename, text):
    with open(filename, 'w') as f:
        f.write(text)

def show_help():
    print('=====] gitaggle/github.py [=====')
    print('')
    print('[SYNTAX]')
    print('')
    print('github.py --cmd <command> --work_dir [working_folder] --repo_url [repository_url] --repo_dir [repository_folder] --msg_file [message_file] --user_name [user_name] --user_email [user_email]')
    print('')
    print('==> Commands <==')
    print('')
    print('<help> show this help')
    print('<clone> clone repository')
    print('<commit> commit repository w/ pushing')
    print('<identity> set config (user name / user email)')
    print('')
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd", type=str, default='help')
    parser.add_argument("--work_dir", type=str, default=None)
    parser.add_argument("--repo_dir", type=str, default=None)
    parser.add_argument("--msg_file", type=str, default=None)    
    parser.add_argument("--user_name", type=str, default=None)    
    parser.add_argument("--user_email", type=str, default=None)        
    parser.add_argument("--repo_url", type=str, default='https://github.com/dinhtt-randrise/gitaggle.git')    
    args = parser.parse_args()
    if args.cmd == 'clone':
        clone(args.repo_url, args.work_dir)
    elif args.cmd == 'commit':
        commit(args.repo_dir, args.msg_file)
    elif args.cmd == 'identity':
        identity(args.repo_dir, args.user_name, args.user_email)
    else:
        show_help()
    
def clone(repo_url, to_dir = None):
    if to_dir is None:
        cmd = 'git clone ' + repo_url.replace('https://', 'https://' + pat() + '@')
    else:
        cmd = 'cd "' + str(to_dir) + '"' + ' && git clone ' + repo_url.replace('https://', 'https://' + pat() + '@')
    if debug_on():
        print('=> [CMD] ' + cmd)
    os.system(cmd)
    
def commit(repo_dir, msg_file):
    if repo_dir is None or msg_file is None:
        print('=> [E] File or folder is not found!')
        return
    if not os.path.exists(repo_dir) or not os.path.exists(msg_file):
        print('=> [E] File or folder does not exist!')
        return
    cmd = 'cd "' + repo_dir + '" && git add *.* && git commit -F "' + msg_file + '" && git push'
    if debug_on():
        print('=> [CMD] ' + cmd)
    os.system(cmd)
    
def identity(repo_dir, name, email):
    if repo_dir is None is None:
        print('=> [E] Folder is not found!')
        return
    if not os.path.exists(repo_dir):
        print('=> [E] Folder does not exist!')
        return    
    if name is None:
        print('=> [E] Name is required!')
        return
    if email is None:
        print('=> [E] Email is required!')
        return
    cmd = 'cd "' + repo_dir + '" && git config user.name "' + name + '" && git config user.email "' + email + '"'
    if debug_on():
        print('=> [CMD] ' + cmd)
    os.system(cmd)
    
if __name__ == "__main__":
    main()
