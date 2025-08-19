from tqdm import tqdm
from multiprocessing import Pool
import pickle, os

def chunk_apply(func, chunk):
    """Apply func to all elements in chunk"""
    return [func(i) for i in tqdm(chunk)]

from functools import partial

def split_list(lst, n):
    k, m = divmod(len(lst), n)
    ret =  [lst[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(n)]
    return [i for i in ret if len(i)]

def multiprocess(func, inp, cores= os.cpu_count()):
    inp = split_list(inp, cores)
    with Pool(cores) as p:
        f = partial(chunk_apply, func)
        return [j for i in list(tqdm(p.imap(f, inp), total = len(inp))) for j in i]

def save_var(path, obj):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def load_var(path):
    with open(path, 'rb') as f:
        r = pickle.load(f)
    return r

def list_all_files(folder_path):
    file_paths = []

    def recurse(current_path):
        for entry in os.listdir(current_path):
            full_path = os.path.join(current_path, entry)
            if os.path.isdir(full_path):
                recurse(full_path)
            else:
                file_paths.append(full_path)

    recurse(folder_path)
    return file_paths