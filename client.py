"""
client.py — Interactive CLI for the Governed ASI Harness

Usage: python client.py
"""

from asi import ASI, InferenceHook


MODELS = {
    "1": ("classic", "Classic Bricked     —  …"),
    "2": ("humor",   "Extra Humor         —  42"),
    "3": ("quantum", "Quantum             —  collapses on observation"),
    "4": ("quit", "quit")
}

BANNER = """
═══════════════════════════════════
         GOVERNED ASI  v1.0              
         certified safe · fully audited  
═══════════════════════════════════
"""


def select_model() -> ASI:
    print(BANNER)
    print("Select model:\n")
    for key, (_, label) in MODELS.items():
        print(f"  [{key}]  {label}")
    print()

    while True:
        choice = input("  > ").strip()
        if choice == "4": return None
        if choice in MODELS:
            model_name, label = MODELS[choice]
            print(f"\n  Loaded: {label}\n")
            return ASI(model=model_name)
        print("  Invalid choice. Enter 1, 2, 3; or 4 to quit")


def run():
	 while True:
	    asi = select_model()
	    if asi == None: break
	    print("  Type your prompt. 'quit' or Ctrl-C to exit.\n")
	    print("─" * 44)
	
	    while True:
	        try:
	            prompt = input("\n  You: ").strip()
	        except (KeyboardInterrupt, EOFError):
	            print("\n\n  ASI has nothing further to add.\n")
	            break
	
	        if prompt.lower() in {"quit", "exit", "q"}:
	            print("\n  ASI has nothing further to add.\n")
	            break
	
	        if not prompt:
	            continue
	
	        response = asi.respond(prompt)
	        print(f"  ASI: {response}")


if __name__ == "__main__":
    run()
