import anthropic
import csv
from config import ANTHROPIC_API_KEY
import os

def get_claude_response(prompt: str, system_prompt: str = None) -> str:
    """
    Send a prompt to Claude and get the response
    
    Args:
        prompt (str): The input prompt to send to Claude
        system_prompt (str, optional): System prompt to guide Claude's behavior
        
    Returns:
        str: Claude's response
    """
    try:
        # Initialize the Anthropic client
        client = anthropic.Anthropic(
            api_key=ANTHROPIC_API_KEY
        )

        # Prepare message parameters
        message_params = {
            "model": "claude-3-5-haiku-20241022",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        # Add system prompt if provided
        if system_prompt:
            message_params["system"] = system_prompt
            
        # Send message to Claude
        message = client.messages.create(**message_params)
        
        return message.content[0].text
        
    except Exception as e:
        return f"Error occurred: {str(e)}"

def process_csv(input_file, prompt_index=None, system_prompt=None, output_file=None):
    """
    Process a CSV file row by row, send each row as a prompt to Claude, 
    and save the responses
    
    Args:
        input_file (str): Path to the input CSV file
        prompt_index (int, optional): Index of the specific prompt to process
        system_prompt (str, optional): System prompt to use for all requests
        output_file (str, optional): Path for the output CSV. If None, will modify the input file.
    """
    if output_file is None:
        output_file = input_file  # Write back to the same file
    
    # Read the entire CSV into memory
    with open(input_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Get the header
        
        # Add a 'response' column if it doesn't exist
        if 'response' not in header:
            header.append('response')
            
        rows = list(csv_reader)  # Read all rows
    
    # Process specific prompt if index is provided
    if prompt_index is not None:
        if 0 <= prompt_index < len(rows):
            row = rows[prompt_index]
            prompt = row[0]
            print(f"Processing prompt {prompt_index + 1}: {prompt[:50]}...")
            
            # Get response from Claude
            response = get_claude_response(prompt, system_prompt)
            
            # Make sure the row has enough columns
            while len(row) < len(header):
                row.append("")
                
            # Add the response to the last column
            row[header.index('response')] = response
            print(f"Processed prompt {prompt_index + 1} successfully.")
        else:
            print(f"Error: Prompt index {prompt_index} is out of range (0-{len(rows)-1}).")
            return
    else:
        # Process each row
        for i, row in enumerate(rows):
            prompt = row[0]
            print(f"Processing row {i+1}/{len(rows)}: {prompt[:50]}...")
            
            # Get response from Claude
            response = get_claude_response(prompt, system_prompt)
            
            # Make sure the row has enough columns
            while len(row) < len(header):
                row.append("")
                
            # Add the response to the last column
            row[header.index('response')] = response
    
    # Write the results back to the CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)
        csv_writer.writerows(rows)
    
    print(f"Processing complete. Results saved to {output_file}")

def main():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create absolute path to the CSV file
    input_csv = os.path.join(script_dir, "prompts.csv")
    
    # You can set a specific prompt index to process (0-based)
    # Set to None to process all prompts
    prompt_index = 2  # Example: Process the 3rd prompt
    
    # Optional: Add a system prompt to guide Claude's behavior
    system_prompt = "You are an assistant specialized in technical writing. Keep responses concise and informative."
    
    # Process the CSV file with the specified prompt index
    process_csv(input_csv, prompt_index=prompt_index, system_prompt=system_prompt)

if __name__ == "__main__":
    main()