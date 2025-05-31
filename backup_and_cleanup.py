import os
import shutil
from pathlib import Path

# Important file patterns to preserve
IMPORTANT_PATTERNS = [
    '*.py',
    '*.tsx',
    '*.ts',
    '*.json',
    '*.yml',
    '*.yaml',
    '*.md',
    '*.env',
    'Dockerfile*',
    'docker-compose*',
    'requirements.txt',
    'package.json',
    'package-lock.json',
    'tsconfig.json',
    '.gitignore'
]

# Directories to check for unique files
DUPLICATE_DIRS = [
    'AI-interview-chatbot-main',
    'ai-interview-chatbot',
    'AI-interview-chatbot-clean'
]

# Create backup directory
backup_dir = Path('backup_files')
backup_dir.mkdir(exist_ok=True)

def is_important_file(file_path):
    """Check if file matches important patterns."""
    return any(file_path.match(pattern) for pattern in IMPORTANT_PATTERNS)

def backup_unique_files():
    """Backup unique files from duplicate directories."""
    for dup_dir in DUPLICATE_DIRS:
        if not Path(dup_dir).exists():
            continue
        
        print(f"Checking {dup_dir} for unique files...")
        for root, _, files in os.walk(dup_dir):
            for file in files:
                file_path = Path(root) / file
                if is_important_file(file_path):
                    # Create relative path for backup
                    rel_path = file_path.relative_to(dup_dir)
                    backup_path = backup_dir / dup_dir / rel_path
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy file to backup
                    shutil.copy2(file_path, backup_path)
                    print(f"Backed up: {file_path} -> {backup_path}")

def cleanup_duplicate_dirs():
    """Remove duplicate directories after backup."""
    for dup_dir in DUPLICATE_DIRS:
        if Path(dup_dir).exists():
            try:
                shutil.rmtree(dup_dir)
                print(f"Removed directory: {dup_dir}")
            except Exception as e:
                print(f"Error removing {dup_dir}: {e}")

def organize_frontend():
    """Organize frontend directories."""
    if Path('frontend').exists() and Path('frontend-new').exists():
        # Backup old frontend
        if any(Path('frontend').iterdir()):
            shutil.move('frontend', backup_dir / 'frontend_old')
            print("Backed up old frontend directory")
    
    # Rename frontend-new to frontend if it exists
    if Path('frontend-new').exists():
        if not Path('frontend').exists():
            shutil.move('frontend-new', 'frontend')
            print("Renamed frontend-new to frontend")

def main():
    print("Starting backup and cleanup process...")
    backup_unique_files()
    organize_frontend()
    cleanup_duplicate_dirs()
    print("Backup and cleanup completed!")

if __name__ == "__main__":
    main() 