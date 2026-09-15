import os
import time
import re

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None

# Attempt to configure Gemini using the GEMINI_API_KEY environment variable.
API_KEY = os.environ.get("GEMINI_API_KEY")
client = None

if API_KEY and genai:
    client = genai.Client(api_key=API_KEY)
    try:
        # Dynamically discover a working flash model 
        available = [m.name for m in client.models.list()]
        
        # Look for standard numbered flash models (e.g., gemini-3.8-flash)
        # Avoid previews, lites, audio, omni, etc which might not have free tier
        valid_models = []
        for m in available:
            match = re.search(r'gemini-(\d+)\.(\d+)-flash$', m)
            if match:
                major, minor = int(match.group(1)), int(match.group(2))
                valid_models.append((major, minor, m))
                
        if valid_models:
            valid_models.sort(key=lambda x: (x[0], x[1]))
            MODEL_NAME = valid_models[-1][2].replace('models/', '')
        else:
            MODEL_NAME = "gemini-3.5-flash" # Safe fallback
    except Exception as e:
        MODEL_NAME = "gemini-3.5-flash"
else:
    MODEL_NAME = "gemini-3.5-flash"

last_call_time = 0.0

# Keywords for Stage 1 Pre-filtering
AUTO_KEEP_WORDS = [
    "engineer", "engineering", "developer", "technician", "mechanic", 
    "software", "hardware", "data", "avionics", "propulsion", "it ", 
    "systems", "technical", "backend", "frontend", "fullstack", "devops",
    "infrastructure", "aerospace"
]

AUTO_REJECT_WORDS = [
    " hr ", "human resources", "marketing", "sales", "recruiter", 
    "accountant", "legal", "finance", "buyer", "purchasing", "talent",
    "counsel", "tax", "facility", "business partner", "communications",
    "event ", "payroll"
]

def is_job_relevant(job_title: str) -> bool:
    """
    Evaluates a job title using a Two-Stage Filter:
    1. Keyword matching for obvious technical/non-technical roles.
    2. Gemini API for ambiguous roles.
    Returns True if the job should be kept.
    Returns False if it is definitively non-technical.
    """
    global last_call_time
    
    title_lower = job_title.lower()
    
    # STAGE 1: LOCAL PRE-FILTER
    for word in AUTO_KEEP_WORDS:
        if word in title_lower:
            # print(f"  [Pre-Filter] Auto-keeping: '{job_title}'")
            return True
            
    for word in AUTO_REJECT_WORDS:
        if word in title_lower:
            print(f"  [Pre-Filter] Auto-rejecting (Non-Technical): '{job_title}'")
            return False

    # STAGE 2: AI FILTER (for ambiguous jobs)
    if not client:
        return True # Default to keep if AI is not configured
        
    prompt = f"Job Title: {job_title}\n\nIs this relevant? Reply YES or NO."
    
    # Rate limit check: 5 RPM means 1 request every 12 seconds. We use 13s to be safe.
    now = time.time()
    elapsed = now - last_call_time
    if elapsed < 13.0:
        time.sleep(13.0 - elapsed)
        
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are a job filtering assistant. Your task is to evaluate a job title (and description, if available). "
                    "You MUST return 'YES' to keep the job, UNLESS the job is definitively non-technical. "
                    "ONLY return 'NO' if the job is strictly in domains like: Human Resources (HR), Marketing, Sales, "
                    "Legal, Finance, Accounting, Talent Acquisition, or Facility Management. "
                    "If the job is an engineering, technical, software, hardware, IT, data, or product role, return 'YES'. "
                    "If you are unsure or if the title is ambiguous, ALWAYS return 'YES'. "
                    "Reply strictly with 'YES' or 'NO'."
                )
            )
        )
        last_call_time = time.time()
        
        if not response or not response.text:
            return True
            
        answer = response.text.strip().upper()
        
        # Safe check: Only filter out if "NO" is firmly in the response and not "YES"
        if "NO" in answer and "YES" not in answer:
            print(f"  [AI Filter] Job '{job_title}' filtered out (Not technical).")
            return False
            
        return True
    except Exception as e:
        print(f"  [AI Filter] Warning: API check failed for job '{job_title}': {e}. Keeping job by default.")
        # Default to keeping the job if the API call fails or times out
        return True
