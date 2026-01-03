"""Unit tests for desktop cleaner functionality"""

import pytest
import tempfile
import shutil
from pathlib import Path
from demo_app.desktop_cleaner import DesktopCleaner, organize_desktop, get_desktop_report


class TestDesktopCleanerInit:
    """Tests for DesktopCleaner initialization."""

    def test_init_with_custom_path(self):
        """Test initialization with a custom path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cleaner = DesktopCleaner(temp_dir)
            assert cleaner.desktop_path == Path(temp_dir)

    def test_init_with_none_path(self):
        """Test initialization with None path (default desktop)."""
        cleaner = DesktopCleaner()
        assert cleaner.desktop_path is not None


class TestGetFileCategory:
    """Tests for file category detection."""

    def test_document_category(self):
        """Test detection of document files."""
        cleaner = DesktopCleaner()
        assert cleaner.get_file_category("file.pdf") == "Documents"
        assert cleaner.get_file_category("file.docx") == "Documents"
        assert cleaner.get_file_category("file.txt") == "Documents"

    def test_image_category(self):
        """Test detection of image files."""
        cleaner = DesktopCleaner()
        assert cleaner.get_file_category("photo.jpg") == "Images"
        assert cleaner.get_file_category("picture.png") == "Images"

    def test_video_category(self):
        """Test detection of video files."""
        cleaner = DesktopCleaner()
        assert cleaner.get_file_category("movie.mp4") == "Videos"
        assert cleaner.get_file_category("video.mkv") == "Videos"

    def test_audio_category(self):
        """Test detection of audio files."""
        cleaner = DesktopCleaner()
        assert cleaner.get_file_category("song.mp3") == "Audio"
        assert cleaner.get_file_category("music.wav") == "Audio"

    def test_other_category(self):
        """Test detection of unknown file types."""
        cleaner = DesktopCleaner()
        assert cleaner.get_file_category("file.unknown") == "Other"
        assert cleaner.get_file_category("randomfile") == "Other"

    def test_case_insensitive_detection(self):
        """Test that category detection is case-insensitive."""
        cleaner = DesktopCleaner()
        assert cleaner.get_file_category("FILE.PDF") == "Documents"
        assert cleaner.get_file_category("photo.JPG") == "Images"


class TestOrganizeFiles:
    """Tests for file organization functionality."""

    def test_organize_files_dry_run(self):
        """Test file organization in dry-run mode."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test files
            (temp_path / "file1.pdf").touch()
            (temp_path / "photo.jpg").touch()
            (temp_path / "song.mp3").touch()

            cleaner = DesktopCleaner(temp_dir)
            organized = cleaner.organize_files(dry_run=True)

            # Verify organization mapping
            assert "Documents" in organized
            assert "Images" in organized
            assert "Audio" in organized

            # Verify files are still in original location
            assert (temp_path / "file1.pdf").exists()
            assert (temp_path / "photo.jpg").exists()

    def test_organize_files_actual(self):
        """Test actual file organization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test files
            (temp_path / "file1.pdf").touch()
            (temp_path / "photo.jpg").touch()

            cleaner = DesktopCleaner(temp_dir)
            organized = cleaner.organize_files(dry_run=False)

            # Verify files were moved
            assert (temp_path / "Documents" / "file1.pdf").exists()
            assert (temp_path / "Images" / "photo.jpg").exists()

    def test_organize_files_with_duplicates(self):
        """Test file organization with duplicate filenames."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test files with same name
            (temp_path / "file.pdf").write_text("content1")
            (temp_path / "file.pdf").write_text("content1")  # This overwrites

            cleaner = DesktopCleaner(temp_dir)
            cleaner.organize_files(dry_run=False)

            # Verify document folder was created
            assert (temp_path / "Documents").exists()

    def test_organize_empty_directory(self):
        """Test organization of an empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cleaner = DesktopCleaner(temp_dir)
            organized = cleaner.organize_files(dry_run=True)

            assert len(organized) == 0


class TestFindDuplicates:
    """Tests for duplicate file detection."""

    def test_find_no_duplicates(self):
        """Test when there are no duplicates."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create unique files
            (temp_path / "file1.txt").write_text("content1")
            (temp_path / "file2.txt").write_text("content2")

            cleaner = DesktopCleaner(temp_dir)
            duplicates = cleaner.find_duplicate_files()

            assert len(duplicates) == 0

    def test_find_duplicates(self):
        """Test detection of duplicate files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create duplicate files
            content = "same content"
            (temp_path / "file1.txt").write_text(content)
            (temp_path / "file2.txt").write_text(content)

            cleaner = DesktopCleaner(temp_dir)
            duplicates = cleaner.find_duplicate_files()

            assert len(duplicates) == 1
            files = list(duplicates.values())[0]
            assert len(files) == 2

    def test_find_duplicates_empty_directory(self):
        """Test duplicate detection in empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cleaner = DesktopCleaner(temp_dir)
            duplicates = cleaner.find_duplicate_files()

            assert len(duplicates) == 0


