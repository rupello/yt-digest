# YT Summary

A command-line tool that uses AI to generate markdown summaries of YouTube videos from their transcripts.

## Features

- Extract transcripts from YouTube videos using video URLs or IDs
- Generate AI-powered summaries with structured markdown output
- Support for multiple LLM models (Anthropic Claude, etc.)
- Automatic timestamp linking for key highlights
- Clean, readable markdown output format

## Installation

Install the project dependencies:

```bash
uv sync
```

## Usage

Summarize a YouTube video by providing either a URL or video ID:

```bash
uv run yt-digest.py summarize "https://www.youtube.com/watch?v=VIDEO_ID"
```

Or use just the video ID:

```bash
uv run yt-digest.py summarize VIDEO_ID
```

### Options

- `--output, -o`: Specify output file path (default: `youtube_summary_{video_id}.md`)
- `--model, -m`: Choose specific LLM model for summarization

### Examples

```bash
# Basic usage
uv run yt-digest.py summarize "https://youtu.be/dQw4w9WgXcQ"

# Custom output file
uv run yt-digest.py summarize VIDEO_ID --output my_summary.md

# Using specific model
uv run yt-digest.py summarize VIDEO_ID --model claude-3-sonnet
```

## Output Format

The generated markdown file includes:

1. **One-line description** of the video
2. **Summary paragraph** of the main content
3. **Conclusions** (if applicable)
4. **Key highlights** (up to 5) with timestamp links back to the video

## Dependencies

- **llm**: Core LLM interface library
- **llm-anthropic**: Anthropic Claude model support
- **llm-claude**: Additional Claude model integration
- **youtube-transcript-api**: YouTube transcript extraction
- **typer**: Command-line interface framework

## Requirements

- Python 3.12+
- Valid YouTube videos with available transcripts
- Configured LLM API access (for AI summarization)

## License

This project is open source. See the license file for details.
