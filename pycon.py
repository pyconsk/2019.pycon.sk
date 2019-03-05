from datetime import date

from flask import Flask, g, request, render_template, abort, make_response, url_for, redirect
from flask_babel import Babel, gettext

EVENT = gettext('PyCon SK 2019')
DOMAIN = 'https://2019.pycon.sk'
API_DOMAIN = 'https://api.pycon.sk'

LANGS = ('en', 'sk')
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+00:00'

app = Flask(__name__, static_url_path='/static')  # pylint: disable=invalid-name
app.config['BABEL_DEFAULT_LOCALE'] = 'sk'
app.jinja_options = {'extensions': ['jinja2.ext.with_', 'jinja2.ext.i18n']}
babel = Babel(app)  # pylint: disable=invalid-name


FRIDAY1 = (
    {
        'time': '08:00 - 09:00',
        'name': gettext('Registration'),
        'title': gettext('Pick up your name badge and goodie bag'),
    },
    {
        'time': '09:00 - 09:25',
        'name': 'Richard Kellner',
        'title': gettext('Conference opening'),
    },
    {
        'time': '09:30 - 10:15',
        'name': 'Meredydd Luff',
        'title': gettext('Anvil: Full-stack Web Apps with Nothing but Python'),
        'avatar': '/static/images/speakers/luff.jpg',
    },
    {
        'time': '10:20 - 10:50',
        'name': gettext('Machine Learning Democratization'),
        'title': 'Jorge Torres',
        'avatar': '/static/images/speakers/torres.png',
    },
    {
        'time': '11:05 - 11:35',
        'name': gettext('Avoiding Macro Trouble of Micro Services'),
        'title': 'Anton Caceres',
        'avatar': '/static/images/speakers/caceres.jpg',
    },
    {
        'time': '11:40 - 12:10',
        'name': 'Jakub Balas',
        'title': gettext('Using Python in new space industry is not a rocket science'),
        'avatar': '/static/images/speakers/balas.jpg',
    },
    {
        'time': '13:10 - 13:55',
        'name': 'Adam Števko',
        'title': gettext('Be a good colleague and help your Security Engineer!'),
        'avatar': '/static/images/speakers/stevko.png',
    },
    {
        'time': '14:00 - 14:30',
        'name': 'Jakub Šedinár',
        'title': gettext('Odoo'),
        'avatar': '/static/images/speakers/sedinar.jpg',
    },
    {
        'time': '14:45 - 15:30',
        'name': 'Sviatoslav Sydorenko',
        'title': gettext('GitHub Bots: Rise of the Machines 🤖'),
        'avatar': '/static/images/speakers/sydorenko.jpg',
    },
    {
        'time': '15:35 - 16:05',
        'name': 'Christian Barra',
        'title': gettext('Let’s talk about MLOps'),
        'avatar': '/static/images/speakers/barra.jpg',
    },
    {
        'time': '16:20 - 16:50',
        'name': 'Filip Štefaňák',
        'title': gettext('Stability with a Hockey-stick'),
        'avatar': '/static/images/speakers/stefanak.jpg',
    },
    {
        'time': '16:55 - 17:25',
        'name': 'Miroslav Šedivý',
        'title': gettext('A Day Has Only 24±1 Hours'),
        'avatar': '/static/images/speakers/sedivy.jpg',
    },
    {
        'time': '17:30 - 18:00',
        'name': '',
        'title': 'Lightning talks',
    },
)
FRIDAY2 = (
    {
        'time': '09:30 - 10:15',
        'name': 'Marek Mansell',
        'title': gettext('Učíme s Hardvérom a finále SPyCup'),
        'avatar': '',
    },
    {
        'time': '10:20 - 10:50',
        'name': 'Miroslav Biňas',
        'title': gettext('Výučba programovania pomocou tvorby hier v PyGame Zero'),
        'avatar': '',
    },
    {
        'time': '11:05 - 11:35',
        'name': 'Peter Kučera',
        'title': gettext('Programujeme v Pythone na strednej škole'),
        'avatar': '/static/images/speakers/kucera.jpg',
    },
    {
        'time': '11:40 - 12:10',
        'name': '',
        'title': 'Vyhodnotenie SPy Cup a Python Cup a HARDWARE SHOWCASE',
    },
    {
        'time': '13:10 - 13:55',
        'name': 'Tomáš Dudík, Jakub Sokolík',
        'title': gettext('Ako sa ďalej pasujeme s Python na hodinách informatiky'),
        'avatar': '',
    },
    {
        'time': '13:10 - 13:55',
        'name': 'Peter Valachovič, Tomáš Kiss, Jakub Hrnčár',
        'title': gettext('Prechod na Python u Piaristov v Nitre a niektoré tamojšie študentské projekty'),
        'avatar': '',
    },
    {
        'time': '14:00 - 14:30',
        'name': 'Luke Spademan',
        'title': gettext('Controling a robotic arm with micro:bits. How to make computer science eduction more interesting'),
        'avatar': '/static/images/speakers/spademan.jpg',
    },
    {
        'time': '14:45 - 16:00',
        'name': 'Juraj Hromkovič',
        'title': gettext('Programovanie s LOGO-filozofiou ako model všeobecného vzdelávania pre všetky odbory'),
        'avatar': '/static/images/speakers/hromkovic.jpg',
    },
    {
        'time': '16:20 - 16:50',
        'name': 'Miroslava Šturmová, Marek Višňovec, Róbert Junas',
        'title': gettext('Objavovanie VPythonu v Dudley College'),
        'avatar': '',
    },
    {
        'time': '16:55 - 17:25',
        'name': '',
        'title': 'EduTalks',
    },
)
FRIDAY3 = (
    {
        'time': '12:00 - 12:30',
        'name': '',
        'title': 'HARDWARE SHOWCASE',
    },
    {
        'time': '13:10 - 14:40',
        'name': 'Joel Lord',
        'title': gettext('Build a Passwordless Authentication Server'),
        'avatar': '/static/images/speakers/lord.jpg',
    },
    {
        'time': '14:45 - 16:50',
        'name': 'Suryansh Tibarewala',
        'title': gettext('Develop for Voice'),
        'avatar': '/static/images/speakers/tibarewala.jpg',
    },
)
FRIDAY4 = (
    {
        'time': '13:10 - 15:30',
        'name': 'Shaun Taylor-Morgan',
        'title': 'Anvil - Build a full-stack web app using nothing but Python',
        'avatar': '/static/images/speakers/taylor-morgan.jpg',
    },
)
SUNDAY1 = (
    {
        'time': '9:30 - 10:00',
        'name': 'Stanislava Sojáková',
        'title': gettext('Lessons Learned from Leading Bratislava Peer Python Learning Group'),
        'avatar': '/static/images/speakers/sojakova.jpg',
    },
)
SUNDAY2 = (
    {
        'time': '10:00 - 12:00',
        'name': 'Mridul Seth',
        'title': gettext('Network Science, Game of Thrones and US Airports'),
        'avatar': '/static/images/speakers/seth.jpg',
    },
    {
        'time': '13:00 - 15:00',
        'name': 'Sviatoslav Sydorenko',
        'title': gettext('Hands-on: Creating GitHub Bots 🤖 to deal with boring routines'),
        'avatar': '/static/images/speakers/sydorenko.jpg',
    },
)
SUNDAY3 = (
    {
        'time': '10:00 - 14:00',
        'name': 'Karol Hrubjak, Veronika Žatková',
        'title': gettext('Machine learning workshop in Python'),
        'avatar': '/static/images/speakers/hrubjak-zatkova.jpg',
    },
)
SUNDAY4 = (
    {
        'time': '09:00 - 17:00',
        'name': '',
        'title': 'Bratislavský Open Data Hackathon',
    },
)

