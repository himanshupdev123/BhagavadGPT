"""
OKF Tag Enhancement Script
Analyzes user queries and enriches verse tags for better matching
"""

import yaml
import json
from pathlib import Path
from collections import defaultdict

# User query themes extracted from real usage
USER_QUERY_THEMES = {
    # Core emotional states
    "anxiety": ["anxious", "worried", "nervous", "stressed", "tension", "panic", "overthinking"],
    "fear": ["afraid", "scared", "fearful", "terrified", "phobia", "dread"],
    "confusion": ["confused", "uncertain", "unclear", "lost", "bewildered", "indecisive"],
    "sadness": ["sad", "depressed", "grief", "sorrow", "melancholy", "heartbroken"],
    "anger": ["angry", "rage", "fury", "irritation", "frustration", "resentment"],
    
    # Modern life challenges
    "procrastination": ["procrastinating", "delaying", "postponing", "avoiding", "lazy", "unmotivated"],
    "motivation": ["motivate", "inspire", "drive", "enthusiasm", "energy", "willpower"],
    "discipline": ["self-control", "consistency", "routine", "habits", "commitment"],
    "distraction": ["distracted", "unfocused", "scattered", "mind-wandering", "concentration"],
    
    # Purpose & meaning
    "purpose": ["life purpose", "meaning", "calling", "destiny", "goal of life", "what to do"],
    "confusion about path": ["career confusion", "which path", "what to choose", "direction"],
    "passion": ["passion", "love for work", "dream", "calling", "vocation"],
    
    # Work & achievement
    "failure": ["failed", "defeat", "loss", "setback", "unsuccessful"],
    "success": ["achieve", "accomplish", "goal", "ambition", "winning"],
    "competition": ["competitive", "rivalry", "comparison", "race"],
    "hard work": ["effort", "dedication", "perseverance", "struggle", "grind"],
    
    # Detachment paradox
    "detachment": ["non-attachment", "letting go", "surrender", "acceptance"],
    "ambition vs detachment": ["results don't matter", "karma yoga", "detached action"],
    
    # Relationships
    "toxic relationships": ["toxic", "abusive", "harmful people", "bad relationships"],
    "breakup": ["separation", "heartbreak", "lost love", "ex"],
    "betrayal": ["cheated", "deceived", "backstabbed", "hurt by friend"],
    "forgiveness": ["forgive", "let go of hurt", "move past pain"],
    
    # Mental challenges
    "mind control": ["control mind", "restless mind", "calm mind", "mental peace"],
    "overthinking": ["thinking too much", "rumination", "analysis paralysis"],
    "mental clarity": ["clear thinking", "focus", "concentration", "sharp mind"],
    
    # Struggle & perseverance  
    "stuck in loop": ["repeating patterns", "same mistakes", "cycle", "trapped"],
    "starting again": ["restart", "new beginning", "second chance", "comeback"],
    "giving up": ["quit", "surrender to failure", "lose hope"],
    
    # Balance
    "work-life balance": ["balance", "time management", "priorities", "juggling"],
    "stress management": ["cope with stress", "handle pressure", "overwhelmed"],
    
    # Spiritual concepts
    "karma": ["action", "duty", "dharma", "right action"],
    "rebirth": ["reincarnation", "past lives", "cycle of birth"],
    "soul": ["atma", "self", "consciousness", "inner being"],
    "maya": ["illusion", "material world", "temporary", "unreal"],
    
    # Self-perception
    "self-doubt": ["not good enough", "inadequate", "incompetent", "unworthy"],
    "self-improvement": ["better person", "growth", "development", "evolution"],
    
    # Decision making
    "decision": ["choice", "dilemma", "crossroads", "options"],
    "right vs wrong": ["morality", "ethics", "what is right", "correct path"],
}

# Tag expansion mapping - maps existing tags to user query language
TAG_EXPANSIONS = {
    "attachment": ["attachment", "clinging", "dependent", "possessive"],
    "duty": ["duty", "responsibility", "obligation", "dharma", "what should I do"],
    "suffering": ["suffering", "pain", "misery", "hardship", "struggle"],
    "peace": ["peace", "calm", "tranquility", "serenity", "mental peace"],
    "ego": ["ego", "pride", "arrogance", "self-importance", "vanity"],
    "desire": ["desire", "want", "craving", "wish", "longing"],
}

