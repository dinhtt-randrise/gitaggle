import os
import argparse

PREPARED = False

def ggs_dir():
    return os.environ.get('GGS_DIR', '/kaggle/input/gitaggle-settings/gitaggle-settings')

def prepare():
    global PREPARED
    if not PREPARED:
        cmd = 'mkdir -p /root/.kaggle && cp -f "' + ggs_dir() + '/kaggle.json" "/root/.kaggle/" && chmod 600 /root/.kaggle/kaggle.json'
        if debug_on():
            print('=> [CMD] ' + cmd)
        os.system(cmd)
        PREPARED = True
            
def kg_user():
    return os.environ.get('KG_USER', 'dinhttrandrise')

def debug_on():
    v = os.environ.get('DEBUG_ON', 'no')
    if v == 'yes':
        return True
    else:
        return False
    
def download_notebook_output(nb_code, output_dir, nb_user = None):
    if output_dir is None:
        print('=> [E] Folder is not found!')
        return
    if nb_user is None:
        nb_user = kg_user()
    prepare()
    nb = nb_user + '/' + nb_code
    cmd = 'kaggle kernels output ' + nb + ' -p "' + output_dir + '"'
    if debug_on():
        print('=> [CMD] ' + cmd)
    os.system(cmd)

def download_notebook(nb_code, output_dir, nb_user = None):
    if output_dir is None:
        print('=> [E] Folder is not found!')
        return
    if nb_user is None:
        nb_user = kg_user()
    prepare()
    nb = nb_user + '/' + nb_code
    cmd = 'kaggle kernels pull ' + nb + ' -p "' + output_dir + '" -m'
    if debug_on():
        print('=> [CMD] ' + cmd)
    os.system(cmd)
    
def download_dataset(ds_code, output_dir, ds_user = None):
    if output_dir is None:
        print('=> [E] Folder is not found!')
        return
    if ds_user is None:
        ds_user = kg_user()
    prepare()
    nb = ds_user + '/' + ds_code
    cmd = 'kaggle datasets download -d ' + nb + ' -p "' + output_dir + '"'
    if debug_on():
        print('=> [CMD] ' + cmd)
    os.system(cmd)
    
def initialize_dataset(output_dir):
    if output_dir is None:
        print('=> [E] Folder is not found!')
        return
    prepare()
    cmd = 'kaggle datasets init -p "' + output_dir + '"'
    if debug_on():
        print('=> [CMD] ' + cmd)
    os.system(cmd)
    
def download_competition(cp_code, output_dir):
    if output_dir is None:
        print('=> [E] Folder is not found!')
        return
    prepare()
    cmd = 'kaggle competitions download -c ' + cp_code + ' -p "' + output_dir + '"'
    if debug_on():
        print('=> [CMD] ' + cmd)
    os.system(cmd)
    
def read_text_file(filename):
    text = ''
    with open(filename, 'r') as f:
        text = f.read()
    return text

def write_text_file(filename, text):
    with open(filename, 'w') as f:
        f.write(text)

def show_help():
    print('=====] gitaggle/kaggle.py [=====')
    print('')
    print('[SYNTAX]')
    print('')
    print('github.py --cmd <command> --kg_user [kaggle_user] --nb_code [notebook_code] --ds_code [dataset_code] --cp_code [competition_code] --output_dir [output_dir]')
    print('')
    print('==> Commands <==')
    print('')
    print('<help> show this help')
    print('<dl.nb.op> download notebook output')
    print('<dl.nb.src> download notebook source code')
    print('<dl.ds> download dataset files')
    print('<md.ds> initialize dataset metadata')
    print('<dl.cp> download competition files')
    print('')
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd", type=str, default='help')
    parser.add_argument("--kg_user", type=str, default=None)
    parser.add_argument("--nb_code", type=str, default=None)
    parser.add_argument("--ds_code", type=str, default=None)
    parser.add_argument("--cp_code", type=str, default=None)
    parser.add_argument("--output_dir", type=str, default=None)
    args = parser.parse_args()
    if args.cmd == 'dl.nb.op':
        download_notebook_output(args.nb_code, args.output_dir, args.kg_user)
    elif args.cmd == 'dl.nb.src':
        download_notebook(args.nb_code, args.output_dir, args.kg_user)
    elif args.cmd == 'dl.ds':
        download_dataset(args.ds_code, args.output_dir, args.kg_user)
    elif args.cmd == 'md.ds':
        initialize_dataset(args.output_dir)
    elif args.cmd == 'dl.cp':
        download_competition(args.cp_code, args.output_dir)
    else:
        show_help()
    
if __name__ == "__main__":
    main()
