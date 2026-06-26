from supabase import create_client, Client
from app.config import settings

# Initialize the Supabase client
# We use this client to execute queries against our PostgreSQL database
try:
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
except Exception as e:
    print(f"Failed to initialize Supabase client: {e}")
    supabase = None # Allow app to start even if supabase isn't configured for MVP testing