import os
from supabase import create_client, Client
from dotenv import load_dotenv
from utils.config_loader import load_config

# Load environment variables
load_dotenv()

# Load YAML config
config = load_config()
SUPABASE_URL = config["supabase"]["url"]
SUPABASE_BUCKET_NAME = config["supabase"]["bucket_name"]
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, SUPABASE_BUCKET_NAME]):
    raise ValueError("Missing Supabase configuration values.")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
