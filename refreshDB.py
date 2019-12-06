import podcastparser
import urllib.request
import pprint
from flaskpodcast import db, User, Podcast, Episode
from rss_links import rss_links


def remove_html(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


for rss in rss_links:
    parsed = podcastparser.parse(rss, urllib.request.urlopen(rss), 10)
    title = parsed.get('title')
    description = remove_html(parsed.get('description'))
    image = parsed.get('cover_url')
    link = parsed.get('link')

    podcast = Podcast.query.filter_by(link=parsed.get('link')).first()

    if(podcast is None):
        podcast = Podcast(title=title, description=description, image=image, link=link)
        db.session.add(podcast)
        db.session.commit()

    for episode in parsed.get('episodes'):
        episode_title = episode.get('title')
        episode_link = episode.get('link')
        episode_audio_url = episode.get('enclosures')[0]['url']
        episode_time_published = episode.get('published')
        episode_length = episode.get('total_time')
        episode_podcast = podcast

        episode = Episode.query.filter_by(audio_url=episode_audio_url).first()

        if(episode is None):
            episode = Episode(title=episode_title,
                                link=episode_link,
                                audio_url=episode_audio_url,
                                time_published=episode_time_published,
                                length=episode_length,
                                podcast=podcast)
            db.session.add(episode)

    db.session.commit()
    # pprint.pprint(parsed)
