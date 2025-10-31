"""
Collect real Python code from popular open-source projects
Using direct file access (no API auth needed)
"""
import requests
from pathlib import Path
import time
import json

def collect_python_code():
    """Collect Python code from open-source projects"""
    
    output_dir = Path("/Users/abeen/Documents/Fall_Quarter/DLS_LAB2_REAL/data/python_code")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_code = []
    metadata = []
    
    print("Collecting Python code from open-source projects...")
    
    # Direct links to Python files in popular repos (using raw.githubusercontent.com)
    files = [
        # Flask framework
        ('flask/app.py', 'https://raw.githubusercontent.com/pallets/flask/main/src/flask/app.py'),
        ('flask/blueprints.py', 'https://raw.githubusercontent.com/pallets/flask/main/src/flask/blueprints.py'),
        ('flask/cli.py', 'https://raw.githubusercontent.com/pallets/flask/main/src/flask/cli.py'),
        
        # Django framework
        ('django/views.py', 'https://raw.githubusercontent.com/django/django/main/django/views/generic/base.py'),
        ('django/models.py', 'https://raw.githubusercontent.com/django/django/main/django/db/models/base.py'),
        ('django/forms.py', 'https://raw.githubusercontent.com/django/django/main/django/forms/forms.py'),
        
        # Requests library
        ('requests/api.py', 'https://raw.githubusercontent.com/psf/requests/main/src/requests/api.py'),
        ('requests/models.py', 'https://raw.githubusercontent.com/psf/requests/main/src/requests/models.py'),
        ('requests/sessions.py', 'https://raw.githubusercontent.com/psf/requests/main/src/requests/sessions.py'),
        
        # NumPy
        ('numpy/core.py', 'https://raw.githubusercontent.com/numpy/numpy/main/numpy/core/__init__.py'),
        ('numpy/linalg.py', 'https://raw.githubusercontent.com/numpy/numpy/main/numpy/linalg/linalg.py'),
        
        # Pandas
        ('pandas/core.py', 'https://raw.githubusercontent.com/pandas-dev/pandas/main/pandas/core/frame.py'),
        ('pandas/series.py', 'https://raw.githubusercontent.com/pandas-dev/pandas/main/pandas/core/series.py'),
        
        # Scikit-learn
        ('sklearn/linear.py', 'https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/sklearn/linear_model/_base.py'),
        ('sklearn/tree.py', 'https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/sklearn/tree/_classes.py'),
        
        # FastAPI
        ('fastapi/applications.py', 'https://raw.githubusercontent.com/tiangolo/fastapi/master/fastapi/applications.py'),
        ('fastapi/routing.py', 'https://raw.githubusercontent.com/tiangolo/fastapi/master/fastapi/routing.py'),
        
        # pytest
        ('pytest/main.py', 'https://raw.githubusercontent.com/pytest-dev/pytest/main/src/_pytest/main.py'),
        ('pytest/fixtures.py', 'https://raw.githubusercontent.com/pytest-dev/pytest/main/src/_pytest/fixtures.py'),
        
        # Black formatter
        ('black/linegen.py', 'https://raw.githubusercontent.com/psf/black/main/src/black/linegen.py'),
        ('black/mode.py', 'https://raw.githubusercontent.com/psf/black/main/src/black/mode.py'),
    ]
    
    headers = {
        'User-Agent': 'Educational-Research-Project'
    }
    
    for file_name, url in files:
        try:
            print(f"  Fetching: {file_name}...")
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                content = response.text
                
                if len(content) > 500:  # Only include substantial files
                    code_block = f"\n{'='*80}\n"
                    code_block += f"# FILE: {file_name}\n"
                    code_block += f"# SOURCE: {url.split('/')[3]}/{url.split('/')[4]}\n"
                    code_block += f"{'='*80}\n\n"
                    code_block += content + "\n"
                    
                    all_code.append(code_block)
                    
                    metadata.append({
                        'file': file_name,
                        'url': url,
                        'size': len(content)
                    })
                    
                    print(f"    ✓ Collected ({len(content):,} chars)")
                else:
                    print(f"    ✗ File too short")
            else:
                print(f"    ✗ Status {response.status_code}")
            
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    # Save all code
    output_file = output_dir / "python_code_corpus.txt"
    full_corpus = "\n".join(all_code)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_corpus)
    
    # Calculate statistics
    total_chars = len(full_corpus)
    total_lines = full_corpus.count('\n')
    num_files = len(all_code)
    
    # Count Python-specific patterns
    num_def = full_corpus.count('def ')
    num_class = full_corpus.count('class ')
    num_import = full_corpus.count('import ')
    num_if = full_corpus.count('if ')
    num_for = full_corpus.count('for ')
    num_try = full_corpus.count('try:')
    num_async = full_corpus.count('async ')
    num_lambda = full_corpus.count('lambda ')
    
    stats = {
        'num_files': num_files,
        'total_chars': total_chars,
        'total_lines': total_lines,
        'total_size_mb': total_chars / (1024 * 1024),
        'avg_chars_per_file': total_chars / num_files if num_files > 0 else 0,
        'def_count': num_def,
        'class_count': num_class,
        'import_count': num_import,
        'if_count': num_if,
        'for_count': num_for,
        'try_count': num_try,
        'async_count': num_async,
        'lambda_count': num_lambda,
        'source': 'Open-source Python projects (Flask, Django, NumPy, Pandas, etc.)'
    }
    
    # Save metadata
    metadata_file = output_dir / "metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Save statistics
    stats_file = output_dir / "statistics.txt"
    with open(stats_file, 'w') as f:
        f.write("Python Code Corpus Statistics\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Number of files: {stats['num_files']}\n")
        f.write(f"Total characters: {stats['total_chars']:,}\n")
        f.write(f"Total lines: {stats['total_lines']:,}\n")
        f.write(f"Total size: {stats['total_size_mb']:.2f} MB\n")
        f.write(f"Avg chars per file: {stats['avg_chars_per_file']:,.0f}\n\n")
        f.write("Python Language Features:\n")
        f.write(f"  def (functions): {stats['def_count']:,}\n")
        f.write(f"  class definitions: {stats['class_count']:,}\n")
        f.write(f"  import statements: {stats['import_count']:,}\n")
        f.write(f"  if statements: {stats['if_count']:,}\n")
        f.write(f"  for loops: {stats['for_count']:,}\n")
        f.write(f"  try blocks: {stats['try_count']:,}\n")
        f.write(f"  async definitions: {stats['async_count']:,}\n")
        f.write(f"  lambda expressions: {stats['lambda_count']:,}\n\n")
        f.write(f"Source: {stats['source']}\n")
    
    print(f"\n✓ Python code collection complete!")
    print(f"  - Saved to: {output_file}")
    print(f"  - Number of files: {num_files}")
    print(f"  - Total size: {stats['total_size_mb']:.2f} MB")
    print(f"  - Statistics saved to: {stats_file}")
    
    return stats

if __name__ == "__main__":
    collect_python_code()

