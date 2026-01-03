# Desktop Cleaner Feature Documentation

## Overview

The **Automated Desktop Cleaner** is a powerful utility feature that helps users organize, analyze, and clean their desktop directories. It provides automated file organization, duplicate detection, temporary file removal, and comprehensive reporting capabilities.

## Features

### 1. **File Organization**
- Automatically categorizes files based on their extensions
- Organizes files into category-specific folders
- Supports 7+ file categories (Documents, Images, Videos, Audio, Archives, Executables, Code, Other)
- Handles file name conflicts with automatic renaming
- Dry-run mode to preview changes without making modifications

### 2. **Duplicate Detection**
- Identifies duplicate files using SHA256 file hashing
- Handles large files efficiently with chunked reading
- Returns all duplicates with their exact file paths
- Useful for freeing up storage space

### 3. **Temporary File Removal**
- Automatically identifies and removes temporary files
- Detects common temp file patterns (.tmp, .bak, .temp, etc.)
- Removes system files like thumbs.db
- Dry-run mode for safe preview

### 4. **Desktop Analysis & Reporting**
- Comprehensive desktop statistics (file count, total size, folder count)
- File categorization breakdown
- Identifies largest files on desktop
- Generates detailed cleanup reports

## Installation

The Desktop Cleaner is integrated into the demo_python_project. No additional dependencies required beyond the base Python environment.

```bash
# Install project dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

#### 1. Using the DesktopCleaner Class

```python
from demo_app import DesktopCleaner

# Initialize cleaner for user's desktop
cleaner = DesktopCleaner()

# Or specify a custom path
cleaner = DesktopCleaner("/path/to/directory")
```

#### 2. Organizing Files

```python
# Preview organization (dry-run)
organized_files = cleaner.organize_files(dry_run=True)
print(organized_files)
# Output: {'Documents': ['file.pdf'], 'Images': ['photo.jpg'], ...}

# Actually organize files
organized_files = cleaner.organize_files(dry_run=False)
```

#### 3. Finding Duplicates

```python
# Find all duplicate files
duplicates = cleaner.find_duplicate_files()

# duplicates structure:
# {
#     'hash123abc...': [Path('file1.txt'), Path('file2.txt')],
#     'hash456def...': [Path('photo1.jpg'), Path('photo2.jpg')]
# }

for file_hash, file_list in duplicates.items():
    print(f"Found {len(file_list)} duplicate files:")
    for file in file_list:
        print(f"  - {file.name}")
```

#### 4. Removing Temporary Files

```python
# Preview temp file removal (dry-run)
temp_files = cleaner.remove_temp_files(dry_run=True)
print(f"Would remove: {temp_files}")

# Actually remove temp files
temp_files = cleaner.remove_temp_files(dry_run=False)
print(f"Removed: {temp_files}")
```

#### 5. Getting Desktop Statistics

```python
# Get comprehensive desktop statistics
stats = cleaner.get_desktop_stats()

print(f"Total Files: {stats['total_files']}")
print(f"Total Folders: {stats['total_folders']}")
print(f"Total Size: {stats['total_size_bytes']} bytes")

# Files by category
for category, count in stats['file_count_by_category'].items():
    print(f"{category}: {count} files")

# Largest files
for filename, size in stats['largest_files']:
    print(f"{filename}: {size} bytes")
```

#### 6. Generating Reports

```python
# Generate comprehensive cleanup report
report = cleaner.generate_cleanup_report()
print(report)

# Output example:
# ============================================================
# DESKTOP CLEANUP REPORT
# ============================================================
# Desktop Path: /home/user/Desktop
#
# STATISTICS:
#   Total Files: 42
#   Total Folders: 5
#   Total Size: 2.45 GB
#
# FILES BY CATEGORY:
#   Documents: 15 files
#   Images: 12 files
#   Videos: 8 files
#   ...
```

### Convenience Functions

```python
from demo_app import organize_desktop, get_desktop_report

# Quick organization
organized = organize_desktop("/path/to/desktop", dry_run=True)