@app.route('/sitemap.xml')
def sitemap():
    excluded = {'static', 'sitemap'}
    pages = []

    for lang in LANGS:
        for rule in app.url_map.iter_rules():
            if 'GET' in rule.methods and rule.endpoint not in excluded:
                # `url_for` appends unknown arguments as query parameters.
                # We want to avoid that when a page isn't localized.
                values = {'lang_code': lang} if 'lang_code' in rule.arguments else {}
                pages.append(DOMAIN + url_for(rule.endpoint, **values))

    sitemap_xml = render_template('sitemap.xml', pages=pages, today=date.today())
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response


@app.route('/')
def root():
    return redirect('sk/index.html')


@app.route('/<lang_code>/index.html')
def index():
    return render_template('index.html', **_get_template_variables(li_index='active'))


@app.route('/<lang_code>/cfp.html')
def cfp():
    return render_template('cfp.html', **_get_template_variables(li_cfp='active'))


@app.route('/<lang_code>/cfp_form.html')
def cfp_form():
    return render_template('cfp_form.html', **_get_template_variables(li_cfp='active'))


@app.route('/<lang_code>/cfv.html')
def cfv():
    return render_template('cfv.html', **_get_template_variables(li_cfv='active'))


@app.route('/<lang_code>/thanks.html')
def thanks():
    return render_template('thanks.html', **_get_template_variables(li_cfp='active'))


