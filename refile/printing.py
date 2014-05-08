def print_err(msg='unknown error', **kwargs):
    ERROR = '\033[31mError:\033[0m'
    print(ERROR, msg, **kwargs)


def print_warn(msg='unknown warning', **kwargs):
    WARNING = '\033[33mWarning:\033[0m'
    print(WARNING, msg, **kwargs)


def print_info(msg='well this isn\'t particularly helpful', **kwargs):
    INFO = '\033[34mInfo:\033[0m'
    print(INFO, msg, **kwargs)


def print_files(d, f_list):
    # if not current directory ('.')
    if d.name != '' and f_list:
        print(d, end='\n  ')
        print('\n  '.join(f.name for f in f_list))
    elif f_list:
        print('\n'.join(f.name for f in f_list))
