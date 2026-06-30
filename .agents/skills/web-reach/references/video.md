# Video & audio — transcripts

The valuable thing from a video is usually its **transcript**. YouTube has made
this harder; there are three paths, in order of preference by environment.

## Path A — yt-dlp (best when YouTube is reachable and yt-dlp is installed)

```bash
command -v yt-dlp || pip install -q yt-dlp        # install if missing
# auto/!manual captions to a file, no video download:
yt-dlp --skip-download --write-auto-sub --write-sub --sub-lang "en.*" \
       --sub-format vtt -o "/tmp/yt.%(ext)s" "https://www.youtube.com/watch?v=<id>"
cat /tmp/yt*.vtt
```

Strip the VTT timestamps to get clean text. yt-dlp also prints metadata
(`--print title`, `--print description`).

## Path B — captionTracks from the watch page (keyless, no yt-dlp)

When `youtube.com` is reachable but yt-dlp is absent:

```bash
# 1) fetch the watch page, pull the caption track URL
curl -s "https://www.youtube.com/watch?v=<id>" \
 | grep -o '"captionTracks":\[[^]]*\]'        # contains baseUrl entries
# 2) fetch that baseUrl (it returns timed XML); add &fmt=json3 for JSON
curl -s "<baseUrl>&fmt=json3"
```

Parse the `events[].segs[].utf8` fields (json3) or the `<text>` nodes (XML) and
join them into a transcript.

## Path C — a transcript backend (when YouTube is blocked on this egress)

Some environments block `youtube.com` entirely (the watch page returns a tiny
egress-policy body). yt-dlp and the captionTracks method both fail there because
both must reach YouTube. Fall back to a service:

- ScrapeCreators / Supadata / Apify "YouTube transcript" actors
  (keyed by the env var `doctor.py` detects).
- As a last resort, the host's `web_search` may surface a third-party transcript
  page that `fetch.py` can then open.

Confirm reachability first: `doctor.py` shows `youtube_direct` reachable/blocked.

## Finding videos and channel uploads

- Discovery: host `web_search` for the topic, or YouTube search results page via
  `fetch.py` (parse the embedded `ytInitialData`).
- A channel's uploads as a feed (no key):
  `https://www.youtube.com/feeds/videos.xml?channel_id=<channelId>` → `feed.py`.

## Podcasts

Most podcasts publish an RSS feed with episode audio enclosures — use `feed.py`
to list episodes. For a transcript of an episode, check the show notes (often
linked in the feed) or transcribe the audio locally with ffmpeg + a speech model
if one is available; this is heavy, so prefer an existing transcript.

## Copyright

Transcripts are copyrighted. Summarize and quote short attributed snippets;
never reproduce a full transcript verbatim.
