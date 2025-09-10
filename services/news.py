import feedparser
from config import RSS_FEEDS, NEWS_PER_POST, CHANNEL_LINK


def _extract_image(entry):
    """Try to extract an image URL from RSS entry."""
    if 'media_content' in entry and entry.media_content:
        return entry.media_content[0].get('url')
    if 'media_thumbnail' in entry and entry.media_thumbnail:
        return entry.media_thumbnail[0].get('url')
    if 'links' in entry:
        for link in entry.links:
            if link.get('type', '').startswith('image'):
                return link.get('href')
    summary = entry.get('summary', '')
    start = summary.find('<img')
    if start != -1:
        src_idx = summary.find('src=', start)
        if src_idx != -1:
            quote = summary[src_idx + 4]
            end = summary.find(quote, src_idx + 5)
            if end != -1:
                return summary[src_idx + 5:end]
    return None


def fetch_latest_news():
    """Return a list of dicts: [{title, link, image}] up to NEWS_PER_POST from multiple feeds."""
    items = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        if not feed.entries:
            continue
        for e in feed.entries:
            title = e.get('title')
            link = e.get('link')
            image = _extract_image(e)
            items.append({'title': title, 'link': link, 'image': image})
            if len(items) >= NEWS_PER_POST:
                break
        if len(items) >= NEWS_PER_POST:
            break
    return items[:NEWS_PER_POST]


def format_news_caption(news_items):
    """Create HTML caption for a news post."""
    lines = ["📰 <b>Crypto News👇</b>\n"]
    for idx, it in enumerate(news_items, start=1):
        title = it.get('title', 'No title')
        link = it.get('link', '')
        lines.append(f"{idx}. <b>{title}</b>\n🔗 <a href=\"{link}\">Link</a>\n")
    lines.append("\n#crypto #news")
    lines.append(f"\n<a href='{CHANNEL_LINK}'>Crypto News Daily</a>")
    return "\n".join(lines)
