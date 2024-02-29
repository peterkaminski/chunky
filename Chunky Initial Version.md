# Chunky Initial Version

The first proof-of-concept version of Chunky was created on on 2024-02-29 by Peter Kaminski and Jordan Sukut as a small automation tool for the Lionsberg Wiki Book publishing project, .

The prompt developed through several iterations. The final iteration for the first version of Chunky:

---

Write a python script to take a long text file as input. Chunk the file into about 1000-word segments, which break on paragraph breaks (two newlines).

Then, we'll use the OpenAI API chat completions API endpoint, via direct REST calls rather than the `openai` module. Assume GPT-4. Assume the API key is in the OPENAI_API_KEY environment variable.

For each segment, send a command to the OpenAI chat completion API endpoint, with a short, configurable chat prompt such as "Check the following passage for typos, spelling errors, duplicated words, etc.", and then send the segment after the prompt. Accumulate the returned text as new segments to write to the output file.

Use "-p" to specify the prompt.

Use argparse, and use -i to specify the input file, and optionally, -o to specify an output file. Use a shebang line, a main() function, and add logging for errors and information messages.

---

One key decision by Pete was to use the direct REST call rather than the `openai` module, which ChatGPT assumed we'd want to use in a previous iteration. The chat completion call is so simple it's easy to do it directly, and saves coding overhead and maintenance involved in using the `openai` module.