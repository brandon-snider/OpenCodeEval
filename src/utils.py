import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([os.path.dirname(ROOT), os.path.dirname(os.path.dirname(ROOT))])

import re
import gzip
import json
import itertools
import numpy as np

from tqdm import tqdm
from collections import defaultdict
from typing import Dict, List, Union, Iterable, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

def multi_process_function(function: Callable,
                           parameters: List,
                           num_workers: int = 1,
                           desc: str = "Completing tasks"):
    
    if num_workers > len(parameters) or num_workers > os.cpu_count():
        num_workers = min(os.cpu_count(), len(parameters))

    with ThreadPoolExecutor(num_workers) as executor:
        futures = []
        for param in parameters:
            future = executor.submit(function, param)
            futures.append(future)
            
        results = []
        for future in tqdm(as_completed(futures), total=len(futures), desc=desc):
            result = future.result()
            results.append(result)

    return results

def program_extract(text: str, program: str = "python") -> str:

    program_pattern = rf"```{program}[ \t]*[\r\n]+(.*?)[ \t]*[\r\n]+```"
    program_re = re.compile(program_pattern, re.DOTALL | re.IGNORECASE)

    match = program_re.search(text)
    if match:
        return match.group(1)
    else:
        return ""

def refine_text(text: str) -> str:
    text =  text.replace("\t", "    ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.strip() + "\n"

def stream_jsonl(filename: str) -> Iterable[Dict]:
    """
    Parses each jsonl line and yields it as a dictionary
    """
    if filename.endswith(".gz"):
        with open(filename, "rb") as gzfp:
            with gzip.open(gzfp, 'rt') as fp:
                for line in fp:
                    if any(not x.isspace() for x in line):
                        yield json.loads(line)
    else:
        with open(filename, "r", encoding="utf-8") as fp:
            for line in fp:
                if any(not x.isspace() for x in line):
                    yield json.loads(line)


def write_jsonl(filename: str, data: Iterable[Dict], append: bool = False):
    """
    Writes an iterable of dictionaries to jsonl
    """
    if append:
        mode = 'ab'
    else:
        mode = 'wb'
    filename = os.path.expanduser(filename)
    if filename.endswith(".gz"):
        with open(filename, mode) as fp:
            with gzip.GzipFile(fileobj=fp, mode='wb') as gzfp:
                for x in data:
                    gzfp.write((json.dumps(x) + "\n").encode('utf-8'))
    else:
        with open(filename, mode) as fp:
            for x in data:
                fp.write((json.dumps(x) + "\n").encode('utf-8'))

def group_and_count(lst, group_key, count_key):

    grouped_counts = defaultdict(int)
    
    for item in lst:
        group = item.get(group_key)
        if group not in grouped_counts:
            grouped_counts[group] = 0
        if item.get(count_key) == True:
            grouped_counts[group] += 1
    
    return list(grouped_counts.values())

def estimate_pass_at_k(
    num_samples: Union[int, List[int], np.ndarray],
    num_correct: Union[List[int], np.ndarray],
    k: int
) -> np.ndarray:
    """
    Estimates pass@k of each problem and returns them in an array.
    """

    def estimator(n: int, c: int, k: int) -> float:
        """
        Calculates 1 - comb(n - c, k) / comb(n, k).
        """
        if n - c < k:
            return 1.0
        return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

    if isinstance(num_samples, int):
        num_samples_it = itertools.repeat(num_samples, len(num_correct))
    else:
        assert len(num_samples) == len(num_correct)
        num_samples_it = iter(num_samples)

    return np.array([estimator(int(n), int(c), k) for n, c in zip(num_samples_it, num_correct)])
