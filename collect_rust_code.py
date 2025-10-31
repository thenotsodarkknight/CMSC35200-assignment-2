"""
Collect real Rust code from popular GitHub repositories
Using GitHub API to fetch actual Rust source files
"""
import requests
from pathlib import Path
import time
import base64
import json

def collect_rust_code():
    """Collect Rust code from real GitHub repositories"""
    
    output_dir = Path("/Users/abeen/Documents/Fall_Quarter/DLS_LAB2_REAL/data/rust_code")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_code = []
    metadata = []
    
    print("Collecting Rust code from GitHub repositories...")
    
    # Popular Rust repositories (public, open source)
    repos = [
        "rust-lang/rust",  # The Rust compiler itself
        "tokio-rs/tokio",  # Async runtime
        "serde-rs/serde",  # Serialization framework
        "actix/actix-web", # Web framework
        "rust-lang/cargo", # Package manager
    ]
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Educational-Research-Project'
    }
    
    total_files = 0
    
    for repo in repos:
        print(f"\n  Fetching from {repo}...")
        
        try:
            # Get repository contents (src directory typically)
            url = f"https://api.github.com/repos/{repo}/contents/src"
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                contents = response.json()
                
                # Filter for .rs files
                rs_files = [item for item in contents if item['name'].endswith('.rs')][:10]  # Limit to 10 per repo
                
                print(f"    Found {len(rs_files)} .rs files, fetching...")
                
                for file_info in rs_files:
                    try:
                        # Fetch the actual file content
                        file_url = file_info['url']
                        file_response = requests.get(file_url, headers=headers, timeout=10)
                        
                        if file_response.status_code == 200:
                            file_data = file_response.json()
                            
                            # Decode base64 content
                            if 'content' in file_data:
                                content_b64 = file_data['content']
                                content = base64.b64decode(content_b64).decode('utf-8', errors='ignore')
                                
                                if len(content) > 100:  # Only include substantial files
                                    code_block = f"\n{'='*80}\n"
                                    code_block += f"// FILE: {file_info['name']}\n"
                                    code_block += f"// REPO: {repo}\n"
                                    code_block += f"// PATH: {file_info['path']}\n"
                                    code_block += f"{'='*80}\n\n"
                                    code_block += content + "\n"
                                    
                                    all_code.append(code_block)
                                    total_files += 1
                                    
                                    metadata.append({
                                        'repo': repo,
                                        'file': file_info['name'],
                                        'path': file_info['path'],
                                        'size': len(content)
                                    })
                                    
                                    print(f"      ✓ {file_info['name']} ({len(content)} chars)")
                        
                        time.sleep(1)  # Rate limiting
                        
                    except Exception as e:
                        print(f"      ✗ Error fetching {file_info['name']}: {e}")
                        continue
                
            elif response.status_code == 403:
                print(f"    ✗ Rate limited by GitHub API")
                break
            else:
                print(f"    ✗ Status {response.status_code}")
            
            time.sleep(2)  # Be nice to GitHub
            
        except Exception as e:
            print(f"    ✗ Error with repo {repo}: {e}")
            continue
    
    # Also fetch from Rust by Example (public educational resource)
    print("\n  Fetching from Rust By Example...")
    try:
        # Rust by Example has code examples in their GitHub repo
        rbe_url = "https://api.github.com/repos/rust-lang/rust-by-example/contents/src"
        response = requests.get(rbe_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            contents = response.json()
            
            # Get .md files which contain code examples
            md_files = [item for item in contents if item['name'].endswith('.md')][:5]
            
            for file_info in md_files:
                try:
                    file_response = requests.get(file_info['url'], headers=headers, timeout=10)
                    if file_response.status_code == 200:
                        file_data = file_response.json()
                        if 'content' in file_data:
                            content = base64.b64decode(file_data['content']).decode('utf-8', errors='ignore')
                            
                            # Extract Rust code blocks from markdown
                            import re
                            rust_blocks = re.findall(r'```rust\n(.*?)```', content, re.DOTALL)
                            
                            for i, block in enumerate(rust_blocks):
                                if len(block) > 50:
                                    code_block = f"\n{'='*80}\n"
                                    code_block += f"// SOURCE: Rust By Example - {file_info['name']} (block {i+1})\n"
                                    code_block += f"{'='*80}\n\n"
                                    code_block += block + "\n"
                                    all_code.append(code_block)
                                    total_files += 1
                    
                    time.sleep(1)
                except:
                    continue
                    
    except Exception as e:
        print(f"    ✗ Error with Rust By Example: {e}")
    
    # Save all code
    output_file = output_dir / "rust_code_corpus.txt"
    full_corpus = "\n".join(all_code)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_corpus)
    
    # Save metadata
    metadata_file = output_dir / "metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Calculate statistics
    total_chars = len(full_corpus)
    total_lines = full_corpus.count('\n')
    num_files = len(all_code)
    
    # Count Rust-specific patterns
    num_fn = full_corpus.count('fn ')
    num_impl = full_corpus.count('impl ')
    num_struct = full_corpus.count('struct ')
    num_enum = full_corpus.count('enum ')
    num_match = full_corpus.count('match ')
    num_unwrap = full_corpus.count('.unwrap()')
    
    stats = {
        'num_files': num_files,
        'total_chars': total_chars,
        'total_lines': total_lines,
        'total_size_mb': total_chars / (1024 * 1024),
        'avg_chars_per_file': total_chars / num_files if num_files > 0 else 0,
        'fn_count': num_fn,
        'impl_count': num_impl,
        'struct_count': num_struct,
        'enum_count': num_enum,
        'match_count': num_match,
        'unwrap_count': num_unwrap,
        'source': 'GitHub API (rust-lang, tokio, serde, actix, cargo)'
    }
    
    # Save statistics
    stats_file = output_dir / "statistics.txt"
    with open(stats_file, 'w') as f:
        f.write("Rust Code Corpus Statistics\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Number of files: {stats['num_files']}\n")
        f.write(f"Total characters: {stats['total_chars']:,}\n")
        f.write(f"Total lines: {stats['total_lines']:,}\n")
        f.write(f"Total size: {stats['total_size_mb']:.2f} MB\n")
        f.write(f"Average chars per file: {stats['avg_chars_per_file']:,.0f}\n\n")
        f.write("Rust Language Features Found:\n")
        f.write(f"  fn (functions): {stats['fn_count']:,}\n")
        f.write(f"  impl blocks: {stats['impl_count']:,}\n")
        f.write(f"  struct definitions: {stats['struct_count']:,}\n")
        f.write(f"  enum definitions: {stats['enum_count']:,}\n")
        f.write(f"  match expressions: {stats['match_count']:,}\n")
        f.write(f"  .unwrap() calls: {stats['unwrap_count']:,}\n\n")
        f.write(f"Data source: {stats['source']}\n")
    
    print(f"\n✓ Rust code collection complete!")
    print(f"  - Saved to: {output_file}")
    print(f"  - Number of files: {num_files}")
    print(f"  - Total size: {stats['total_size_mb']:.2f} MB")
    print(f"  - Statistics saved to: {stats_file}")
    
    return stats

if __name__ == "__main__":
    collect_rust_code()

