import anthropic
import csv
from config import ANTHROPIC_API_KEY
import os

def get_claude_response(prompt: str) -> str:
    """
    Send a prompt to Claude and get the response
    
    Args:
        prompt (str): The input prompt to send to Claude
        
    Returns:
        str: Claude's response
    """
    try:
        # Initialize the Anthropic client
        client = anthropic.Anthropic(
            api_key=ANTHROPIC_API_KEY
        )

        # Send message to Claude
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return message.content[0].text
        
    except Exception as e:
        return f"Error occurred: {str(e)}"

def process_csv(input_file, output_file=None):
    """
    Process a CSV file row by row, send each row as a prompt to Claude, 
    and save the responses
    
    Args:
        input_file (str): Path to the input CSV file
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
    
    # Process each row
    for i, row in enumerate(rows):
        # Assume the prompt is in the first column - adjust this if needed
        prompt = row[0]
        print(f"Processing row {i+1}/{len(rows)}: {prompt[:50]}...")
        
        # Get response from Claude
        response = get_claude_response(prompt)
        
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
    
    # Process the CSV file (will modify the original file)
    process_csv(input_csv)

if __name__ == "__main__":
    main()