#!/usr/bin/env python3
"""
Verification script to check if the Snake AI project is properly set up.
Run this to verify all components are in place.
"""

import os
import sys
from pathlib import Path


def check_file(filepath, description=""):
    """Check if a file exists"""
    exists = os.path.isfile(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {filepath.ljust(50)} {description}")
    return exists


def check_dir(dirpath, description=""):
    """Check if a directory exists"""
    exists = os.path.isdir(dirpath)
    status = "✅" if exists else "❌"
    print(f"{status} {dirpath.ljust(50)} {description}")
    return exists


def verify_imports():
    """Verify all required imports work"""
    print("\n" + "="*70)
    print("CHECKING IMPORTS")
    print("="*70)
    
    imports_ok = True
    
    try:
        import numpy
        print("✅ numpy is installed")
    except ImportError:
        print("❌ numpy is NOT installed - run: pip install numpy")
        imports_ok = False
    
    try:
        import matplotlib
        print("✅ matplotlib is installed")
    except ImportError:
        print("❌ matplotlib is NOT installed - run: pip install matplotlib")
        imports_ok = False
    
    try:
        import pygame
        print("✅ pygame is installed")
    except ImportError:
        print("⚠️  pygame is NOT installed (optional) - run: pip install pygame")
    
    return imports_ok


def main():
    """Main verification function"""
    
    print("\n" + "="*70)
    print("SNAKE GAME AI - PROJECT VERIFICATION")
    print("="*70)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("\n" + "="*70)
    print("CHECKING DIRECTORY STRUCTURE")
    print("="*70)
    
    all_ok = True
    
    # Check directories
    dirs_to_check = [
        ("game/", "Game environment"),
        ("agent/", "AI agent"),
        ("training/", "Training scripts"),
        ("utils/", "Utility modules"),
        ("saved_models/", "Models storage"),
    ]
    
    for dir_path, desc in dirs_to_check:
        full_path = os.path.join(base_dir, dir_path)
        if not check_dir(full_path, desc):
            all_ok = False
    
    # Check files
    print("\n" + "="*70)
    print("CHECKING PYTHON FILES")
    print("="*70)
    
    files_to_check = [
        # Game module
        ("game/__init__.py", "Game module init"),
        ("game/snake_game.py", "Snake game implementation"),
        
        # Agent module
        ("agent/__init__.py", "Agent module init"),
        ("agent/q_agent.py", "Q-Learning agent"),
        
        # Training module
        ("training/__init__.py", "Training module init"),
        ("training/train.py", "Training script"),
        ("training/test.py", "Testing script"),
        
        # Utils module
        ("utils/__init__.py", "Utils module init"),
        ("utils/config.py", "Configuration"),
        ("utils/state_representation.py", "State encoding"),
        ("utils/visualization.py", "Visualization"),
        
        # Root files
        ("main.py", "Main entry point"),
        ("requirements.txt", "Dependencies"),
    ]
    
    for file_path, desc in files_to_check:
        full_path = os.path.join(base_dir, file_path)
        if not check_file(full_path, desc):
            all_ok = False
    
    # Check documentation
    print("\n" + "="*70)
    print("CHECKING DOCUMENTATION")
    print("="*70)
    
    docs = [
        ("README.md", "Main documentation"),
        ("GETTING_STARTED.md", "Quick start guide"),
        ("PROJECT_SUMMARY.md", "Project summary"),
        ("INDEX.md", "File index"),
        ("COMPLETION_REPORT.md", "Completion report"),
    ]
    
    for doc_file, desc in docs:
        full_path = os.path.join(base_dir, doc_file)
        if not check_file(full_path, desc):
            all_ok = False
    
    # Check imports
    imports_ok = verify_imports()
    
    # Summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    if all_ok and imports_ok:
        print("\n✅ ALL CHECKS PASSED!")
        print("\nYour Snake AI project is ready to use!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Start training: python training/train.py")
        print("3. Read guide: GETTING_STARTED.md")
        return 0
    elif all_ok and not imports_ok:
        print("\n⚠️  FILES OK, BUT MISSING DEPENDENCIES")
        print("\nFix with: pip install -r requirements.txt")
        return 1
    else:
        print("\n❌ SOME FILES ARE MISSING!")
        print("\nPlease ensure all files are created properly.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
