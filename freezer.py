import os

from flask_frozen import Freezer
from pycon import app

LANGUAGES = (
    {'lang_code': 'sk'},
    {'lang_code': 'en'}
)

app.config['FREEZER_DESTINATION'] = 'docs'  # GitHub pages directory for static site
# app.config['APPLICATION_ROOT'] = '/2019.pycon.sk/'

freezer = Freezer(app)


@freezer.register_generator
def index():
    for lang in LANGUAGES:
        yield lang


def fix_calendar():
    for f in os.listdir(freezer.root):
        full_path = os.path.join(freezer.root, f)

        if os.path.isdir(full_path):
            cal = os.path.join(full_path, 'calendar.ics')

            if os.path.exists(cal):
                print('Replacing "\\n" with "\\r\\n" in {}'.format(cal))
                with open(cal, 'r') as f:
                    cal_content = f.read()
                with open(cal, 'w') as f:
                    f.write(cal_content.replace('\n', '\r\n'))


if __name__ == '__main__':
    freezer.freeze()
    # fix_calendar()
