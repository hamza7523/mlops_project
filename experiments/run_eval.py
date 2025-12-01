import argparse
import json
import os
import sys
import mlflow
import pandas as pd
from llama_cpp import Llama
from rouge_score import rouge_scorer

# Add the parent directory to sys.path to allow imports from experiments.prompts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.prompts import zero_shot, few_shot, meta_prompt

# Configuration
MODEL_DIR = os.getenv("MODEL_DIR", "backend/models")
GGUF_FILE = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
GGUF_PATH = os.path.join(MODEL_DIR, GGUF_FILE)
DATA_PATH = "data/eval.jsonl"

# Map strategy names to modules
STRATEGIES = {"zero_shot": zero_shot, "few_shot": few_shot, "meta_prompt": meta_prompt}


def load_model():
    print(f"🚀 Loading Model from {GGUF_PATH}...")
    if not os.path.exists(GGUF_PATH):
        raise FileNotFoundError(f"❌ Model not found at {GGUF_PATH}")

    return Llama(model_path=GGUF_PATH, n_ctx=2048, n_threads=4, verbose=False)


def evaluate(strategy_name):
    print(f"🧪 Starting Evaluation for Strategy: {strategy_name}")

    # 1. Setup
    llm = load_model()
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    prompt_module = STRATEGIES[strategy_name]

    results = []
    rouge_scores = []

    # 2. Load Data
    with open(DATA_PATH, "r") as f:
        data = [json.loads(line) for line in f]

    # 3. Run Inference
    mlflow.set_experiment("Flora_Prompt_Engineering")

    with mlflow.start_run(run_name=f"eval_{strategy_name}"):
        mlflow.log_param("strategy", strategy_name)
        mlflow.log_param("model", GGUF_FILE)

        for i, item in enumerate(data):
            question = item["question"]
            context = item.get("context_class")
            ideal = item["ideal_answer"]

            # Generate Prompt
            prompt = prompt_module.get_prompt(question, context)

            # Run Model
            output = llm(
                prompt,
                max_tokens=150,
                stop=["Question:", "Context:", "User Question:"],
                echo=False,
            )
            response = output["choices"][0]["text"].strip()

            # Calculate Metric (ROUGE-L)
            score = scorer.score(ideal, response)["rougeL"].fmeasure
            rouge_scores.append(score)

            print(f"[{i+1}/{len(data)}] Score: {score:.4f}")

            results.append(
                {
                    "question": question,
                    "context": context,
                    "ideal_answer": ideal,
                    "generated_answer": response,
                    "rouge_l": score,
                    "human_score": "",  # Placeholder for manual entry
                }
            )

        # 4. Log Aggregate Metrics
        avg_rouge = sum(rouge_scores) / len(rouge_scores)
        mlflow.log_metric("avg_rouge_l", avg_rouge)
        print(f"✅ Finished. Average ROUGE-L: {avg_rouge:.4f}")

        # 5. Save Results
        results_dir = "experiments/results"
        os.makedirs(results_dir, exist_ok=True)
        output_file = os.path.join(results_dir, f"results_{strategy_name}.csv")
        df = pd.DataFrame(results)
        df.to_csv(output_file, index=False)
        mlflow.log_artifact(output_file)
        print(f"💾 Results saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "strategy", choices=STRATEGIES.keys(), help="Prompting strategy to evaluate"
    )
    args = parser.parse_args()

    evaluate(args.strategy)
