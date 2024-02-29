#!/usr/bin/env python3

import argparse
import os
import logging
import requests
import re

def chunk_file(input_file, word_limit=100):
    """
    Chunk the input file into segments of approximately `word_limit` words, 
    breaking on paragraph breaks (two newlines).
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    paragraphs = content.split('\n\n')
    chunks = []
    current_chunk = []

    current_word_count = 0
    for paragraph in paragraphs:
        paragraph_word_count = len(re.findall(r'\w+', paragraph))
        if current_word_count + paragraph_word_count > word_limit:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [paragraph]
            current_word_count = paragraph_word_count
        else:
            current_chunk.append(paragraph)
            current_word_count += paragraph_word_count

    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))

    return chunks

def call_openai_api(text, prompt):
    """
    Call the OpenAI API to process the text with the given prompt.
    """
    api_key = os.environ.get('OPENAI_API_KEY')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "system", "content": "Please complete the following task:"},
                     {"role": "user", "content": f"{prompt}\n\n{text}"}]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        logging.error(f"API call failed with status code {response.status_code}: {response.text}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Chunk text and check with OpenAI API.")
    parser.add_argument("-i", "--input", required=True, help="Input file path")
    parser.add_argument("-o", "--output", help="Output file path", default="output.txt")
    parser.add_argument("-p", "--prompt", help="Prompt for the API call", 
                        default="Check the following passage for typos, spelling errors, duplicated words, etc.")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    chunks = chunk_file(args.input)
    logging.info(f"Total chunks created: {len(chunks)}")

    with open(args.output, 'w', encoding='utf-8') as output_file:
        for i, chunk in enumerate(chunks, start=1):
            logging.info(f"Processing chunk {i}/{len(chunks)}")
            response_text = call_openai_api(chunk, args.prompt)
            if response_text:
                output_file.write(response_text + "\n\n")
            else:
                logging.error("Failed to process chunk due to API error.")

if __name__ == "__main__":
    main()