def load_okf_verse(file_path):
    """Load OKF markdown file and extract frontmatter"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2]
            return frontmatter, body
    return None, None

def save_okf_verse(file_path, frontmatter, body):
    """Save OKF markdown file with updated frontmatter"""
    yaml_str = yaml.dump(frontmatter, sort_keys=False, allow_unicode=True)
    content = f"---\n{yaml_str}---{body}"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def enhance_tags(current_tags, verse_content):
    """
    Enhance existing tags with user-query-aligned variations
    """
    enhanced = set(current_tags) if current_tags else set()
    
    # Convert content to lowercase for matching
    content_lower = verse_content.lower()
    
    # Add user-query variations for existing tags
    for tag in current_tags or []:
        tag_lower = tag.lower()
        
        # Check if tag matches any theme
        for theme, variations in USER_QUERY_THEMES.items():
            if any(var in tag_lower for var in variations):
                enhanced.update(variations[:3])  # Add top 3 variations
                break
        
        # Check expansions
        for base_tag, expansions in TAG_EXPANSIONS.items():
            if base_tag in tag_lower:
                enhanced.update(expansions[:2])
    
    # Add theme tags based on content analysis
    keywords_in_content = {
        "mind": ["mind control", "mental peace", "restless mind"],
        "action": ["karma", "duty", "work"],
        "fear": ["fear", "anxiety", "worry"],
        "attachment": ["detachment", "non-attachment"],
        "desire": ["desire", "craving", "want"],
    }
    
    for keyword, tags_to_add in keywords_in_content.items():
        if keyword in content_lower:
            enhanced.add(tags_to_add[0])
    
    return sorted(list(enhanced))

def find_related_verses(chapter, verse, all_verses_data):
    """
    Find related verses based on tag overlap and thematic connections
    Returns list of verse references like ['chapter_2/verse_47', ...]
    """
    related = []
    current_tags = set(all_verses_data.get(f"{chapter}_{verse}", {}).get('tags', []))
    
    if not current_tags:
        return []
    
    # Find verses with overlapping tags
    verse_scores = []
    for verse_key, verse_data in all_verses_data.items():
        if verse_key == f"{chapter}_{verse}":
            continue
        
        other_tags = set(verse_data.get('tags', []))
        overlap = len(current_tags & other_tags)
        
        if overlap >= 2:  # At least 2 common tags
            verse_scores.append((overlap, verse_key))
    
    # Sort by overlap and take top 5
    verse_scores.sort(reverse=True, key=lambda x: x[0])
    for score, verse_key in verse_scores[:5]:
        # Convert "chapter_2_verse_47" to "chapter_2/verse_47"
        parts = verse_key.split('_')
        related_ref = f"{parts[0]}_{parts[1]}/verse_{parts[3]}"
        related.append(related_ref)
    
    return related

def main():
    """Main enhancement process"""
    okf_dir = Path("bhagvadgpt_okf")
    
    if not okf_dir.exists():
        print("❌ OKF directory not found!")
        return
    
    print("🚀 Starting OKF tag enhancement...")
    print(f"📚 Processing verses from {okf_dir}\n")
    
    # First pass: collect all verse data
    all_verses = {}
    verse_files = []
    
    for chapter_dir in sorted(okf_dir.glob("chapter_*")):
        for verse_file in sorted(chapter_dir.glob("verse_*.md")):
            frontmatter, body = load_okf_verse(verse_file)
            if frontmatter:
                chapter = chapter_dir.name
                verse = verse_file.stem
                key = f"{chapter}_{verse}"
                all_verses[key] = {
                    'tags': frontmatter.get('tags', []),
                    'file': verse_file,
                    'frontmatter': frontmatter,
                    'body': body
                }
                verse_files.append((chapter, verse, verse_file))
    
    print(f"✅ Loaded {len(all_verses)} verses\n")
    
    # Second pass: enhance tags and find related verses
    updated_count = 0
    for chapter, verse, verse_file in verse_files:
        key = f"{chapter}_{verse}"
        verse_data = all_verses[key]
        
        # Enhance tags
        current_tags = verse_data['frontmatter'].get('tags', [])
        enhanced_tags = enhance_tags(current_tags, verse_data['body'])
        
        # Find related verses
        related = find_related_verses(chapter, verse, all_verses)
        
        # Update if changed
        if enhanced_tags != current_tags or related != verse_data['frontmatter'].get('related', []):
            verse_data['frontmatter']['tags'] = enhanced_tags
            verse_data['frontmatter']['related'] = related
            save_okf_verse(verse_file, verse_data['frontmatter'], verse_data['body'])
            updated_count += 1
            
            if updated_count % 50 == 0:
                print(f"📝 Updated {updated_count} verses...")
    
    print(f"\n🎉 Enhancement complete!")
    print(f"✅ Updated {updated_count} verses with enhanced tags and relationships")
    print(f"📊 Average tags per verse: {sum(len(v['frontmatter']['tags']) for v in all_verses.values()) / len(all_verses):.1f}")

if __name__ == "__main__":
    main()
