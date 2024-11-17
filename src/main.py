import os
import argparse

os.environ["TOKENIZERS_PARALLELISM"] = "false"

import numpy as np
from tqdm import tqdm

from args import get_args, check_args
from utils import refine_text, write_jsonl, group_and_count, estimate_pass_at_k, multi_process_function, program_extract

from backend.vllm import VllmGenerator
from factory import BenchmarkFactory, BackendFactory

def main():
    parser = argparse.ArgumentParser()
    args = get_args(parser)
    args = check_args(args)

    save_path = args.save_path
    os.makedirs(save_path, exist_ok=True)

    task = BenchmarkFactory.get_task(args)

    decoder = BackendFactory.get_backend(args)

    prompts = task.get_prompt()

    for prompt in prompts:
        prompt['prompt'] = refine_text(args.prompt_prefix + prompt['prompt'] + args.prompt_suffix)
    write_jsonl(save_path + "/prompts.jsonl", prompts)

    end_words = task.general_stop_words + task.completion_stop_words if args.model_type == "Base" else task.general_stop_words
    generations = decoder.generate(prompts,
                                   end_words,
                                   args.response_prefix,
                                   args.response_suffix)
    write_jsonl(save_path + "/generations.jsonl", generations)

    solutions = multi_process_function(function = task.postprocess_generation,
                                       parameters = generations,
                                       num_workers = args.num_workers,
                                       desc = "Post-processing solutions")
    write_jsonl(save_path + "/solutions.jsonl", solutions)

    evaluations = multi_process_function(function = task.process_results,
                                             parameters = solutions,
                                             num_workers = args.num_workers,
                                             desc = "Evaluating solutions")
    write_jsonl(save_path + "/evaluation.jsonl", evaluations)

    result_list = group_and_count(evaluations, group_key = 'task_id', count_key = 'passed')
    pass_rate = float(np.mean(estimate_pass_at_k(num_samples = args.num_samples, num_correct = result_list, k = 1)))
    write_jsonl(save_path + "/result.json", [{"score": pass_rate}])
    print("Pass@1:", pass_rate)

if __name__ == "__main__":
    main()