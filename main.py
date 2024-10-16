from dotenv import load_dotenv
import os
import openai

#Load env variable from api.env
load_dotenv('api.env')
api_key = os.getenv('OPENAI_API_KEY')

#Setting OpenAI API key
openai.api_key = api_key

def get_user_request():
    user_request = input("Please describe what you want to write about ('quit' to exit): ")
    if user_request.lower() == 'quit':
        print("Exiting...")
        exit()
    return user_request

def clarify_request(initial_request):
    clarification_needed = True
    conversation_history = []
    
    while clarification_needed:
        messages = [
            {"role": "system", "content": "You are an assistant helping to clarify a request about a novel."},
            {"role": "user", "content": f"The user wants: {initial_request}. Decide if you need more details, and ask questions if you do."}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=messages
        )
        clarification = response['choices'][0]['message']['content'].strip()
        
        if "enough info" in clarification.lower():
            clarification_needed = False
        else:
            print(f"Clarification needed: {clarification}")
            user_input = input("Please clarify further (or type 'proceed' to continue): ")
            
            if user_input.lower() == 'proceed':
                clarification_needed = False
            else:
                conversation_history.append({"question": clarification, "answer": user_input})
                initial_request += " " + user_input
    
    return initial_request, conversation_history

def summarize_request(conversation_history, initial_request2):
    #Format conversation history as a readable string for AI to read
    conversation_str = ""
    for entry in conversation_history:
        conversation_str += f"Q: {entry['question']}\nA: {entry['answer']}\n"

    messages = [
        {"role": "system", "content": "You are summarizing the key information from a conversation about a novel."},
        {"role": "user", "content": f"Here is the conversation history:\n\n{initial_request2} {conversation_str}\n\nPlease summarize the " +
         "key details, such as themes, characters, setting, genre, etc. If there is not enough information, use any provided " + 
         "information and use your creativity to make up the rest."}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages
    )
    summary = response['choices'][0]['message']['content'].strip()
    
    return summary




def plan_task(summary):
    messages = [
        {"role": "system", "content": "Your job is to split a novel outline into clear, actionable sub-tasks."},
        {"role": "user", "content": f"The request: {summary}. \n This request has all the information needed to be completed. " + 
         "Delegate tasks to as many people as needed. Try to use the minimum needed for the job, depending on length of the novel. Each person should be assigned a chapter, act, etc. " +
          "An example of a task assigned to a person should be like this: 'Write the 4th chapter of a book about BLANK. The main characters are BLANK and BLANK. So far, BLANK has happened. " +
          "It has themes of BLANK and BLANK, genre of BLANK. You must write BLANK amount of words.' The most each person can write " +
          "is 2500 words. Do not assign the task of brainstormer, editor, reviewer, etc. to people - only assign them to write " + 
          "a specific section of the text. Make sure the word counts of all people combined are equivalent to the total requested wordcount."}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages
    )
    
    task_plan = response['choices'][0]['message']['content'].strip().split("\n")
    task_plan = [task.strip() for task in task_plan if task.strip()]
    
    print("Task:", task_plan)
    
    return task_plan


def execute_tasks(task_plan):
    results = []
    
    for i, task in enumerate(task_plan):
        #Create a clear task for each AI instance
        messages = [
            {"role": "system", "content": "You are an AI assigned to write a specific part of a novel. Focus ONLY on the task assigned to you."},
            {"role": "user", "content": f"Task {i+1}:\n{task}"}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=messages
        )
        result = response['choices'][0]['message']['content'].strip()
        results.append(result)
    
    return results



def save_to_text_file(content, filename="output.txt"):
    try:
        print("Attempting to save content to file...")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        print("Content saved successfully to", filename)
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")


def main():
    try:
        #Get the user request
        user_request = get_user_request()

        #Clarify the user request (if needed)
        clarified_request, conversation_history = clarify_request(user_request)
        
        #Summarize the conversation into a clear task
        summary = summarize_request(conversation_history, user_request)
        
        #Plan the task into manageable parts
        task_plan = plan_task(summary)
        
        #Execute each task and collect results
        results = execute_tasks(task_plan)
        
        #Save the final content to a text file
        full_content = "\n".join(results)
        save_to_text_file(full_content)

    except Exception as e:
        print(f"An error occurred during the process: {e}")

if __name__ == "__main__":
    main()
