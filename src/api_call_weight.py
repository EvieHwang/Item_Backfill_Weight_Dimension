import anthropic
import csv
import json
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

def load_prompt_template(template_file):
    """
    Load the prompt template from a JSON file
    
    Args:
        template_file (str): Path to the JSON file containing the prompt template
        
    Returns:
        dict: The prompt template as a dictionary
    """
    with open(template_file, 'r', encoding='utf-8') as file:
        template = json.load(file)
    return template

def create_product_prompt(prompt_template, product_data):
    """
    Create a prompt for a specific product by inserting product data into the template
    
    Args:
        prompt_template (dict): The prompt template
        product_data (dict): The product data to insert into the template
        
    Returns:
        str: The complete prompt for Claude
    """
    # Extract components from the template
    instructions = prompt_template["instructions"]
    descriptions = prompt_template["descriptions"]
    examples = prompt_template["examples"]
    input_format = prompt_template["input_format"]
    output_format = prompt_template["output_format"]
    
    # Create the prompt text
    prompt = f"""
Instructions:
{json.dumps(instructions, indent=2)}

Descriptions:
{json.dumps(descriptions, indent=2)}

Input Format:
{json.dumps(input_format, indent=2)}

Output Format:
{json.dumps(output_format, indent=2)}

Here are some examples:
{json.dumps(examples, indent=2)}

Now predict for this product:
{json.dumps(product_data, indent=2)}
"""
    
    return prompt

def process_csv(input_file, prompt_template_file, prompt_index=None, output_file=None):
    """
    Process a CSV file row by row, create a prompt for each product,
    send to Claude, and save the responses
    
    Args:
        input_file (str): Path to the input CSV file with product data
        prompt_template_file (str): Path to the JSON file with the prompt template
        prompt_index (int, optional): Index of the specific prompt to process
        output_file (str, optional): Path for the output CSV. If None, will modify the input file.
    """
    if output_file is None:
        output_file = input_file  # Write back to the same file
    
    # Load the prompt template
    prompt_template = load_prompt_template(prompt_template_file)
    system_prompt = prompt_template["system"]
    
    # Read the product data from CSV
    with open(input_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)  # Read all rows as dictionaries
    
    # Prepare the header for the output CSV
    header = list(rows[0].keys()) if rows else []
    if 'response' not in header:
        header.append('response')
    
    # Process specific product if index is provided
    if prompt_index is not None:
        if 0 <= prompt_index < len(rows):
            product_data = rows[prompt_index]
            print(f"Processing product {prompt_index + 1}: {product_data.get('name', '')}...")
            
            # Create prompt for this product
            prompt = create_product_prompt(prompt_template, product_data)
            
            # Get response from Claude
            response = get_claude_response(prompt, system_prompt)
            
            # Add the response
            rows[prompt_index]['response'] = response
            print(f"Processed product {prompt_index + 1} successfully.")
        else:
            print(f"Error: Product index {prompt_index} is out of range (0-{len(rows)-1}).")
            return
    else:
        # Process each product
        for i, product_data in enumerate(rows):
            print(f"Processing product {i+1}/{len(rows)}: {product_data.get('name', '')}...")
            
            # Create prompt for this product
            prompt = create_product_prompt(prompt_template, product_data)
            
            # Get response from Claude
            response = get_claude_response(prompt, system_prompt)
            
            # Add the response
            rows[i]['response'] = response
    
    # Write the results back to the CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.DictWriter(file, fieldnames=header)
        csv_writer.writeheader()
        csv_writer.writerows(rows)
    
    print(f"Processing complete. Results saved to {output_file}")

def main():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create absolute paths to the files
    input_csv = os.path.join(script_dir, "products.csv")
    prompt_template_file = os.path.join(script_dir, "prompt_template.json")
    
    # You can set a specific product index to process (0-based)
    # Set to None to process all products
    prompt_index = None
    
    # Process the CSV file with the specified product index
    process_csv(input_csv, prompt_template_file, prompt_index=prompt_index)

if __name__ == "__main__":
    main()