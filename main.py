from dotenv import load_dotenv
import os
import openai

#Load env var from api.env
load_dotenv('api.env')
api_key = os.getenv('OPENAI_API_KEY')

#OpenAI API key
openai.api_key = api_key

# Function to gather and clarify user input
def get_user_request():
    while True:
        user_request = input("Please describe what you want (or type 'quit' to exit): ")
        
        if user_request.lower() == 'quit':
            print("Exiting...")
            exit()  # This will quit the program
        
        clarification_needed = True
        while clarification_needed:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[
                    {"role": "system", "content": "You are an assistant helping to clarify a request."},
                    {"role": "user", "content": f"The user wants: {user_request}. Is this request clear enough? If not, ask for clarification."},
                ]
            )
            clarification = response['choices'][0]['message']['content']
            
            if "clear enough" in clarification.lower():
                clarification_needed = False
            else:
                user_input = input("I have asked for more clarification, but you can type 'proceed' to continue without further questions, or 'quit' to exit: ")
                if user_input.lower() == 'proceed':
                    clarification_needed = False
                    break  # Exit the clarification loop and proceed
                elif user_input.lower() == 'quit':
                    print("Exiting...")
                    exit()
                else:
                    user_request += " " + user_input
        
        return user_request


# Function to generate instructions and outline
def generate_instructions(user_request):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are an expert planner."},
            {"role": "user", "content": f"Based on the request '{user_request}', create a detailed plan. Include an outline, number of parts needed, and clear instructions for each part."},
        ]
    )
    instructions = response['choices'][0]['message']['content']
    return instructions

# Function to execute the tasks recursively
def execute_recursive_tasks(instructions):
    parts = instructions.split("Part")
    results = []
    
    for i in range(1, len(parts)):
        part_instruction = f"Part {i}" + parts[i]
        result = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are an expert executor."},
                {"role": "user", "content": part_instruction},
            ]
        )
        results.append(result['choices'][0]['message']['content'])
    
    return results

# Function to save the output to a text file
def save_to_text_file(content, filename="output.txt"):
    try:
        print("Attempting to save content to file...")
        with open(filename, "w") as file:
            file.write(content)
        print("Content saved successfully to", filename)
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

def main():
    try:
        # Step 1: Get and clarify user request
        user_request = get_user_request()
        
        # Step 2: Generate instructions based on the request
        instructions = generate_instructions(user_request)
        print("Generated Instructions: ", instructions)  # Debugging line
        
        # Step 3: Execute the tasks recursively based on the instructions
        results = execute_recursive_tasks(instructions)
        
        # Combine all parts and instructions
        final_output = instructions + "\n\n" + "\n\n".join(results)
        
        # Step 4: Save the output to a text file
        print("Saving the output to a text file...")
        save_to_text_file(final_output)
    except Exception as e:
        print(f"An error occurred during the process: {e}")

if __name__ == "__main__":
    main()
