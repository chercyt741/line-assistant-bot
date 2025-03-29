import os
import json

input_folder = 'funeral_articles'
output_folder = 'funeral_ariticles.json'

data = []

for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as f:
            content = f.read()
        
        title = filename.replace('.txt', '').replace('_', '/')

        entry = {
            'title': title,
            'content': content,
            'category': 'funeral',
        }
        data.append(entry)

with open(output_folder, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"已轉換 {len(data)} 筆資料, 存於 {output_folder}")