python src/main.py \
    --model_name Qwen/Qwen2.5-Coder-0.5B \
    --trust_remote_code \
    --task HumanEval \
    --prompt_type Completion \
    --model_type Base \
    --save_path out/evals/qwen-0.5b/humaneval \
    --temperature 0.1

# python src/main.py \
#     --model_name EleutherAI/pythia-160m \
#     --trust_remote_code \
#     --task LeetCode \
#     --prompt_type Completion \
#     --model_type Base \
#     --save_path out/evals/pythia-160m/leetcode

# python src/main.py \
#     --model_name EleutherAI/pythia-160m \
#     --trust_remote_code \
#     --task MBPP \
#     --prompt_type Instruction \
#     --model_type Base \
#     --save_path out/evals/pythia-160m/mbpp

# python src/main.py \
#     --model_name ~/az-fs4/LLM-Shearing/out/prune_pythia/pythia_160m__70m_2048_opencoder-annealing/hf \
#     --trust_remote_code \
#     --task HumanEval \
#     --prompt_type Completion \
#     --model_type Base \
#     --save_path out/evals/pythia-70m-pruned/humaneval \
#     --temperature 0.1

# python src/main.py \
#     --model_name ~/az-fs4/LLM-Shearing/out/prune_pythia/pythia_160m__70m_2048_opencoder-annealing/hf \
#     --trust_remote_code \
#     --task LeetCode \
#     --prompt_type Completion \
#     --model_type Base \
#     --save_path out/evals/pythia-70m-pruned/leetcode

# python src/main.py \
#     --model_name ~/az-fs4/LLM-Shearing/out/prune_pythia/pythia_160m__70m_2048_opencoder-annealing/hf \
#     --trust_remote_code \
#     --task MBPP \
#     --prompt_type Instruction \
#     --model_type Base \
#     --save_path out/evals/pythia-70m-pruned/mbpp