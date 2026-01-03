"""
Desktop Cleaner Module

This module provides automated desktop cleaning functionality to help users
organize and clean their desktop directories. It can:
- Organize files into category-based folders
- Remove duplicate files
- Delete temporary and system files
- Generate cleanup reports

Author: Demo Project Team
Version: 1.0.0
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict
import hashlib


class DesktopCleaner:
    """
    Automated Desktop Cleaner class for organizing and cleaning desktop directories.

    This class provides utilities to organize files, remove duplicates,
    and manage temporary files on the desktop.
    """

    # File extensions grouped by category
    FILE_CATEGORIES = {
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".xls", ".ppt", ".pptx"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv", ".m4v"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".m4a", ".wma", ".ogg"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Executables": [".exe", ".msi", ".app", ".dmg"],
        "Code": [".py", ".js", ".java", ".cpp", ".c", ".html", ".css", ".json"],
    }

    def __init__(self, desktop_path: str = None):
        """
        Initialize the DesktopCleaner.

        Args:
            desktop_path (str): Path to the desktop directory.
                                If None, uses the user's default desktop path.
        """
        if desktop_path is None:
            # Default to user's desktop
            if os.name == 'nt':  # Windows
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            else:  # Unix-like
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        self.desktop_path = Path(desktop_path)
        self.cleanup_report = {}

    def get_file_category(self, filename: str) -> str:
        """
        Determine the category of a file based on its extension.

        Args:
            filename (str): Name of the file

        Returns:
            str: Category name, or "Other" if no matching category
        """
        file_extension = Path(filename).suffix.lower()
        for category, extensions in self.FILE_CATEGORIES.items():
            if file_extension in extensions:
                return category
        return "Other"

    def organize_files(self, dry_run: bool = True) -> Dict[str, List[str]]:
        """
        Organize files on the desktop into category-based folders.

        Args:
            dry_run (bool): If True, only simulate the operation without making changes.
                           If False, actually move files.

        Returns:
            Dict[str, List[str]]: Dictionary mapping categories to lists of organized files
        """
        organized_files = defaultdict(list)

        if not self.desktop_path.exists():
            return organized_files

        for item in self.desktop_path.iterdir():
            if item.is_file():
                category = self.get_file_category(item.name)
                organized_files[category].append(item.name)

                if not dry_run:
                    category_folder = self.desktop_path / category
                    category_folder.mkdir(exist_ok=True)

                    dest_path = category_folder / item.name
                    # Handle file conflicts
                    if dest_path.exists():
                        base_name = item.stem
                        extension = item.suffix
                        counter = 1
                        while dest_path.exists():
                            new_name = f"{base_name}_{counter}{extension}"
                            dest_path = category_folder / new_name
                            counter += 1

                    shutil.move(str(item), str(dest_path))

        return dict(organized_files)

    def find_duplicate_files(self) -> Dict[str, List[Path]]:
        """
        Find duplicate files on the desktop based on file hash.

        Returns:
            Dict[str, List[Path]]: Dictionary mapping file hashes to lists of duplicate file paths
        """
        file_hashes = defaultdict(list)

        if not self.desktop_path.exists():
            return {}

        for item in self.desktop_path.rglob("*"):
            if item.is_file():
                try:
                    file_hash = self._get_file_hash(item)
                    file_hashes[file_hash].append(item)
                except (OSError, IOError):
                    # Skip files that can't be read
                    continue

        # Return only duplicates (files with hash count > 1)
        duplicates = {hash_val: files for hash_val, files in file_hashes.items() if len(files) > 1}
        return duplicates

    def _get_file_hash(self, filepath: Path, chunk_size: int = 8192) -> str:
        """
        Calculate SHA256 hash of a file.

        Args:
            filepath (Path): Path to the file
            chunk_size (int): Size of chunks to read (default 8192 bytes)

        Returns:
            str: SHA256 hash of the file
        """
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    def remove_temp_files(self, dry_run: bool = True) -> List[str]:
        """
        Remove temporary and system files from the desktop.

        Args:
            dry_run (bool): If True, only simulate the operation without making changes.

        Returns:
            List[str]: List of removed files
        """
        temp_patterns = [".tmp", ".temp", "~", ".bak", ".cache", "thumbs.db"]
        removed_files = []

        if not self.desktop_path.exists():
            return removed_files

        for item in self.desktop_path.iterdir():
            should_remove = (
                item.name.lower().startswith("~") or
                any(item.name.lower().endswith(pattern) for pattern in temp_patterns) or
                item.name.lower() == "thumbs.db"
            )

            if item.is_file() and should_remove:
                removed_files.append(item.name)
                if not dry_run:
                    item.unlink()

        return removed_files

    def get_desktop_stats(self) -> Dict:
        """
        Get statistics about the desktop directory.

        Returns:
            Dict: Dictionary containing desktop statistics
        """
        stats = {
            "total_files": 0,
            "total_folders": 0,
            "total_size_bytes": 0,
            "file_count_by_category": defaultdict(int),
            "largest_files": []
        }

        if not self.desktop_path.exists():
            return stats

        file_sizes = []

        for item in self.desktop_path.iterdir():
            if item.is_file():
                stats["total_files"] += 1
                file_size = item.stat().st_size
                stats["total_size_bytes"] += file_size
                file_sizes.append((item.name, file_size))

                category = self.get_file_category(item.name)
                stats["file_count_by_category"][category] += 1
            elif item.is_dir():
                stats["total_folders"] += 1

        # Get top 5 largest files
        file_sizes.sort(key=lambda x: x[1], reverse=True)
        stats["largest_files"] = file_sizes[:5]

        return stats

    def generate_cleanup_report(self) -> str:
        """
        Generate a comprehensive cleanup report.

        Returns:
            str: Formatted cleanup report
        """
        stats = self.get_desktop_stats()

        report = []
        report.append("=" * 60)
        report.append("DESKTOP CLEANUP REPORT")
        report.append("=" * 60)
        report.append(f"Desktop Path: {self.desktop_path}")
        report.append("")

        report.append("STATISTICS:")
        report.append(f"  Total Files: {stats['total_files']}")
        report.append(f"  Total Folders: {stats['total_folders']}")
        report.append(f"  Total Size: {self._format_size(stats['total_size_bytes'])}")
        report.append("")

        if stats['file_count_by_category']:
            report.append("FILES BY CATEGORY:")
            for category, count in sorted(stats['file_count_by_category'].items()):
                report.append(f"  {category}: {count} files")
            report.append("")

        if stats['largest_files']:
            report.append("TOP 5 LARGEST FILES:")
            for filename, size in stats['largest_files']:
                report.append(f"  {filename}: {self._format_size(size)}")
            report.append("")

        duplicates = self.find_duplicate_files()
        if duplicates:
            report.append(f"DUPLICATE FILES FOUND: {len(duplicates)}")
            for i, (hash_val, files) in enumerate(list(duplicates.items())[:3]):
                report.append(f"  Duplicate Group {i+1}: {len(files)} files")
            report.append("")

        report.append("=" * 60)
        return "\n".join(report)

    @staticmethod
    def _format_size(bytes_size: int) -> str:
        """
        Format bytes to human-readable size.

        Args:
            bytes_size (int): Size in bytes

        Returns:
            str: Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024
        return f"{bytes_size:.2f} TB"


def organize_desktop(desktop_path: str = None, dry_run: bool = True) -> Dict:
    """
    Convenience function to organize desktop files.

    Args:
        desktop_path (str): Path to the desktop directory
        dry_run (bool): If True, simulate without making changes

    Returns:
        Dict[str, List[str]]: Organized files by category
    """
    cleaner = DesktopCleaner(desktop_path)
    return cleaner.organize_files(dry_run=dry_run)


def get_desktop_report(desktop_path: str = None) -> str:
    """
    Convenience function to get desktop cleanup report.

    Args:
        desktop_path (str): Path to the desktop directory

    Returns:
        str: Cleanup report
    """
    cleaner = DesktopCleaner(desktop_path)
    return cleaner.generate_cleanup_report()

