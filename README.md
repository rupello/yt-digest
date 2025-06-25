# YT Summary

A command-line tool that uses AI to generate markdown summaries of YouTube videos from their transcripts.

## Usage

```
 Usage: yt-digest.py [OPTIONS] VIDEO

 Summarize a YouTube video transcript using AI.

 Provide either a YouTube URL or video ID to generate a markdown summary.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    video      TEXT  YouTube video URL or video ID [default: None] [required]                                         │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output              -o      TEXT  Output markdown file path [default: None]                                          │
│ --model               -m      TEXT  LLM model to use for summarization [default: None]                                 │
│ --install-completion                Install completion for the current shell.                                          │
│ --show-completion                   Show completion for the current shell, to copy it or customize the installation.   │
│ --help                              Show this message and exit.                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```


## Installation

Requires `uv` then:

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

## License

This project is open source. See the license file for details.
