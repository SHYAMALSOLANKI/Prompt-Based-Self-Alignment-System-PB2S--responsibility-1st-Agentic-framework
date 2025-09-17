import os
import glob
import re
import json

# Knowledge storage directory
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), 'knowledge')
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

def extract_conversational_knowledge(md_text, filename=""):
    """
    Extract conversational knowledge from markdown for LLM-style learning.
    Focus on topics, concepts, questions, answers, and contextual understanding.
    """
    knowledge_items = []
    
    # Split into sections by headers
    sections = []
    current_section = {'title': '', 'content': '', 'level': 0}
    
    for line in md_text.splitlines():
        line = line.strip()
        if line.startswith('#'):
            # Save previous section
            if current_section['title'] or current_section['content']:
                sections.append(current_section)
            
            # Start new section
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('# ').strip()
            current_section = {'title': title, 'content': '', 'level': level}
        elif line:
            current_section['content'] += line + '\n'
    
    # Add final section
    if current_section['title'] or current_section['content']:
        sections.append(current_section)
    
    # Process sections into conversational knowledge
    for section in sections:
        if not section['title'] and not section['content'].strip():
            continue
            
        # Create knowledge item
        item = {
            'topic': section['title'] or f"Content from {filename}",
            'content': section['content'].strip(),
            'type': 'concept',
            'source': filename,
            'level': section['level']
        }
        
        # Extract additional context
        content = section['content']
        
        # Look for questions and answers
        if '?' in content:
            item['contains_questions'] = True
            
        # Look for equations or formulas
        if any(marker in content for marker in ['$$', '\\(', '\\[', '=', '+', '-', '*', '/']):
            item['type'] = 'technical'
            
        # Look for examples or analogies
        if any(word in content.lower() for word in ['example', 'like', 'similar', 'analogy', 'imagine']):
            item['has_examples'] = True
            
        # Look for definitions
        if any(word in content.lower() for word in ['is', 'are', 'means', 'refers to', 'defined as']):
            item['type'] = 'definition'
            
        knowledge_items.append(item)
    
    return knowledge_items

def import_markdown_folder(folder_path):
    """Import markdown knowledge for LLM-style conversational learning"""
    md_files = glob.glob(os.path.join(folder_path, '*.md'))
    skipped_files = []
    
    # Store comprehensive knowledge base
    knowledge_base = {
        'topics': {},           # topic -> detailed content
        'concepts': {},         # concept -> definition/explanation  
        'questions': {},        # question -> answer/context
        'examples': {},         # example -> context/explanation
        'definitions': {},      # term -> definition
        'relationships': [],    # topic relationships
        'metadata': {}         # file sources and structure
    }
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                md_text = f.read()
        except UnicodeDecodeError:
            print(f"Skipped (encoding error): {md_file}")
            skipped_files.append(md_file)
            continue
            
        # Extract knowledge items
        knowledge_items = extract_conversational_knowledge(md_text, os.path.basename(md_file))
        
        for item in knowledge_items:
            topic = item['topic'].lower()
            content = item['content']
            
            # Store in appropriate knowledge categories
            knowledge_base['topics'][topic] = {
                'content': content,
                'type': item['type'],
                'source': item['source'],
                'level': item['level']
            }
            
            # Extract definitions
            if item['type'] == 'definition':
                # Try to extract key terms from the topic and content
                words = topic.replace('-', ' ').replace('_', ' ').split()
                for word in words:
                    if len(word) > 3:  # Skip short words
                        knowledge_base['definitions'][word.lower()] = content[:200] + '...' if len(content) > 200 else content
            
            # Extract examples
            if item.get('has_examples'):
                knowledge_base['examples'][topic] = content
                
            # Extract questions (for Q&A style responses)
            if item.get('contains_questions'):
                knowledge_base['questions'][topic] = content
                
            print(f"Imported: {item['topic']}")
    
    # Save comprehensive knowledge base
    knowledge_path = os.path.join(KNOWLEDGE_DIR, 'conversational_knowledge.json')
    try:
        with open(knowledge_path, 'w', encoding='utf-8') as f:
            json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
        print(f"Saved comprehensive knowledge base to {knowledge_path}")
        
        # Create quick lookup files for common queries
        quick_lookups = {}
        
        # Combine all text for word-level lookups
        for topic, data in knowledge_base['topics'].items():
            # Add topic itself
            quick_lookups[topic] = data['content']
            
            # Add key phrases from content
            sentences = data['content'].split('.')
            for sentence in sentences[:3]:  # First 3 sentences
                sentence = sentence.strip()
                if len(sentence) > 20:
                    key = sentence.split()[0:3]  # First 3 words as key
                    if len(key) >= 2:
                        key_phrase = ' '.join(key).lower()
                        quick_lookups[key_phrase] = sentence
        
        # Add definitions to quick lookup
        quick_lookups.update(knowledge_base['definitions'])
        
        # Save quick lookup
        quick_path = os.path.join(KNOWLEDGE_DIR, 'quick_lookup.json')
        with open(quick_path, 'w', encoding='utf-8') as f:
            json.dump(quick_lookups, f, ensure_ascii=False, indent=2)
            
        print(f"Created quick lookup with {len(quick_lookups)} entries")
        
    except Exception as e:
        print(f"Error saving knowledge: {e}")
    
    print("Import complete.")
    if skipped_files:
        print("\nSkipped files due to encoding errors:")
        for fname in skipped_files:
            print(fname)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python import_markdown_knowledge.py <folder_path>")
    else:
        import_markdown_folder(sys.argv[1])
