import gettext
from pathlib import Path
import logging

domain = 'bot'
localedir = 'locales'

def get_i18n_string(s, lang) -> str:
    if lang in ['ru']:
        language_translations = gettext.translation(domain, Path(__file__).parent.parent / localedir, languages=[lang])
        language_translations.install()
        
        return _(s)
    language_translations = gettext.translation(domain, localedir, languages=['en'])
    language_translations.install()
    
    return _(s)