from models import Article, HeaderSection, TitleSection, LeadSection, TextSection, ImageSection, MediaSection
from datetime import datetime
from time import sleep
import requests
import json
import bs4



ARTICLES_URL = 'https://mapping-test.fra1.digitaloceanspaces.com/data/list.json'

get_article_details_url = lambda article_id: f'https://mapping-test.fra1.digitaloceanspaces.com/data/articles/{article_id}.json'
get_article_media_url = lambda article_id: f'https://mapping-test.fra1.digitaloceanspaces.com/data/media/{article_id}.json'



def strip_text(html_text):
	text = bs4.BeautifulSoup(html_text, 'html.parser')
	return text.get_text()



def get_articles():
	articles = requests.get(ARTICLES_URL)
	articles_dict = articles.json()
	return articles_dict

def get_article_details(article_id):
	article_details_url = get_article_details_url(article_id)
	article_details = requests.get(article_details_url)
	article_details_dict = article_details.json()
	article_details_dict['url'] = article_details_url

	return article_details_dict

def get_article_media(article_id):
	article_media_url = get_article_media_url(article_id)
	article_media = requests.get(article_media_url)
	article_media_dict = article_media

	return article_media_dict



def mapped_article(article_id):
	article_details = get_article_details(article_id)
	article_pub_date = datetime.strptime(article_details['pub_date'], '%Y-%m-%d-%H;%M;%S')
	article_mod_date = datetime.strptime(article_details['mod_date'], '%Y-%m-%d-%H:%M:%S')

	if 'media' in [section['type'] for section in article_details['sections']]:
		article_media = get_article_media(article_id).json()
		article_media_dict = dict()

		for media in article_media:
			article_media_dict[media['id']] = media

	article_sections = []
	for section in article_details['sections']:
		if section['type'] == 'header':
			tmp_section = HeaderSection(
				type = section.get('type'),
				level = section.get('level'),
				text = strip_text(section.get('text'))
			)

			article_sections.append(tmp_section)

		elif section['type'] == 'title':
			tmp_section = TitleSection(
				type = section.get('type'),
				text = strip_text(section.get('text'))
			)

			article_sections.append(tmp_section)

		elif section['type'] == 'lead':
			tmp_section = LeadSection(
				type = section.get('type'),
				text = strip_text(section.get('text'))
			)

			article_sections.append(tmp_section)

		elif section['type'] == 'text':
			tmp_section = TextSection(
				type = section.get('type'),
				text = strip_text(section.get('text'))
			)

			article_sections.append(tmp_section)

		elif section['type'] == 'image':
			tmp_section = ImageSection(
				type = section.get('type'),
				url = section.get('url'),
				alt = section.get('alt'),
				caption = section.get('caption'),
				source = section.get('source'),
			)

			article_sections.append(tmp_section)

		elif section['type'] == 'media':
			media = article_media_dict[section['id']]


			if media['type'] == 'media':
				media_pub_date = datetime.strptime(media['pub_date'], '%Y-%m-%d-%H;%M;%S')

				if media.get('mod_date'):
					media_mod_date = datetime.strptime(media['mod_date'], '%Y-%m-%d-%H:%M:%S')

				else:
					media_mod_date = None

				tmp_section = MediaSection(
					type = media.get('type'),
					id = media.get('id'),
					url = media.get('url'),
					thumbnail = media.get('thumbnail'),
					caption = media.get('caption'),
					author = media.get('author'),
					publication_date = media_pub_date,
					modification_date = media_mod_date,
					duration = media.get('duration')
				)

				article_sections.append(tmp_section)

			elif media['type'] == 'image':
				tmp_section = ImageSection(
					type = media.get('type'),
					url = media.get('url'),
					alt = media.get('alt'),
					caption = media.get('caption'),
					source = media.get('source'),
				)

				article_sections.append(tmp_section)
			

	article = Article(
		id = article_id,
		original_language = article_details['original_language'],
		url = article_details['url'],
		publication_date = article_pub_date,

		thumbnail = article_details.get('thumbnail'),
		categories = {article_details.get('category')},
		tags = article_details.get('tags'),
		author = article_details.get('author'),
		modification_date = article_mod_date,
		sections = article_sections
	)

	return article



def main():
	articles = get_articles()
	mapped_articles = []

	for article in articles:
		article_id = article['id']
		mapped_articles.append(mapped_article(article_id))

	with open('log.txt', 'a') as f:
		current_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
		print(current_time)
		f.write(current_time)
		print()
		f.write('\n\n')

		for article in mapped_articles:
			article_dict = article.json()
			article_dict = json.loads(article_dict)
			article_dict = json.dumps(article_dict, indent=4)
			print(article_dict)
			f.write(article_dict)
			print('\n\n\n')
			f.write('\n\n\n\n')


if __name__ == '__main__':
	minutes = 5

	while True:
		main()
		sleep(minutes*60)