class TestRemoveTempFiles:
    """Tests for temporary file removal."""

    def test_remove_temp_files_dry_run(self):
        """Test temp file removal in dry-run mode."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create temp files
            (temp_path / "file.tmp").touch()
            (temp_path / "file.bak").touch()
            (temp_path / "normalfile.txt").touch()

            cleaner = DesktopCleaner(temp_dir)
            removed = cleaner.remove_temp_files(dry_run=True)

            assert len(removed) == 2
            assert (temp_path / "file.tmp").exists()
            assert (temp_path / "normalfile.txt").exists()

    def test_remove_temp_files_actual(self):
        """Test actual temp file removal."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create temp files
            (temp_path / "file.tmp").touch()
            (temp_path / "file.bak").touch()
            (temp_path / "normalfile.txt").touch()

            cleaner = DesktopCleaner(temp_dir)
            removed = cleaner.remove_temp_files(dry_run=False)

            assert len(removed) == 2
            assert not (temp_path / "file.tmp").exists()
            assert (temp_path / "normalfile.txt").exists()

    def test_remove_no_temp_files(self):
        """Test removal when no temp files exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            (temp_path / "normalfile.txt").touch()

            cleaner = DesktopCleaner(temp_dir)
            removed = cleaner.remove_temp_files(dry_run=True)

            assert len(removed) == 0


class TestDesktopStats:
    """Tests for desktop statistics."""

    def test_get_desktop_stats(self):
        """Test getting desktop statistics."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test files
            (temp_path / "file1.pdf").write_text("a" * 1000)
            (temp_path / "file2.jpg").write_text("b" * 2000)
            (temp_path / "subdir").mkdir()

            cleaner = DesktopCleaner(temp_dir)
            stats = cleaner.get_desktop_stats()

            assert stats["total_files"] == 2
            assert stats["total_folders"] == 1
            assert stats["total_size_bytes"] == 3000
            assert stats["file_count_by_category"]["Documents"] == 1
            assert stats["file_count_by_category"]["Images"] == 1

    def test_get_desktop_stats_largest_files(self):
        """Test that largest files are correctly identified."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create files of different sizes
            (temp_path / "small.txt").write_text("a" * 100)
            (temp_path / "medium.txt").write_text("b" * 500)
            (temp_path / "large.txt").write_text("c" * 1000)

            cleaner = DesktopCleaner(temp_dir)
            stats = cleaner.get_desktop_stats()

            assert len(stats["largest_files"]) == 3
            assert stats["largest_files"][0][0] == "large.txt"
            assert stats["largest_files"][1][0] == "medium.txt"

    def test_get_desktop_stats_empty_directory(self):
        """Test stats for empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cleaner = DesktopCleaner(temp_dir)
            stats = cleaner.get_desktop_stats()

            assert stats["total_files"] == 0
            assert stats["total_folders"] == 0
            assert stats["total_size_bytes"] == 0


class TestGenerateReport:
    """Tests for report generation."""

    def test_generate_cleanup_report(self):
        """Test cleanup report generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test files
            (temp_path / "file1.pdf").touch()
            (temp_path / "file2.jpg").touch()

            cleaner = DesktopCleaner(temp_dir)
            report = cleaner.generate_cleanup_report()

            assert "DESKTOP CLEANUP REPORT" in report
            assert "Total Files: 2" in report
            assert "Files by Category" in report or "FILES BY CATEGORY" in report

    def test_generate_report_empty_directory(self):
        """Test report generation for empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cleaner = DesktopCleaner(temp_dir)
            report = cleaner.generate_cleanup_report()

            assert "DESKTOP CLEANUP REPORT" in report
            assert "Total Files: 0" in report


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_organize_desktop_function(self):
        """Test organize_desktop convenience function."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "file.pdf").touch()

            organized = organize_desktop(temp_dir, dry_run=True)

            assert "Documents" in organized

    def test_get_desktop_report_function(self):
        """Test get_desktop_report convenience function."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "file.pdf").touch()

            report = get_desktop_report(temp_dir)

            assert "DESKTOP CLEANUP REPORT" in report


class TestFormatSize:
    """Tests for size formatting utility."""

    def test_format_bytes(self):
        """Test formatting of byte sizes."""
        assert "B" in DesktopCleaner._format_size(100)
        assert "KB" in DesktopCleaner._format_size(1024 * 10)
        assert "MB" in DesktopCleaner._format_size(1024 * 1024 * 10)
        assert "GB" in DesktopCleaner._format_size(1024 * 1024 * 1024 * 10)

