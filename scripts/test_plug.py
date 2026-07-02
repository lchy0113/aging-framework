# Backward-compatible wrapper.
# New code should use scripts/test_power.py.

from test_power import main

from dotenv import load_dotenv

# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------
load_dotenv("config/.env")

if __name__ == "__main__":
    main()
