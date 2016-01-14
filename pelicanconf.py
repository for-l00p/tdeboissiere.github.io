#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'Thibault de Boissiere'
SITENAME = u'Pony Pony Learn Learn'
SITEURL = ''

PATH = 'content'

#########################
# Theme and architecture
#########################

#General
THEME = 'themes/pelican-bootstrap3'
BOOTSTRAP_THEME = "united"
DEFAULT_PAGINATION = 10
PYGMENTS_STYLE = "monokai"
# Banner and title
BANNER = 'images/banner.JPG'
BANNER_SUBTITLE = 'Machine Learning, Data science and ponies'
#Menu
DISPLAY_PAGES_ON_MENU = False
BOOTSTRAP_NAVBAR_INVERSE = True
DISPLAY_CATEGORIES_ON_MENU = False
# Sidebar
SIDEBAR_IMAGES = ["images/pony.jpg"]
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
DISPLAY_CATEGORIES_ON_SIDEBAR = True
DISPLAY_TAGS_ON_SIDEBAR = True
TAG_CLOUD_MAX_ITEMS = 10
# Social widget
SOCIAL = (('linkedin', 'https://www.linkedin.com/in/thibault-main-de-boissi%C3%A8re-25476699'),
          ('github', 'http://github.com/tdeboissiere'))



# Title menu options
MENUITEMS = (
			('About','/pages/about.html'),
			('Projects','/pages/project.html'),
			)

# Order archives
NEWEST_FIRST_ARCHIVES = True

# Times and dates
DEFAULT_DATE_FORMAT = '%b %d, %Y'
TIMEZONE = 'Australia/ACT'
DEFAULT_LANG = u'en'

# Show when a post belongs to a series of posts
SHOW_SERIES = True


# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = ['liquid_tags.img', 'liquid_tags.video',
           'liquid_tags.youtube', 'liquid_tags.vimeo',
           'liquid_tags.include_code', "tipue_search", 'tag_cloud', 'series']

DIRECT_TEMPLATES = ('index', 'categories', 'authors', 'archives', 'search')


# markdown extension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.toc import TocExtension
from pymdownx.inlinehilite import InlineHiliteExtension


MD_EXTENSIONS = [
	CodeHiliteExtension(css_class='highlight', linenums = True),
    "pymdownx.extra",
    "pymdownx.mark",
    "pymdownx.caret",
    "pymdownx.magiclink",
    "pymdownx.smartsymbols",
    "pymdownx.githubemoji"
]

# No Feed generation 
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Add search box
SEARCH_BOX = True
