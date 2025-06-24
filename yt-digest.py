#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#    "youtube-transcript-api",
#    "llm>=0.26",
#    "llm-anthropic>=0.17",
#    "llm-claude>=0.4.2",
#    "youtube-transcript-api>=1.1.0",
#    "typer>=0.9.0"
# ]
# ///
import re
import llm
import typer
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



def summarize_transcript(video_id_or_url: str, output_file: Optional[str] = None):
    """Summarize YouTube transcript and save to markdown file"""
    
    # Extract video ID
    video_id = extract_video_id(video_id_or_url)
    
    # Get transcript
    transcript = get_transcript(video_id)
    
    # Initialize LLM - use default model
    model = llm.get_model()
    
    # Extract highlights for timestamp matching
    prompt = f"""
    This is a transcript of a YouTube video with id {video_id}.
    From this transcript, generate a markdown document containing the following:
    1. A one line description of the video
    2. A single paragraph summary of the main content
    3. A summary of conclusions (if any)
    4. Up to 5 key highlights or important points from the video, with links to the video at that time

    Transcript: {transcript}
    """
    
    typer.echo("Generating summary with AI...")
    markdown_content = model.prompt(prompt=prompt)
    
    # Save to file
    if output_file is None:
        output_file = f"youtube_summary_{video_id}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content.text())
    
    typer.echo(f"Summary saved to: {output_file}")
    return output_file

@app.command()
def summarize(
    video: str = typer.Argument(..., help="YouTube video URL or video ID"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output markdown file path"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="LLM model to use for summarization")
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
        output_file = summarize_transcript(video, output)
        typer.echo(f"✅ Summary completed and saved to: {output_file}")
        
    except ValueError as e:
        typer.echo(f"❌ Error: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Failed to summarize video: {e}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
