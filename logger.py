import os
import random
from datetime import datetime
from . import github as gggh

ALL_LOGGER = {}

def gh_user_name():
    return os.environ.get('USER_NAME', 'Dinh Thoai Tran @ randrise.com')

def gh_user_email():
    return os.environ.get('USER_EMAIL', 'dinhtt@randrise.com')

def create_logger(gh_user_name, gh_user_email, gh_repo_url, nb_code):
    lid = random.randint(0, 1000000)
    while lid in ALL_LOGGER:
        lid = random.randint(0, 1000000)
    ld = {'id': lid, 'user_name': gh_user_name, 'user_email': gh_user_email, 'repo_url': gh_repo_url, 'nb_code': nb_code, 'logs': ''}
    ALL_LOGGER[lid] = ld
    return lid

def read_log_file(lid, path, def_val):
    if lid not in ALL_LOGGER:
        return
    ld = ALL_LOGGER[lid]
    now = datetime.now()
    root_dir = '/kaggle/tmp/logger-' + ld['nb_code'] + '-' + str(lid)
    os.system('rm -rf "' + root_dir + '"')
    os.system('mkdir -p "' + root_dir + '"')

    folder_name = ld['repo_url'].split('/')[-1].replace('.git', '')
    repo_dir = root_dir + '/' + folder_name
    gggh.clone(ld['repo_url'], root_dir)
    fn = path.split('/')[-1]
    fd = path[:len(path) - len(fn) - 1]
    log_dir = repo_dir + fd
    os.system('mkdir -p "' + log_dir + '"')
    log_file = log_dir + '/' + fn

    try:
        sn = gggh.read_text_file(log_file)
        return sn
    except Exception as e:
        return def_val
        
def flush_log(lid):
    if lid not in ALL_LOGGER:
        return
    ld = ALL_LOGGER[lid]
    if len(ld['logs'].lstrip().rstrip()) == 0:
        return
    now = datetime.now()
    root_dir = '/kaggle/tmp/logger-' + ld['nb_code'] + '-' + str(lid)
    os.system('rm -rf "' + root_dir + '"')
    os.system('mkdir -p "' + root_dir + '"')

    folder_name = ld['repo_url'].split('/')[-1].replace('.git', '')
    repo_dir = root_dir + '/' + folder_name
    gggh.clone(ld['repo_url'], root_dir)
    log_dir = repo_dir + '/nb/' + ld['nb_code'] + '/' + now.strftime('%Y') + '/' + now.strftime('%m') + '/' + now.strftime('%d')
    os.system('mkdir -p "' + log_dir + '"')
    log_file = log_dir + '/log-' + now.strftime('%H-%M-%S') + '.txt'

    gggh.write_text_file(log_file, ld['logs'])
    print('=> [L] ' + log_dir + ' | ' + repo_dir)
    os.system('ls "' + log_dir + '"')
    msg_file = '/kaggle/tmp/log-msg-' + ld['nb_code'] + '-' + str(lid) + '.txt'
    gggh.write_text_file(msg_file, 'Write logs at [' + now.strftime("%m/%d/%Y, %H:%M:%S") + ']')
    gggh.identity(repo_dir, ld['user_name'], ld['user_email'])
    gggh.commit(repo_dir, msg_file)
    ld['logs'] = ''
    ALL_LOGGER[lid] = ld
    
def save_log(lid, text):
    if lid not in ALL_LOGGER:
        return
    ld = ALL_LOGGER[lid]
    now = datetime.now()
    ln = '[' + now.strftime("%m/%d/%Y, %H:%M:%S") + '] ' + str(text)
    ld['logs'] += '\n' + ln
    ALL_LOGGER[lid] = ld
    if len(ld['logs']) > 1024 * 1024:
        flush_log(lid)

def flush_all():
    for lid in ALL_LOGGER.keys():
        flush_log(lid)
