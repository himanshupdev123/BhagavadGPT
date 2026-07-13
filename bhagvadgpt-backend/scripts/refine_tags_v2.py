"""
Advanced OKF Tag Refinement - Phase 2
Tests real user queries and adds domain-specific tags
"""

import yaml
import json
from pathlib import Path
from collections import defaultdict, Counter
import re

# Real user queries from your data
TEST_QUERIES = [
    "How to start a thing again where you failed? And how to motivate yourself",
    "How to deal with procrastination?",
    "How to stop worrying about the future?",
    "Most of the time I am confused to take the decision",
    "I am feeling with anxiety and always in sad mood",
    "How do I control my mind when it keeps jumping between tasks?",
    "How can I be disciplined to work towards achieving my goals?",
    "I'm feeling distraction what to do",
    "Is it wrong to cut off people who hurt me emotionally?",
    "I feel confused about my purpose in life",
    "What should be the ideal goal of a human being in his life",
    "When achieving goals depend on luck and not hardworking, how to stay motivated",
    "I feel quite distracted nowadays. There are lots of things running at me",
    "Why do people with good heart usually suffer?",
    "Mind is feeling restless thinking about my future",
    "I want to surrender to God but I am also ambitious",
    "How can I get mental peace in my hectic schedule?",
    "What to do in life if I am getting confused while choosing right path?",
    "I am developing self regret since long time",
    "How do we overcome laziness",
    "How to achieve peace of mind",
    "How to do stress management",
    "How to make decisions when I don't know what's right?",
    "What to do when you get betrayed by your friend",
    "How to get succeed in life",
]

# Advanced tag mappings based on real queries
ADVANCED_TAG_MAPPINGS = {
    # Failure & Recovery
    "failure": {
        "primary": ["failure", "failed", "defeat", "setback", "loss"],
        "context": ["starting again", "second chance", "comeback", "resilience", "recovery"],
        "emotional": ["disappointment", "discouragement", "hopelessness"],
    },
    
    # Procrastination & Discipline
    "procrastination": {
        "primary": ["procrastination", "delay", "postponing", "avoiding"],
        "context": ["laziness", "unmotivated", "stuck", "inaction", "paralysis"],
        "solutions": ["discipline", "self-control", "action", "momentum", "starting"],
    },
    
    # Worry & Anxiety
    "worry": {
        "primary": ["worry", "worried", "worrying", "anxiety", "anxious"],
        "context": ["future", "uncertainty", "unknown", "what if"],
        "emotional": ["nervous", "stressed", "tense", "fearful", "overthinking"],
    },
    
    # Decision Making
    "decision": {
        "primary": ["decision", "choice", "choose", "deciding", "dilemma"],
        "context": ["confused", "uncertain", "don't know", "stuck"],
        "solutions": ["clarity", "wisdom", "guidance", "right path"],
    },
    
    # Mind Control
    "mind control": {
        "primary": ["control mind", "mind jumping", "restless mind", "wandering mind"],
        "context": ["distraction", "unfocused", "scattered", "concentration"],
        "solutions": ["focus", "meditation", "mental discipline", "steadiness"],
    },
    
    # Goals & Ambition
    "goals": {
        "primary": ["goals", "achieve", "ambition", "success", "accomplish"],
        "context": ["work hard", "effort", "dedication", "perseverance"],
        "conflicts": ["detachment", "non-attachment", "surrender", "letting go"],
    },
    
    # Purpose & Meaning
    "purpose": {
        "primary": ["purpose", "meaning", "life goal", "calling", "destiny"],
        "context": ["confused", "lost", "direction", "path"],
        "questions": ["why am I here", "what should I do", "what is my role"],
    },
    
    # Motivation
    "motivation": {
        "primary": ["motivation", "motivate", "inspire", "drive", "enthusiasm"],
        "context": ["lost motivation", "giving up", "quitting", "hopeless"],
        "blocks": ["luck", "circumstances", "external factors"],
    },
    
    # Emotional Relationships
    "toxic relationships": {
        "primary": ["toxic", "hurt emotionally", "harmful people", "bad relationships"],
        "context": ["cutting off", "boundaries", "protecting peace"],
        "emotions": ["betrayal", "pain", "hurt", "wounded"],
    },
    
    # Mental Peace
    "mental peace": {
        "primary": ["mental peace", "peace of mind", "calm", "tranquility"],
        "context": ["hectic", "busy", "overwhelmed", "stressed"],
        "solutions": ["balance", "rest", "mindfulness", "serenity"],
    },
    
    # Suffering
    "suffering": {
        "primary": ["suffering", "pain", "misery", "hardship"],
        "context": ["good people", "innocent", "undeserved"],
        "questions": ["why me", "unfair", "injustice"],
    },
    
    # Self-doubt
    "self-doubt": {
        "primary": ["self-doubt", "not good enough", "regret", "inadequate"],
        "context": ["comparing", "failing", "disappointing"],
        "emotions": ["shame", "guilt", "worthless", "incompetent"],
    },
    
    # Surrender vs Ambition paradox
    "surrender ambition": {
        "primary": ["surrender", "ambition", "detachment", "goals"],
        "conflict": ["contradiction", "paradox", "both"],
        "context": ["karma yoga", "action without attachment"],
    },
    
    # Path confusion
    "confused path": {
        "primary": ["confused", "which path", "right path", "direction"],
        "context": ["crossroads", "options", "choices", "uncertain"],
        "need": ["clarity", "guidance", "wisdom", "sign"],
    },
    
    # Betrayal
    "betrayal": {
        "primary": ["betrayed", "betrayal", "cheated", "backstabbed"],
        "context": ["friend", "trust broken", "hurt"],
        "response": ["forgiveness", "moving on", "kindness despite pain"],
    },
    
    # Success
    "success": {
        "primary": ["success", "succeed", "achievement", "winning"],
        "context": ["how to", "path to", "way to"],
        "methods": ["hard work", "smart work", "strategy", "effort"],
    },
}

