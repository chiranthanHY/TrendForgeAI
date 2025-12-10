import sys
import os
import subprocess

def run_module(module_name):
    """Runs a python module using -m to ensure imports work correctly."""
    print(f"\n--- Launching {module_name} ---\n")
    try:
        # Run the module from the current directory (project root)
        subprocess.run([sys.executable, "-m", module_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nError: {module_name} failed with exit code {e.returncode}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

def main():
    while True:
        print("\n" + "="*40)
        print("   TrendForgeAI - Control Panel")
        print("="*40)
        print("1. [Extractor] LinkedIn Data")
        print("2. [Extractor] YouTube Data")
        print("3. [Extractor] Twitter Data")
        print("4. [Extractor] Google Trends Data")
        print("-" * 40)
        print("5. [Engine]    Run Data Curator (Prepare Dataset)")
        print("6. [Engine]    Run Content Engine (Generate Content)")
        print("-" * 40)
        print("0. Exit")
        print("="*40)
        
        choice = input("\nSelect an option (0-6): ").strip()
        
        if choice == '1':
            run_module("src.extractors.linkedin_data_extractor")
        elif choice == '2':
            run_module("src.extractors.youtube_data_extractor")
        elif choice == '3':
            run_module("src.extractors.twitter_data_extractor")
        elif choice == '4':
            run_module("src.extractors.google_trends_extract")
        elif choice == '5':
            run_module("src.engine.data_curator")
        elif choice == '6':
            run_module("src.engine.content_engine")
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    # Ensure we are running from the project root
    if not os.path.exists("src"):
        print("Error: Please run this script from the project root directory (TrendForgeAI).")
    else:
        main()