@app.route('/<lang_code>/tickets.html')
def tickets():
    return render_template('tickets.html', **_get_template_variables(li_tickets='active'))


@app.route('/<lang_code>/edusummit.html')
def edusummit():
    return render_template('edusummit.html', **_get_template_variables(li_edusummit='active'))


@app.route('/<lang_code>/speakers.html')
def speakers():
    return render_template('speakers.html', **_get_template_variables(li_speakers='active'))


@app.route('/<lang_code>/friday.html')
def friday():
    return render_template('schedule.html', **_get_template_variables(li_schedule='active', magna=FRIDAY1,
                                                                      minor=FRIDAY2, babageovaA=FRIDAY3,
                                                                      babageovaB=FRIDAY4))

@app.route('/<lang_code>/saturday.html')
def saturday():
    return render_template('schedule.html', **_get_template_variables(li_schedule='active', magna=FRIDAY1,
                                                                      minor=FRIDAY2, babageovaA=FRIDAY3,
                                                                      babageovaB=FRIDAY4))

@app.route('/<lang_code>/sunday.html')
def sunday():
    return render_template('schedule.html', **_get_template_variables(li_schedule='active', magna=SUNDAY1,
                                                                      minor=SUNDAY2, babageovaA=SUNDAY3,
                                                                      babageovaB=SUNDAY4))

@app.route('/<lang_code>/job-fair.html')
def jobfair():
    return render_template('job-fair.html', **_get_template_variables(li_jobfair='active'))


@app.route('/<lang_code>/coc.html')
def coc():
    return render_template('coc.html', **_get_template_variables(li_coc='active'))


@app.route('/<lang_code>/faq.html')
def faq():
    return render_template('faq.html', **_get_template_variables(li_faq='active'))


@app.route('/<lang_code>/venue.html')
def venue():
    return render_template('venue.html', **_get_template_variables(li_venue='active'))


@app.route('/<lang_code>/privacy-policy.html')
def privacy_policy():
    return render_template('privacy-policy.html', **_get_template_variables(li_privacy='active'))


@app.route('/<lang_code>/sponsoring.html')
def sponsoring():
    return render_template('sponsoring.html', **_get_template_variables(li_sponsoring='active'))


@app.route('/<lang_code>/recording.html')
def recording():
    return render_template('recording.html', **_get_template_variables(li_recording='active'))


def _get_template_variables(**kwargs):
    """Collect variables for template that repeats, e.g. are in body.html template"""
    variables = {
        'title': EVENT,
        'domain': DOMAIN,
    }
    variables.update(kwargs)

    if 'current_lang' in g:
        variables['lang_code'] = g.current_lang
    else:
        variables['lang_code'] = app.config['BABEL_DEFAULT_LOCALE']

    return variables


@app.before_request
def before():  # pylint: disable=inconsistent-return-statements
    if request.view_args and 'lang_code' in request.view_args:
        g.current_lang = request.view_args['lang_code']
        if request.view_args['lang_code'] not in LANGS:
            return abort(404)
        request.view_args.pop('lang_code')


@babel.localeselector
def get_locale():
    # try to guess the language from the user accept
    # header the browser transmits. The best match wins.
    # return request.accept_languages.best_match(['de', 'sk', 'en'])
    return g.get('current_lang', app.config['BABEL_DEFAULT_LOCALE'])
