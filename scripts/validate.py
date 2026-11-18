#!/usr/bin/env python3
"""Offline integrity checks; this does not test Clopos behavior."""
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit


def require(condition, message):
    if not condition:
        raise ValueError(message)


def workflow_citations(references):
    """Map primary-source URLs to the operational guides that cite them."""
    result = {}
    catalog_files = {'video-catalog.md', 'known-gaps.md', 'source-guide.md'}
    for md in references.glob('*.md'):
        if md.name in catalog_files:
            continue
        for url in re.findall(r'https://az\.help\.clopos\.com/az/article/[^\s)]+', md.read_text(encoding='utf-8')):
            result.setdefault(url, set()).add(md.name)
    return result


def validate(root):
    root = Path(root).resolve()
    skill = root / 'skills/clopos'
    entry = (skill / 'SKILL.md').read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---\n', entry, re.S)
    require(match, 'Missing YAML frontmatter')
    require(re.search(r'^name: clopos$', match.group(1), re.M), 'Invalid skill name')
    require(re.search(r'^description: .{30,}$', match.group(1), re.M), 'Missing description')
    require(len(entry.splitlines()) < 150, 'Entrypoint should stay compact')

    ui = (skill / 'agents/openai.yaml').read_text(encoding='utf-8')
    fields = dict(re.findall(r'^  (\w+): (".*")$', ui, re.M))
    fields = {key: json.loads(value) for key, value in fields.items()}
    require('$clopos' in fields.get('default_prompt', ''), 'Default prompt must invoke $clopos')
    require(25 <= len(fields.get('short_description', '')) <= 64, 'Invalid UI description length')

    for md in root.rglob('*.md'):
        content = md.read_text(encoding='utf-8')
        require(not re.search(r'\b(?:TODO|FIXME|TBD)\b', content), f'Unfinished scaffold: {md}')
        for target in re.findall(r'\]\(([^)]+)\)', content):
            if urlsplit(target).scheme or target.startswith('#'):
                continue
            path = (md.parent / target.split('#', 1)[0]).resolve()
            require(path.is_relative_to(root), f'Link leaves repository: {md}: {target}')
            require(path.exists(), f'Broken local link: {md}: {target}')

    registry = json.loads((skill / 'references/sources.json').read_text(encoding='utf-8'))
    retrieved_at = date.fromisoformat(registry['retrieved_at'])
    videos, playlists, articles = (registry[key] for key in ('videos', 'playlists', 'help_articles'))
    ids = {v['id'] for v in videos}
    require(len(ids) == len(videos), 'Duplicate video IDs')
    require(all(re.fullmatch(r'[\w-]{11}', i, re.ASCII) for i in ids), 'Invalid video ID')
    require(len({p['id'] for p in playlists}) == len(playlists), 'Duplicate playlists')
    require(len({a['url'] for a in articles}) == len(articles), 'Duplicate articles')
    for p in playlists:
        require(set(p['video_ids']) <= ids, f"Unknown playlist video: {p['id']}")
        require(len(set(p['video_ids'])) == len(p['video_ids']), 'Duplicate playlist membership')
    for v in videos:
        require(v['url'] == 'https://www.youtube.com/watch?v=' + v['id'], 'Video URL mismatch')
        require(set(v['playlist_ids']) == {p['id'] for p in playlists if v['id'] in p['video_ids']}, 'Membership mismatch')
        require(v['transcript_status'] in {'retrieved_and_reviewed', 'unavailable'}, 'Unknown evidence state')
        if v['transcript_status'] == 'unavailable':
            require(v['caption_language_code'] is None and v['quality'] == 'not_available', 'Unavailable transcript has invented metadata')
        require(not v['full_audiovisual_review'], 'Initial release must not imply full video review')

    expected = {
        'playlists': len(playlists),
        'unique_playlist_videos': len({i for p in playlists for i in p['video_ids']}),
        'channel_videos_feed': sum('videos' in v['channel_feeds'] for v in videos),
        'channel_shorts_feed': sum('shorts' in v['channel_feeds'] for v in videos),
        'unique_videos': len(videos),
        'transcripts_retrieved_and_reviewed': sum(v['transcript_status'] == 'retrieved_and_reviewed' for v in videos),
        'transcripts_unavailable': sum(v['transcript_status'] == 'unavailable' for v in videos),
        'full_audiovisual_reviews': sum(v['full_audiovisual_review'] for v in videos),
        'help_articles_text_retrieved': sum(a['text_retrieved'] for a in articles),
        'help_articles_used_in_workflows': sum(bool(a['used_in']) for a in articles),
    }
    require(registry['coverage'] == expected, 'Coverage totals do not match source records')
    article_urls = {a['url'] for a in articles}
    for md in (skill / 'references').glob('*.md'):
        text = md.read_text(encoding='utf-8')
        for url in re.findall(r'https://az\.help\.clopos\.com/az/article/[^\s)]+', text):
            require(url in article_urls, f'Unregistered help article: {url}')
        for video_id in re.findall(r'youtube\.com/watch\?v=([\w-]{11})', text):
            require(video_id in ids, f'Unregistered video: {video_id}')
    citations = workflow_citations(skill / 'references')
    for a in articles:
        declared = a['used_in']
        require(len(declared) == len(set(declared)), f"Duplicate citation locations: {a['url']}")
        require(set(declared) == citations.get(a['url'], set()), f"Article citation drift: {a['url']}")
        if 'last_checked_at' in a:
            require(date.fromisoformat(a['last_checked_at']) >= retrieved_at, f"Recheck precedes retrieval: {a['url']}")

    cases = json.loads((root / 'evals/cases.json').read_text(encoding='utf-8'))
    require(len({c['id'] for c in cases}) == len(cases), 'Duplicate evaluation IDs')
    require(len(cases) >= 8, 'Missing meaningful evaluation scenarios')
    for case in cases:
        require(all(case.get(k) for k in ('id', 'request', 'state', 'pass_criteria')), 'Incomplete evaluation')
        require(case['side_effects'] == 'none', 'Evaluations must be offline')
    print(f"PASS: skill, UI metadata, links, {len(videos)} videos, {len(articles)} articles, {len(cases)} evaluation fixtures")
    return expected


if __name__ == '__main__':
    try:
        validate(Path(__file__).resolve().parents[1])
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        raise SystemExit(f'FAIL: {exc}')
