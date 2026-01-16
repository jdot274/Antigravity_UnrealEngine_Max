try:
    import google.generativeai as genai
    import PIL
    import requests
    print("✅ SUCCESS: .nexus_env is working! Google AI libs are importable.")
    print(f"PIL Version: {PIL.__version__}")
    print(f"Requests Version: {requests.__version__}")
except ImportError as e:
    print(f"❌ FAIL: Could not import dependencies. {e}")