# Quick report generation
report = get_desktop_report("/path/to/desktop")
print(report)
```

## File Categories

The Desktop Cleaner automatically recognizes and organizes the following file types:

| Category | Extensions |
|----------|-----------|
| Documents | .pdf, .doc, .docx, .txt, .xlsx, .xls, .ppt, .pptx |
| Images | .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp |
| Videos | .mp4, .avi, .mkv, .mov, .flv, .wmv, .m4v |
| Audio | .mp3, .wav, .flac, .aac, .m4a, .wma, .ogg |
| Archives | .zip, .rar, .7z, .tar, .gz, .bz2 |
| Executables | .exe, .msi, .app, .dmg |
| Code | .py, .js, .java, .cpp, .c, .html, .css, .json |
| Other | All other file types |

## API Reference

### DesktopCleaner Class

#### `__init__(desktop_path: str = None)`
Initialize the Desktop Cleaner.

**Parameters:**
- `desktop_path` (str, optional): Path to the desktop directory. If None, uses the user's default desktop path.

#### `get_file_category(filename: str) -> str`
Determine the category of a file based on its extension.

**Parameters:**
- `filename` (str): Name of the file

**Returns:**
- (str): Category name

#### `organize_files(dry_run: bool = True) -> Dict[str, List[str]]`
Organize files into category-based folders.

**Parameters:**
- `dry_run` (bool): If True, only simulates without making changes

**Returns:**
- (Dict): Mapping of categories to file lists

#### `find_duplicate_files() -> Dict[str, List[Path]]`
Find duplicate files based on file hash.

**Returns:**
- (Dict): Mapping of file hashes to duplicate file paths

#### `remove_temp_files(dry_run: bool = True) -> List[str]`
Remove temporary and system files.

**Parameters:**
- `dry_run` (bool): If True, only simulates without making changes

**Returns:**
- (List): List of removed/would-be-removed files

#### `get_desktop_stats() -> Dict`
Get statistics about the desktop directory.

**Returns:**
- (Dict): Desktop statistics including file counts, sizes, and categories

#### `generate_cleanup_report() -> str`
Generate a comprehensive cleanup report.

**Returns:**
- (str): Formatted cleanup report

### Convenience Functions

#### `organize_desktop(desktop_path: str = None, dry_run: bool = True) -> Dict`
Quick function to organize desktop files.

#### `get_desktop_report(desktop_path: str = None) -> str`
Quick function to get desktop cleanup report.

## Examples

### Example 1: Complete Desktop Cleanup Workflow

```python
from demo_app import DesktopCleaner

# Initialize cleaner
cleaner = DesktopCleaner()

# Step 1: Generate a report
print(cleaner.generate_cleanup_report())

# Step 2: Find duplicates
duplicates = cleaner.find_duplicate_files()
if duplicates:
    print(f"Found {len(duplicates)} sets of duplicates")

# Step 3: Remove temp files (with confirmation)
temp_files = cleaner.remove_temp_files(dry_run=True)
if temp_files:
    print(f"Will remove {len(temp_files)} temp files")
    # User confirms...
    cleaner.remove_temp_files(dry_run=False)

# Step 4: Organize files
organized = cleaner.organize_files(dry_run=False)
print(f"Organized {sum(len(f) for f in organized.values())} files")
```

### Example 2: Storage Analysis

```python
from demo_app import DesktopCleaner

cleaner = DesktopCleaner()
stats = cleaner.get_desktop_stats()

# Find largest files
print("Top 5 Largest Files:")
for filename, size in stats['largest_files']:
    size_mb = size / (1024 * 1024)
    print(f"  {filename}: {size_mb:.2f} MB")

# Calculate storage by category
print("\nStorage by Category:")
# This would require enhanced stats method
```

### Example 3: Finding and Removing Duplicates

```python
from demo_app import DesktopCleaner

cleaner = DesktopCleaner()
duplicates = cleaner.find_duplicate_files()

for file_hash, files in duplicates.items():
    print(f"\nDuplicate Group ({len(files)} files):")
    for file in files:
        print(f"  {file}")
    
    # Keep the first, remove others (requires user confirmation)
    # for file in files[1:]:
    #     file.unlink()
```

## Safety Features

1. **Dry-Run Mode**: All destructive operations support dry-run mode for preview
2. **File Conflict Handling**: Automatic renaming when moving files with duplicate names
3. **Error Handling**: Graceful handling of inaccessible files
4. **Hash-Based Duplicate Detection**: Uses SHA256 for reliable duplicate identification

## Performance Considerations

- **Large Directories**: For directories with thousands of files, duplicate detection may take time
- **File Size**: Handles files of any size efficiently with chunked hashing
- **Memory**: Streaming approach ensures low memory usage

## Limitations

- Desktop path detection uses OS-specific paths (Windows, Linux, macOS supported)
- Requires read/write permissions on the desktop directory
- Some system-protected files may not be deletable

## Testing

The Desktop Cleaner includes comprehensive unit tests:

```bash
# Run all tests
pytest tests/test_desktop_cleaner.py -v

# Run specific test class
pytest tests/test_desktop_cleaner.py::TestDesktopCleanerInit -v

# Run with coverage
pytest tests/test_desktop_cleaner.py --cov=demo_app.desktop_cleaner
```

## Future Enhancements

- [ ] Scheduled automated cleanup
- [ ] Cloud integration (OneDrive, Google Drive sync cleanup)
- [ ] Custom category definition
- [ ] Advanced filtering and search
- [ ] Desktop cleanup history/undo functionality
- [ ] Multi-language support
- [ ] GUI dashboard
- [ ] Cleanup recommendations based on usage patterns

## Contributing

To contribute to the Desktop Cleaner feature:

1. Create a new branch for your feature
2. Write comprehensive tests
3. Update documentation
4. Submit a pull request

## License

This feature is part of the Demo Python Project and follows the same license terms.

## Support

For issues, feature requests, or questions about the Desktop Cleaner:

1. Check the existing documentation and examples
2. Review the test cases for usage patterns
3. Create an issue on GitHub with detailed information

