import os
import logging
from typing import Literal
import yt_dlp

# Constants
DOWNLOAD_PATH = "downloads"
MEDIA_TYPE: Literal["video", "audio"] = "video"
MEDIA_QUALITY = "best"
SUPPORTED_MEDIA_TYPES = ("video", "audio")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sanitize_filename(filename: str) -> str:
    """Remove illegal characters from filenames.

    Sanitize the provided filename by removing characters that are not alphanumeric,
    spaces, hyphens, or underscores.

    :param filename:    The input filename to be sanitized.
    :return:            A sanitized version of the filename with only valid characters.
    """
    return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_'))


def select_video_quality(quality_input: str) -> str:
    """Convert user input into a valid yt-dlp quality format.

    This function checks if the user input is a digit, representing a maximum video height.
    If it is, it constructs a yt-dlp quality format string for the best video below or equal
    to the specified height, along with the best available audio.
    If the input is not a digit, it returns the input as a valid yt-dlp quality string (converted to lowercase).

    :param quality_input:   The quality input from the user, either a digit or a yt-dlp quality string.
    :return:                A yt-dlp compatible quality format string based on the user input.
    """
    if quality_input.isdigit():
        return f"bestvideo[height<={quality_input}]+bestaudio/best"
    return quality_input.lower()


def download_media(url, quality=MEDIA_QUALITY, download_path=DOWNLOAD_PATH, media_type=MEDIA_TYPE, ) -> None:
    """Download media from a URL using yt-dlp.

    This function supports downloading both audio and video content. For audio,
    it will extract the best audio format and convert it to MP3. For video, it will
    allow selection of quality based on user input (either a specific resolution or
    predefined options). The media is downloaded to the specified directory, and
    any required subdirectories are created if they do not exist.

    :param url:             The URL of the media to download (e.g., a YouTube or Facebook URL).
    :param quality:         The desired video quality (e.g., 'best', '720', '480'). Defaults to 'best'.
    :param download_path:   The directory path where the media will be saved. Defaults to a predefined path.
    :param media_type:      The type of media to download, either 'audio' or 'video'. Defaults to 'video'.
    :raises:
        ValueError: If an unsupported media type is provided.
        yt_dlp.utils.DownloadError: If yt-dlp encounters an issue during the download process.
        Exception: If an unexpected error occurs.
    """
    try:
        os.makedirs(download_path, exist_ok=True)

        if media_type not in SUPPORTED_MEDIA_TYPES:
            raise ValueError(f"Unsupported media type: {media_type}")

        ydl_opts = {
            "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
            "writethumbnail": False,
            "noplaylist": True,
        }

        if media_type == "audio":
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            })
        else:  # video
            ydl_opts["format"] = select_video_quality(quality)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            logger.info("Download completed successfully!")

    except yt_dlp.utils.DownloadError as e:
        logger.error(f"Download failed: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    try:
        url = input("Enter the video URL: ").strip()
        if not url:
            raise ValueError("URL cannot be empty.")

        media_type = (
                input(f"Choose media type ({'/'.join(SUPPORTED_MEDIA_TYPES)}) [{MEDIA_TYPE}]: ")
                .strip()
                .lower() or MEDIA_TYPE
        )

        media_quality = MEDIA_QUALITY
        if media_type == "video":
            quality_input = input(
                f"Choose quality (best/worst/720/480/360) [{MEDIA_QUALITY}]: ").strip() or MEDIA_QUALITY
            media_quality = select_video_quality(quality_input)

        download_media(url, media_quality, media_type=media_type)

    except KeyboardInterrupt:
        logger.info("\nDownload cancelled by user.")
    except Exception as e:
        logger.error(f"Error: {e}")
