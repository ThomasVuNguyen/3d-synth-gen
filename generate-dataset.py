import openai
import time
from credentials import RIFT_API_KEY

client = openai.OpenAI(
  api_key=RIFT_API_KEY,
  base_url="https://inference.cloudrift.ai/v1"
)

def make_api_request():
    return client.chat.completions.create(
        model="Qwen/Qwen3-Next-80B-A3B-Thinking",
        messages=[
            {"role": "user", "content": "Create a complete Three.js scene with a 3D duck using only basic Three.js geometries (no external models). Requirements:\n\n1. Use ONLY ```javascript code blocks\n2. Create duck using basic shapes: spheres, cones, cylinders\n3. Include: scene, camera, renderer, lighting, materials, and smooth animation\n4. Add orbit controls for user interaction\n5. Make duck waddle/walk animation, not just rotation\n6. Use proper colors: yellow body, orange beak, black eyes\n7. Include error handling and resize functionality\n8. Ensure code is complete and runnable\n9. Add comments explaining each part\n10. Make it visually appealing with good lighting and materials\n\nProvide ONLY the JavaScript code, no HTML structure."}
        ]
    )

# Retry mechanism
max_retries = 3
retry_delay = 1  # seconds

for attempt in range(max_retries):
    try:
        print(f"Attempt {attempt + 1}/{max_retries}")
        completion = make_api_request()
        response_content = completion.choices[0].message.content
        
        if response_content is not None:
            print("API request successful!")
            break
        else:
            print(f"API returned None on attempt {attempt + 1}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print("All retry attempts failed")
                exit(1)
                
    except Exception as e:
        print(f"Error on attempt {attempt + 1}: {e}")
        if attempt < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2
        else:
            print("All retry attempts failed")
            exit(1)

print(f"Response content type: {type(response_content)}")
print(f"Response content: {response_content}")

# Check if response is None or empty
if response_content is None:
    print("ERROR: API returned None response")
    exit(1)

# Extract code blocks from the response
import re

# Find all code blocks (both ``` and ```javascript, ```html, etc.)
code_blocks = re.findall(r'```(?:javascript|html|css|js|html)?\n?(.*?)```', response_content, re.DOTALL)

print(f"Found {len(code_blocks)} code blocks")
print("Code blocks:", code_blocks)

if code_blocks:
    # Join all code blocks
    code_content = '\n\n'.join(code_blocks)
    
    # Create HTML file with the code
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3JS Duck Code</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: #000;
            color: #fff;
            font-family: Arial, sans-serif;
        }}
        #container {{
            width: 100%;
            height: 100vh;
        }}
        pre {{
            background: #1a1a1a;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <h1>3JS Duck Code</h1>
    <div id="container"></div>
    <pre><code>{code_content}</code></pre>
    
    <script>
        {code_content}
    </script>
</body>
</html>"""
    
    with open('duck_3js.html', 'w') as f:
        f.write(html_content)
    
    print("Code extracted and saved to duck_3js.html")
    print("Code content:")
    print(code_content)
else:
    print("No code blocks found in response")
    print("Full response:")
    print(response_content)