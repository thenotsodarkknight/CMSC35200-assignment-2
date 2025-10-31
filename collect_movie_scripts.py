"""
Collect real movie scripts from IMSDB (Internet Movie Script Database)
All scripts are publicly available
"""
import requests
from pathlib import Path
import time
import re

def collect_movie_scripts():
    """Collect movie scripts from IMSDB"""
    
    output_dir = Path("/Users/abeen/Documents/Fall_Quarter/DLS_LAB2_REAL/data/movie_scripts")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_scripts = []
    metadata = []
    
    print("Collecting movie scripts from IMSDB...")
    
    # List of freely available scripts on IMSDB
    scripts = [
        ('The Matrix', 'Matrix,-The'),
        ('Pulp Fiction', 'Pulp-Fiction'),
        ('The Shawshank Redemption', 'Shawshank-Redemption,-The'),
        ('The Godfather', 'Godfather'),
        ('Forrest Gump', 'Forrest-Gump'),
        ('Goodfellas', 'Goodfellas'),
        ('The Dark Knight', 'Dark-Knight,-The'),
        ('Fight Club', 'Fight-Club'),
        ('Inception', 'Inception'),
        ('Interstellar', 'Interstellar'),
        ('The Departed', 'Departed,-The'),
        ('Se7en', 'Se7en'),
        ('The Usual Suspects', 'Usual-Suspects,-The'),
        ('American Beauty', 'American-Beauty'),
        ('The Silence of the Lambs', 'Silence-of-the-Lambs,-The'),
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    for title, url_name in scripts:
        try:
            url = f'https://imsdb.com/scripts/{url_name}.html'
            print(f"  Fetching: {title}...")
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                content = response.text
                
                # Extract script from HTML
                if '<pre>' in content and '</pre>' in content:
                    script_start = content.find('<pre>')
                    script_end = content.find('</pre>', script_start)
                    
                    if script_start != -1 and script_end != -1:
                        script_text = content[script_start+5:script_end]
                        
                        # Clean HTML entities and tags
                        script_text = script_text.replace('&nbsp;', ' ')
                        script_text = script_text.replace('&lt;', '<')
                        script_text = script_text.replace('&gt;', '>')
                        script_text = script_text.replace('&amp;', '&')
                        script_text = script_text.replace('<b>', '').replace('</b>', '')
                        script_text = script_text.replace('<i>', '').replace('</i>', '')
                        script_text = re.sub(r'<[^>]+>', '', script_text)
                        
                        if len(script_text) > 5000:  # Only include substantial scripts
                            script_block = f"\n{'='*80}\n"
                            script_block += f"SCRIPT: {title}\n"
                            script_block += f"SOURCE: IMSDB\n"
                            script_block += f"{'='*80}\n\n"
                            script_block += script_text
                            
                            all_scripts.append(script_block)
                            
                            metadata.append({
                                'title': title,
                                'source': 'IMSDB',
                                'length': len(script_text)
                            })
                            
                            print(f"    ✓ Collected ({len(script_text):,} chars)")
                        else:
                            print(f"    ✗ Script too short")
                    else:
                        print(f"    ✗ Could not parse script")
                else:
                    print(f"    ✗ No <pre> tags found")
            else:
                print(f"    ✗ Status {response.status_code}")
            
            time.sleep(2)  # Be respectful
            
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    # Save all scripts
    output_file = output_dir / "movie_scripts_corpus.txt"
    full_corpus = "\n".join(all_scripts)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_corpus)
    
    # Calculate statistics
    total_chars = len(full_corpus)
    total_lines = full_corpus.count('\n')
    num_scripts = len(all_scripts)
    
    # Analyze screenplay elements
    num_int = len(re.findall(r'\bINT\.', full_corpus, re.IGNORECASE))
    num_ext = len(re.findall(r'\bEXT\.', full_corpus, re.IGNORECASE))
    num_fade = len(re.findall(r'FADE', full_corpus, re.IGNORECASE))
    num_cut = len(re.findall(r'CUT TO', full_corpus, re.IGNORECASE))
    
    stats = {
        'num_scripts': num_scripts,
        'total_chars': total_chars,
        'total_lines': total_lines,
        'total_size_mb': total_chars / (1024 * 1024),
        'avg_chars_per_script': total_chars / num_scripts if num_scripts > 0 else 0,
        'int_scenes': num_int,
        'ext_scenes': num_ext,
        'fades': num_fade,
        'cuts': num_cut,
        'source': 'Internet Movie Script Database (IMSDB)'
    }
    
    # Save metadata
    import json
    metadata_file = output_dir / "metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Save statistics
    stats_file = output_dir / "statistics.txt"
    with open(stats_file, 'w') as f:
        f.write("Movie Scripts Corpus Statistics\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Number of scripts: {stats['num_scripts']}\n")
        f.write(f"Total characters: {stats['total_chars']:,}\n")
        f.write(f"Total lines: {stats['total_lines']:,}\n")
        f.write(f"Total size: {stats['total_size_mb']:.2f} MB\n")
        f.write(f"Avg chars per script: {stats['avg_chars_per_script']:,.0f}\n\n")
        f.write("Screenplay Elements:\n")
        f.write(f"  INT. scenes: {stats['int_scenes']}\n")
        f.write(f"  EXT. scenes: {stats['ext_scenes']}\n")
        f.write(f"  FADE transitions: {stats['fades']}\n")
        f.write(f"  CUT TO transitions: {stats['cuts']}\n\n")
        f.write(f"Source: {stats['source']}\n")
    
    print(f"\n✓ Movie scripts collection complete!")
    print(f"  - Saved to: {output_file}")
    print(f"  - Number of scripts: {num_scripts}")
    print(f"  - Total size: {stats['total_size_mb']:.2f} MB")
    print(f"  - Statistics saved to: {stats_file}")
    
    return stats

if __name__ == "__main__":
    collect_movie_scripts()

