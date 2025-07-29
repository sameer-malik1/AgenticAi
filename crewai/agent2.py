from crewai.flow.flow import Flow, start, listen
from litellm import completion
import logging
from dotenv import load_dotenv
import os

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class BasicFlow(Flow):
    def __init__(self):
        super().__init__()
        # Manually add the start method name (string) if it's not registered
        if not self._start_methods:
            print("Manually registering start method")
            self._start_methods = ['generate_random_city']  # Use method name as string
            # Also ensure the method is in _methods dict
            if 'generate_random_city' not in self._methods:
                self._methods['generate_random_city'] = self.generate_random_city
    
    def generate_random_city(self):
        try:
            print("=== GENERATE_RANDOM_CITY EXECUTING ===")
            logger.info("Starting generate_random_city")
            
            result = completion(
                model="gemini/gemini-2.5-flash",
                api_key=GOOGLE_API_KEY,
                messages=[{"content": "Return any random city name only","role":"user"}]
            )
            
            city = result['choices'][0]['message']['content'].strip()
            print(f"Generated city: {city}")
            logger.info(f"Generated city: {city}")
            
            return city
            
        except Exception as e:
            logger.error(f"Error in generate_random_city: {str(e)}")
            print(f"Error: {str(e)}")
            return "DefaultCity"

    @listen(generate_random_city)
    def process_city(self, city):
        print(f"=== PROCESS_CITY EXECUTING with: {city} ===")
        logger.info(f"Processing city: {city}")
        return f"Processed: {city}"

def kickoff():
    try:
        logger.info("Starting flow...")
        obj = BasicFlow()
        
        print(f"Start methods registered: {len(obj._start_methods)}")
        if obj._start_methods:
            print(f"Start method names: {[method.__name__ if hasattr(method, '__name__') else str(method) for method in obj._start_methods]}")
        
        result = obj.kickoff()
        
        print(f"Final result: {result}")
        print(f"Method outputs: {obj.method_outputs}")
        
        logger.info("Flow completed")
        
    except Exception as e:
        logger.error(f"Flow failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    kickoff()