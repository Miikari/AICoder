import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # TEST FOR AI AGENT 
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    client = genai.Client(api_key=api_key)
    for i in range(20):
     
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            )
        )
        metadata = response.usage_metadata
        if not metadata.prompt_token_count or not metadata.candidates_token_count:
            raise RuntimeError("Failed API request, no token metadata found")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {metadata.prompt_token_count}")
            print(f"Response tokens: {metadata.candidates_token_count}")
        
        if(response.candidates):
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)
        else:
            print("No candidates found")
        if response.function_calls:
            function_responses = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)
                if not function_call_result.parts:
                    raise Exception("Error: empty function list returned")
                if not function_call_result.parts[0].function_response:
                    raise Exception("Error: empty cell in the function list returned")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Error: empty response in the function list cell returned")
                
                function_result = function_call_result.parts[0]

        #        if args.verbose:
        #            print(f"-> {function_call_result.parts[0].function_response.response}")

                function_responses.append(function_result)          
            
            messages.append(types.Content(role="user", parts=function_responses))

        else:
            print(response.text)
            return
    print("No responses found!")
    sys.exit(1)

                


if __name__ == "__main__":
    main()
