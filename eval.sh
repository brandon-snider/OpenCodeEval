python /root/OpenCodeEval/src/main.py \
    --model_name EleutherAI/pythia-160m \
    --trust_remote_code \
    --task HumanEval \
    --prompt_type Completion \
    --model_type Base \
    --save_path /root/pruning-vol/evals/pythia-160m/humaneval

python /root/OpenCodeEval/src/main.py \
    --model_name EleutherAI/pythia-160m \
    --trust_remote_code \
    --task LeetCode \
    --prompt_type Completion \
    --model_type Base \
    --save_path /root/pruning-vol/evals/pythia-160m/leetcode

python /root/OpenCodeEval/src/main.py \
    --model_name EleutherAI/pythia-160m \
    --trust_remote_code \
    --task MBPP \
    --prompt_type Instruction \          
    --model_type Base \
    --save_path /root/pruning-vol/evals/pythia-160m/mbpp