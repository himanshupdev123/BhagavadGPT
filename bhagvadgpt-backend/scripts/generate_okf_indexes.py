"""
Generate OKF-compliant index.md files for each chapter directory
Following the Open Knowledge Format v0.1 specification
"""

from pathlib import Path
import yaml
import sys

def load_verse(verse_path):
    """Load verse metadata from markdown file"""
    with open(verse_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            return frontmatter
    return None

def generate_chapter_index(chapter_dir):
    """Generate index.md for a single chapter"""
    chapter_name = chapter_dir.name
    chapter_num = chapter_name.split('_')[1]
    
    # Chapter titles and descriptions
    chapter_info = {
        '1': ('Arjuna Vishada Yoga', 'The Yoga of Arjuna\'s Dejection', 
              'Arjuna is overcome with despair and confusion on the battlefield, unable to fight.'),
        '2': ('Sankhya Yoga', 'The Yoga of Knowledge',
              'Krishna begins his teachings, explaining the nature of the soul, duty, and the path of knowledge and action.'),
        '3': ('Karma Yoga', 'The Yoga of Action',
              'Krishna teaches the importance of selfless action and performing one\'s duty without attachment to results.'),
        '4': ('Jnana Yoga', 'The Yoga of Knowledge',
              'Krishna explains the science of action and inaction, the nature of divine incarnation, and transcendental knowledge.'),
        '5': ('Karma Sannyasa Yoga', 'The Yoga of Renunciation of Action',
              'Krishna clarifies the relationship between renunciation and action in devotion.'),
        '6': ('Dhyana Yoga', 'The Yoga of Meditation',
              'Krishna teaches the practice of meditation, self-control, and the discipline of the mind.'),
        '7': ('Jnana Vijnana Yoga', 'The Yoga of Knowledge and Wisdom',
              'Krishna reveals knowledge of the Absolute and the manifestation of His divine nature.'),
        '8': ('Aksara Brahma Yoga', 'The Yoga of the Imperishable Brahman',
              'Krishna explains the path to reach the Supreme at the time of death and the nature of the Absolute.'),
        '9': ('Raja Vidya Yoga', 'The Yoga of Royal Knowledge',
              'Krishna reveals the most confidential knowledge and the supreme science of devotion.'),
        '10': ('Vibhuti Yoga', 'The Yoga of Divine Glories',
              'Krishna describes His infinite manifestations and divine powers throughout creation.'),
        '11': ('Vishwarupa Darshana Yoga', 'The Yoga of the Vision of the Universal Form',
               'Arjuna witnesses Krishna\'s cosmic, universal form - a vision of the entire universe.'),
        '12': ('Bhakti Yoga', 'The Yoga of Devotion',
               'Krishna explains the path of devotion and love for God as the highest spiritual practice.'),
        '13': ('Kshetra Kshetrajna Vibhaga Yoga', 'The Yoga of Distinction between Field and Knower',
               'Krishna distinguishes between the body (field), the soul (knower), and the Supreme Soul.'),
        '14': ('Gunatraya Vibhaga Yoga', 'The Yoga of the Division of Three Gunas',
               'Krishna explains the three modes of material nature (gunas) and how to transcend them.'),
        '15': ('Purushottama Yoga', 'The Yoga of the Supreme Person',
               'Krishna describes the ultimate reality and the Supreme Personality.'),
        '16': ('Daivasura Sampad Vibhaga Yoga', 'The Yoga of Division between Divine and Demoniac',
               'Krishna distinguishes between divine and demoniac qualities in human beings.'),
        '17': ('Shraddhatraya Vibhaga Yoga', 'The Yoga of Division of Three Kinds of Faith',
               'Krishna explains the three types of faith and how they manifest in worship, charity, and austerity.'),
        '18': ('Moksha Sannyasa Yoga', 'The Yoga of Liberation through Renunciation',
               'Krishna summarizes all teachings and reveals the ultimate path to liberation.')
    }
    
    title, subtitle, description = chapter_info.get(chapter_num, 
                                                     (f'Chapter {chapter_num}', '', ''))
    
    # Collect all verses
    verses = []
    for verse_file in sorted(chapter_dir.glob('verse_*.md')):
        metadata = load_verse(verse_file)
        if metadata:
            verse_num = verse_file.stem.split('_')[1]
            verses.append({
                'number': int(verse_num),
                'file': verse_file.name,
                'title': metadata.get('title', ''),
                'description': metadata.get('description', '')[:100] + '...' if len(metadata.get('description', '')) > 100 else metadata.get('description', '')
            })
    
    # Generate index content
    index_content = f"""# Chapter {chapter_num} - {title}

## {subtitle}

{description}

**Total Verses**: {len(verses)}

---

## Verses

"""
    
    # Add verse listings in groups of 10
    for i, verse in enumerate(verses, 1):
        index_content += f"- **[Verse {verse['number']}]({verse['file']})** - {verse['description']}\n"
        
        # Add separator every 10 verses for readability
        if i % 10 == 0 and i < len(verses):
            index_content += "\n"
    
    index_content += f"""
---

## Notable Verses

"""
    
    # Highlight key verses per chapter (manually curated)
    key_verses = {
        '2': [47, 55, 62, 63],
        '3': [19, 27],
        '4': [7, 8],
        '6': [5, 35],
        '9': [22, 27],
        '12': [8, 13, 14],
        '13': [13],
        '18': [66, 78]
    }
    
    if chapter_num in key_verses:
        for verse_num in key_verses[chapter_num]:
            verse = next((v for v in verses if v['number'] == verse_num), None)
            if verse:
                index_content += f"- **Verse {verse_num}**: {verse['description']}\n"
    else:
        index_content += "*Key verses to be identified*\n"
    
    index_content += f"""
---

## Navigation

- [← Back to Root Index](../index.md)
- [View Change Log](../log.md)

*This index follows the [Open Knowledge Format v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)*
"""
    
    return index_content

def main():
    """Generate index.md files for all chapters"""
    okf_dir = Path('bhagvadgpt_okf')
    
    if not okf_dir.exists():
        print(f"❌ Error: {okf_dir} directory not found")
        print("   Make sure you're running from the backend root directory")
        return 1
    
    print("=" * 70)
    print("GENERATING OKF CHAPTER INDEX FILES")
    print("=" * 70)
    print()
    
    generated = 0
    for chapter_dir in sorted(okf_dir.glob('chapter_*')):
        if chapter_dir.is_dir():
            print(f"📝 Generating index for {chapter_dir.name}...")
            
            index_content = generate_chapter_index(chapter_dir)
            index_path = chapter_dir / 'index.md'
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            print(f"   ✅ Created {index_path}")
            generated += 1
    
    print()
    print("=" * 70)
    print(f"✅ SUCCESS: Generated {generated} chapter index files")
    print("=" * 70)
    print()
    print("These index files enable:")
    print("  • Progressive disclosure for agents and humans")
    print("  • Chapter-level navigation without loading all verses")
    print("  • OKF v0.1 specification compliance")
    print()
    return 0

if __name__ == '__main__':
    sys.exit(main())
