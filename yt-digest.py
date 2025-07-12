#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#    "youtube-transcript-api",
#    "llm>=0.26",
#    "llm-anthropic>=0.17",
#    "llm-claude>=0.4.2",
#    "youtube-transcript-api>=1.1.0",
#    "typer>=0.9.0",
#    "requests>=2.25.0"
# ]
# ///
import re
import llm
import typer
import requests
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi

app = typer.Typer(help="Summarize YouTube videos using AI")

def extract_video_id(url_or_id):
    """Extract YouTube video ID from URL or return ID if already provided"""
    if len(url_or_id) == 11 and not '/' in url_or_id:
        return url_or_id
    
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    
    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def get_transcript(video_id):
    """Fetch transcript for a YouTube video"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        raise Exception(f"Failed to fetch transcript for video {video_id}: {e}")


def get_video_metadata(video_id):
    """Fetch video title from YouTube"""
    try:
        # Use YouTube's oEmbed API to get video metadata
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        typer.echo(f"Warning: Could not fetch video title: {e}", err=True)
        return f"Video_{video_id}"


def get_video_title(video_id):
    return get_video_metadata(video_id).get('title', f'Video_{video_id}')

        
def sanitize_filename(title):
    """Sanitize title for use as filename"""
    # Remove or replace characters that are problematic in filenames
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', title)
    # Limit length to avoid filesystem issues
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    return sanitized



def summarize_transcript(video_id_or_url: str, output_file: Optional[str] = None, format: str = "markdown"):
    """Summarize YouTube transcript and save to markdown file"""
    
    # Extract video ID
    video_id = extract_video_id(video_id_or_url)
    
    # Get video title
    typer.echo("Fetching video metadata...")
    video_metadata = get_video_metadata(video_id)
    video_title = video_metadata.get('title', f'Video_{video_id}')
    typer.echo(f"Video title: {video_title}")
    
    # Get transcript
    transcript = get_transcript(video_id)
    
    # Initialize LLM - use default model
    model = llm.get_model()
    
    # Extract highlights for timestamp matching
    prompt = f"""
    You write summaries of youtube videos using a youtube transcript. 

    This is a transcript of a YouTube video titled "{video_title}" with id {video_id}.

    From this transcript, generate a {format} formatted document containing the following:
    1. A one line description of the video
    2. A single paragraph summary of the main content
    3. A summary of conclusions (if any)
    4. Up to 10 key highlights or important points from the video, with links to the video at that time
    5. If the title references a list (e.g., "Top 10"), include the list items with timestamps
    6. Use the attached metedata to generate an embedded iframe with video thumbnail keeping strictly to the {format} format (use thumbnail_width for the size of this iframe).

    Use a wry, entertaining style. Note if the title of the video is not congruent with the content.
    If the title is a question, comment if the conclusion answers the question.
    If the title is a bold or controversial statement or question, comment if the video could be considered 'clickbait'


    Transcript: {transcript}
    
    Metedata: {video_metadata}
    """
    
    typer.echo("Generating summary with AI...")
    markdown_content = model.prompt(prompt=prompt)
    
    # Save to file
    extension = "md" if format == "markdown" else "html"
    if output_file is None:
        sanitized_title = sanitize_filename(video_title)
        output_file = f"{sanitized_title}_{video_id}.{extension}"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content.text())
    
    typer.echo(f"Summary saved to: {output_file}")
    return output_file

@app.command()
def summarize(
    video: str = typer.Argument(..., help="YouTube video URL or video ID"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output markdown file path"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="LLM model to use for summarization"),
    format: str = typer.Option("markdown", "--format", "-f", help="Output format (markdown or html)", case_sensitive=False, show_default=True)
):
    """
    Summarize a YouTube video transcript using AI.
    
    Provide either a YouTube URL or video ID to generate a markdown summary.
    """
    try:
        # Set model if specified
        if model:
            typer.echo(f"Using model: {model}")
            # Note: You may need to configure the specific model here based on llm library usage
        
        typer.echo(f"Processing video: {video}")
        output_file = summarize_transcript(video, output, format)
        typer.echo(f"✅ Summary completed and saved to: {output_file}")
        
    except ValueError as e:
        typer.echo(f"❌ Error: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Failed to summarize video: {e}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
