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
    with open(filename) as f:
        text = f.read()
    return text

def show_help():
    print('=====] gitaggle/github.py [=====')
    print('')
    print('[SYNTAX]')
    print('')
    print('github.py --cmd <command> --work_dir [working_folder] --repo_url [repository_url]')
    print('')
    print('==> Commands <==')
    print('')
    print('<help> show this help')
    print('<clone> clone repository')
    print('')
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd", type=str, default='help')
    parser.add_argument("--work_dir", type=str, default=None)
    parser.add_argument("--repo_url", type=str, default='https://github.com/dinhtt-randrise/gitaggle.git')    
    args = parser.parse_args()
    if args.cmd == 'clone':
        clone(args.repo_url, args.work_dir)
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
    
if __name__ == "__main__":
    main()
