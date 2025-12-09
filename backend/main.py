"""
Main entry point for the LangGraph Text Analysis Workflow

This script demonstrates how to use the workflow with various
input texts and configuration options.
"""

import sys
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.graph.workflow import run_workflow, stream_workflow
from src.utils.helpers import (
    validate_input,
    print_result,
    create_sample_inputs,
)


def main():
    """Main function to run the workflow"""
    parser = argparse.ArgumentParser(
        description="LangGraph Text Analysis Workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with a sample text
  python main.py --sample 0
  
  # Run with custom text
  python main.py --text "Your text here..."
  
  # Run with a different model
  python main.py --sample 0 --model llama3.2
  
  # Output as JSON
  python main.py --sample 1 --format json
  
  # Stream mode
  python main.py --sample 0 --stream
        """,
    )

    parser.add_argument("--text", type=str, help="Input text to analyze")

    parser.add_argument(
        "--sample", type=int, choices=[0, 1, 2, 3, 4], help="Use a sample input (0-4)"
    )

    parser.add_argument(
        "--model",
        type=str,
        default="llama3.2:1b",
        help="Ollama model to use (default: llama3.2:1b)",
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format (default: text)",
    )

    parser.add_argument(
        "--stream", action="store_true", help="Stream the workflow execution"
    )

    parser.add_argument(
        "--thread-id", type=str, help="Thread ID for persistent conversations"
    )

    args = parser.parse_args()

    # Determine input text
    if args.sample is not None:
        samples = create_sample_inputs()
        input_text = samples[args.sample]
        print(f"\n📝 Using sample input #{args.sample}")
        print(f"Preview: {input_text[:100]}...\n")
    elif args.text:
        input_text = args.text
    else:
        # Interactive mode
        print("\n" + "=" * 70)
        print("LangGraph Text Analysis Workflow")
        print("=" * 70)
        print(
            "\nNo input provided. Enter your text (press Ctrl+D or Ctrl+Z when done):\n"
        )

        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass

        input_text = "\n".join(lines)

    # Validate input
    is_valid, error = validate_input(input_text)
    if not is_valid:
        print(f"\n❌ Error: {error}\n")
        return 1

    # Run workflow
    try:
        if args.stream:
            # Stream mode
            print("\n🔄 Streaming workflow execution...\n")
            for update in stream_workflow(
                input_text=input_text, model_name=args.model, thread_id=args.thread_id
            ):
                print(f"\n📦 Update: {update}")
        else:
            # Standard mode
            print(f"\n🚀 Running workflow with model: {args.model}\n")
            result = run_workflow(
                input_text=input_text, model_name=args.model, thread_id=args.thread_id
            )

            # Display results
            print_result(result, format_type=args.format)

        print("\n✅ Workflow completed successfully!\n")
        return 0

    except (ValueError, TypeError, RuntimeError, ConnectionError) as e:
        print(f"\n❌ Error: {str(e)}\n")
        import traceback

        traceback.print_exc()
        return 1


def run_demo():
    """Run a quick demo with a sample text"""
    print("\n" + "=" * 70)
    print("LangGraph Text Analysis Workflow - Demo Mode")
    print("=" * 70)

    samples = create_sample_inputs()

    print("\n📝 Running demo with sample text about AI...\n")
    print(f"Input: {samples[0][:100]}...\n")

    try:
        result = run_workflow(
            input_text=samples[0], model_name="llama3.2:1b", thread_id="demo"
        )

        print_result(result)

        print("\n✅ Demo completed successfully!")
        print("\nTry running with different samples:")
        for i, sample in enumerate(samples):
            print(f"  python main.py --sample {i}  # {sample[:50]}...")

    except (ValueError, TypeError, RuntimeError, ConnectionError) as e:
        print(f"\n❌ Error: {str(e)}\n")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # If no arguments provided, run demo
    if len(sys.argv) == 1:
        run_demo()
    else:
        sys.exit(main())
