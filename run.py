import argparse
import subprocess
from pathlib import Path
import sys

TASKS = {
    "magic_numbers": "magic_numbers/main.py",
    "drop_test": "drop_test/main.py",
    "ipconfig_parser": "ipconfig_parser/main.py",
    "parking_calculator": "parking_calculator/main.py"
}

def run_task(task_name: str) -> None:
    if task_name not in TASKS:
        print(f"Error: Task '{task_name}' not found.")
        return
        
    script_path = Path(__file__).parent / TASKS[task_name]
    print(f"\n{'='*40}")
    print(f"Running {task_name}...")
    print(f"{'='*40}")
    
    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Task '{task_name}' failed with exit code {e.returncode}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Nokia Hackathon Solutions CLI")
    parser.add_argument("--task", type=str, choices=list(TASKS.keys()), help="Run a specific task")
    parser.add_argument("--all", action="store_true", help="Run all tasks sequentially")
    
    args = parser.parse_args()
    
    if args.all:
        for task in TASKS:
            run_task(task)
    elif args.task:
        run_task(args.task)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
