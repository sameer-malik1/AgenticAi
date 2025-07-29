from crewai.flow.flow import Flow, start, listen
from litellm import completion
import time
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging to show output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class BasicFlow(Flow):
    @start()
    def generate_random_city(self):
        try:
            logger.info("Starting generate_random_city")
            print("DEBUG: About to make API call")
            
            result = completion(
                model="gemini/gemini-2.5-flash",
                api_key=GOOGLE_API_KEY,
                messages=[{"content": "Return any random city","role":"user"}]
            )
            
            print(f"DEBUG: Full API result: {result}")
            city = result['choices'][0]['message']['content']
            logger.info(f"Generated city: {city}")
            print(f"PRINT: Generated city: {city}")
            print(f"DEBUG: About to return city: {city}")
            return city  # This was commented out - it's essential!
        except Exception as e:
            logger.error(f"Error in generate_random_city: {str(e)}")
            print(f"DEBUG: Exception occurred: {str(e)}")
            raise

    @listen(generate_random_city)
    def func2(self, city):
        print(f"DEBUG: func2 called with city: {city}")
        logger.info(f"step 2 - Received city: {city}")
        time.sleep(3)
        processed = f"Processed: {city}"
        print(f"DEBUG: func2 returning: {processed}")
        return processed
    
    @listen(func2)
    def func3(self, processed_data):
        print(f"DEBUG: func3 called with data: {processed_data}")
        logger.info(f"step 3 - Received processed data: {processed_data}")
        return f"Final: {processed_data}"

def kickoff():
    try:
        logger.info("Starting flow...")
        obj = BasicFlow()
        obj.kickoff()
        logger.info("Flow completed")
    except Exception as e:
        logger.error(f"Flow failed: {str(e)}")

if __name__ == "__main__":
    kickoff()