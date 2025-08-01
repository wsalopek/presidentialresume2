import os
import json
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_resume(member):
    name = member.get('name', 'Unknown')
    bio = f"Generate a professional political resume for {name}. Include contact, education, experience, legislative focus, committees, and any public statements."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a political analyst creating resumes for politicians."},
            {"role": "user", "content": bio}
        ],
        temperature=0.7,
        max_tokens=800
    )

    return response['choices'][0]['message']['content']

def process_members(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        members = json.load(f)

    os.makedirs(output_path, exist_ok=True)

    for member in members:
        try:
            name_slug = member['name'].replace(' ', '_').replace('.', '').lower()
            resume_text = generate_resume(member)
            with open(os.path.join(output_path, f"{name_slug}.txt"), 'w', encoding='utf-8') as f_out:
                f_out.write(resume_text)
            print(f"✅ Generated resume for {member['name']}")
        except Exception as e:
            print(f"❌ Error for {member.get('name', 'Unknown')}: {e}")

def main():
    process_members('data/house_members.json', 'data/house_resumes')
    process_members('data/senate_members.json', 'data/senate_resumes')

if __name__ == "__main__":
    main()