# Chapter-specific expertise
CHAPTER_THEMES = {
    2: ["self-knowledge", "equanimity", "steadiness", "wisdom", "detachment"],
    3: ["karma yoga", "selfless action", "duty", "work", "sacrifice"],
    4: ["knowledge", "renunciation", "action in inaction"],
    5: ["renunciation", "karma yoga balance", "peace"],
    6: ["meditation", "mind control", "yoga", "concentration", "discipline"],
    7: ["divine knowledge", "devotion", "supreme reality"],
    8: ["supreme person", "ultimate goal", "remembrance"],
    9: ["devotion", "bhakti", "grace", "surrender"],
    10: ["divine manifestations", "glory", "power"],
    11: ["universal form", "divine vision", "awe"],
    12: ["devotion path", "bhakti yoga", "divine qualities"],
    13: ["field and knower", "body and soul", "knowledge"],
    14: ["three gunas", "qualities", "transcendence"],
    15: ["supreme person", "eternal tree", "liberation"],
    16: ["divine and demoniac qualities", "virtues", "vices"],
    17: ["three types of faith", "austerity", "charity"],
    18: ["liberation", "renunciation", "moksha", "perfection"],
}

def load_all_verses(okf_dir):
    """Load all OKF verses"""
    verses = {}
    for chapter_dir in sorted(okf_dir.glob("chapter_*")):
        for verse_file in sorted(chapter_dir.glob("verse_*.md")):
            with open(verse_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    body = parts[2]
                    
                    chapter_num = int(chapter_dir.name.split('_')[1])
                    verse_num = int(verse_file.stem.split('_')[1])
                    
                    verses[f"{chapter_num}.{verse_num}"] = {
                        'file': verse_file,
                        'frontmatter': frontmatter,
                        'body': body,
                        'chapter': chapter_num,
                        'verse': verse_num
                    }
    return verses

def extract_keywords(query):
    """Extract meaningful keywords from query"""
    # Remove common words
    stop_words = {'how', 'to', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'is', 'are', 'was', 'were', 'i', 'my', 'me', 'do', 'does', 'what', 'when', 'where'}
    
    words = re.findall(r'\w+', query.lower())
    keywords = [w for w in words if w not in stop_words and len(w) > 3]
    
    return keywords

def find_matching_theme(query):
    """Find best matching theme for a query"""
    query_lower = query.lower()
    best_match = None
    best_score = 0
    
    for theme, tag_data in ADVANCED_TAG_MAPPINGS.items():
        score = 0
        all_tags = []
        
        for category, tags in tag_data.items():
            all_tags.extend(tags)
        
        for tag in all_tags:
            if tag in query_lower:
                score += 1
        
        if score > best_score:
            best_score = score
            best_match = theme
    
    return best_match, best_score

def suggest_tags_for_verse(verse_data, theme):
    """Suggest additional tags based on verse content and theme"""
    current_tags = set(verse_data['frontmatter'].get('tags', []))
    suggested = set()
    
    if theme and theme in ADVANCED_TAG_MAPPINGS:
        theme_data = ADVANCED_TAG_MAPPINGS[theme]
        
        # Add primary tags if relevant
        body_lower = verse_data['body'].lower()
        for category, tags in theme_data.items():
            for tag in tags:
                # Check if tag concept appears in verse
                if any(keyword in body_lower for keyword in tag.split()):
                    suggested.add(tag)
    
    # Add chapter-specific themes
    chapter = verse_data['chapter']
    if chapter in CHAPTER_THEMES:
        for theme_tag in CHAPTER_THEMES[chapter]:
            if theme_tag.split()[0] in verse_data['body'].lower():
                suggested.add(theme_tag)
    
    # Return only new suggestions
    return sorted(list(suggested - current_tags))

def test_queries_and_refine(okf_dir):
    """Test queries and suggest tag improvements"""
    print("🔍 Testing real user queries...\n")
    
    verses = load_all_verses(okf_dir)
    print(f"✅ Loaded {len(verses)} verses\n")
    
    suggestions = defaultdict(set)
    query_results = []
    
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\n{'='*70}")
        print(f"Query {i}: {query}")
        print('='*70)
        
        # Find theme
        theme, score = find_matching_theme(query)
        keywords = extract_keywords(query)
        
        print(f"🎯 Theme: {theme} (confidence: {score})")
        print(f"🔑 Keywords: {', '.join(keywords[:5])}")
        
        # Find matching verses
        matches = []
        for verse_id, verse_data in verses.items():
            verse_score = 0
            tags = verse_data['frontmatter'].get('tags', [])
            
            for keyword in keywords:
                for tag in tags:
                    if keyword in tag.lower():
                        verse_score += 1
            
            if verse_score > 0:
                matches.append((verse_score, verse_id, verse_data))
        
        matches.sort(reverse=True, key=lambda x: x[0])
        
        if matches:
            print(f"\n✅ Found {len(matches)} matching verses:")
            for score, verse_id, verse_data in matches[:3]:
                print(f"  • {verse_id} (score: {score}) - {verse_data['frontmatter'].get('title', '')}")
                
                # Suggest additional tags
                new_tags = suggest_tags_for_verse(verse_data, theme)
                if new_tags:
                    suggestions[verse_id].update(new_tags)
                    print(f"    💡 Suggested tags: {', '.join(new_tags[:5])}")
        else:
            print("⚠️ No matching verses found - need better tags!")
            print(f"   Should match verses about: {theme}")
        
        query_results.append({
            'query': query,
            'theme': theme,
            'matches': len(matches),
            'top_verse': matches[0][1] if matches else None
        })
    
    return suggestions, query_results

def apply_suggestions(okf_dir, suggestions):
    """Apply tag suggestions to verses"""
    print(f"\n\n{'='*70}")
    print("📝 Applying suggested tags...")
    print('='*70)\n")
    
    updated = 0
    for verse_id, new_tags in suggestions.items():
        chapter, verse = verse_id.split('.')
        verse_file = okf_dir / f"chapter_{chapter}" / f"verse_{verse}.md"
        
        with open(verse_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2]
            
            current_tags = set(frontmatter.get('tags', []))
            updated_tags = sorted(list(current_tags | new_tags))
            
            if len(updated_tags) > len(current_tags):
                frontmatter['tags'] = updated_tags
                yaml_str = yaml.dump(frontmatter, sort_keys=False, allow_unicode=True)
                new_content = f"---\n{yaml_str}---{body}"
                
                with open(verse_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                updated += 1
                print(f"✅ Updated {verse_id}: +{len(new_tags)} tags")
    
    print(f"\n🎉 Updated {updated} verses with refined tags!")

def main():
    okf_dir = Path("bhagvadgpt_okf")
    
    if not okf_dir.exists():
        print("❌ OKF directory not found!")
        return
    
    print("🚀 Starting Advanced Tag Refinement - Phase 2\n")
    
    # Test queries and get suggestions
    suggestions, query_results = test_queries_and_refine(okf_dir)
    
    # Show summary
    print(f"\n\n{'='*70}")
    print("📊 SUMMARY")
    print('='*70)
    print(f"Total queries tested: {len(TEST_QUERIES)}")
    print(f"Verses to update: {len(suggestions)}")
    print(f"Average matches per query: {sum(r['matches'] for r in query_results) / len(query_results):.1f}")
    
    # Apply suggestions
    if suggestions:
        apply_suggestions(okf_dir, suggestions)
    else:
        print("\n✅ No additional tags needed - system is well optimized!")

if __name__ == "__main__":
    main()
