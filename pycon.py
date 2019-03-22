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
        'name': 'Ján Gordulič',
        'title': gettext('Conference opening'),
    },
    {
        'time': '09:30 - 10:15',
        'name': 'Meredydd Luff',
        'title': gettext('Anvil: Full-stack Web Apps with Nothing but Python'),
        'avatar': '/static/images/speakers/luff.jpg',
        'speaker': 'luff',
    },
    {
        'time': '10:20 - 10:50',
        'name': 'Jorge Torres',
        'title': gettext('Machine Learning Democratization'),
        'avatar': '/static/images/speakers/torres.png',
        'speaker': 'torres',
    },
    {
        'time': '11:05 - 11:35',
        'name': 'Jakub Šedinár',
        'title': gettext('Odoo'),
        'avatar': '/static/images/speakers/sedinar.jpg',
        'speaker': 'sedinar',
    },
    {
        'time': '11:40 - 12:10',
        'name': 'Jakub Balas',
        'title': gettext('Using Python in new space industry is not a rocket science'),
        'avatar': '/static/images/speakers/balas.jpg',
        'speaker': 'balas',
    },
    {
        'time': '12:10 - 13:10',
        'title': gettext('Lunch break'),
    },
    {
        'time': '13:10 - 13:55',
        'name': 'Adam Števko',
        'title': gettext('Be a good colleague and help your Security Engineer!'),
        'avatar': '/static/images/speakers/stevko.png',
        'speaker': 'stevko',
    },
    {
        'time': '14:00 - 14:30',
        'name': 'Anton Caceres',
        'title': gettext('Avoiding Macro Trouble of Micro Services'),
        'avatar': '/static/images/speakers/caceres.jpg',
        'speaker': 'caceres',
    },
    {
        'time': '14:45 - 15:30',
        'name': 'Sviatoslav Sydorenko',
        'title': gettext('GitHub Bots: Rise of the Machines 🤖'),
        'avatar': '/static/images/speakers/sydorenko.jpg',
        'speaker': 'sydorenko',
    },
    {
        'time': '15:35 - 16:05',
        'name': 'Christian Barra',
        'title': gettext('Let’s talk about MLOps'),
        'avatar': '/static/images/speakers/barra.jpg',
        'speaker': 'barra',
    },
    {
        'time': '16:20 - 16:50',
        'name': 'Filip Štefaňák',
        'title': gettext('Stability with a Hockey-stick'),
        'avatar': '/static/images/speakers/stefanak.jpg',
        'speaker': 'stefanak',
    },
    {
        'time': '16:55 - 17:25',
        'name': 'Miroslav Šedivý',
        'title': gettext('A Day Has Only 24±1 Hours'),
        'avatar': '/static/images/speakers/sedivy.jpg',
        'speaker': 'sedivy',
    },
    {
        'time': '17:30 - 18:00',
        'name': 'Ján Gordulič',
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
        'speaker': 'kucera',
    },
    {
        'time': '11:40 - 12:10',
        'name': 'Miroslava Šturmová, Marek Višňovec, Róbert Junas',
        'title': gettext('Objavovanie VPythonu v Dudley College'),
        'avatar': '/static/images/speakers/sturmova.jpg',
        'speaker': 'sturmova',
    },
    {
        'time': '12:10 - 13:10',
        'title': gettext('Lunch break'),
    },
    {
        'time': '13:10 - 13:33',
        'name': 'Tomáš Dudík',
        'title': gettext('Ako sa ďalej pasujeme s Python na hodinách informatiky'),
        'avatar': '',
    },
    {
        'time': '13:33 - 13:55',
        'name': 'Peter Valachovič, Tomáš Kiss, Jakub Hrnčár',
        'title': gettext('Prechod na Python u Piaristov v Nitre a niektoré tamojšie študentské projekty'),
        'avatar': '/static/images/speakers/valachovic.jpg',
        'speaker': 'valachovic',
    },
    {
        'time': '14:00 - 14:30',
        'name': '',
        'title': gettext('Diskusia za okrúhlymi stolmi: Otvorené vzdelávanie'),
    },
    {
        'time': '14:45 - 16:00',
        'name': 'Juraj Hromkovič',
        'title': gettext('Programovanie s LOGO-filozofiou ako model všeobecného vzdelávania pre všetky odbory'),
        'avatar': '/static/images/speakers/hromkovic.jpg',
        'speaker': 'hromkovic',
    },
    {
        'time': '16:20 - 16:50',
        'name': '',
        'title': 'Vyhodnotenie SPy Cup a Python Cup a Hardware showcase',
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
        'title': 'Hardware showcase',
    },
    {
        'time': '13:10 - 14:40',
        'name': 'Joel Lord',
        'title': gettext('Build a Passwordless Authentication Server'),
        'avatar': '/static/images/speakers/lord.jpg',
        'speaker': 'lord',
    },
    {
        'time': '14:45 - 16:50',
        'name': 'Suryansh Tibarewala',
        'title': gettext('Develop for Voice'),
        'avatar': '/static/images/speakers/tibarewala.jpg',
        'speaker': 'tibarewala',
    },
)
FRIDAY4 = (
    {
        'time': '13:10 - 15:30',
        'name': 'Shaun Taylor-Morgan',
        'title': 'Anvil - Build a full-stack web app using nothing but Python',
        'avatar': '/static/images/speakers/taylor-morgan.jpg',
        'speaker': 'taylor-morgan',
    },
)
SATURDAY1 = (
    {
        'time': '08:00 - 09:00',
        'name': gettext('Registration'),
        'title': gettext('Pick up your name badge and goodie bag'),
    },
    {
        'time': '09:00 - 09:25',
        'name': 'Ján Gordulič',
        'title': gettext('Conference opening'),
    },
    {
        'time': '09:30 - 10:00',
        'name': 'Markus Holtermann',
        'title': gettext('Less Obvious Things To Do With Django\'s ORM'),
        'avatar': '/static/images/speakers/holtermann.jpg',
        'speaker': 'holtermann',
    },
    {
        'time': '10:05 - 10:50',
        'name': 'Laurent Picard',
        'title': gettext('Building smarter solutions with Machine Learning, from magic to reality'),
        'avatar': '/static/images/speakers/picard.jpg',
        'speaker': 'picard',
    },
    {
        'time': '11:05 - 11:35',
        'name': 'Joel Lord',
        'title': gettext('I Don\'t Care About Security (And Neither Should You)'),
        'avatar': '/static/images/speakers/lord.jpg',
        'speaker': 'lord',
    },
    {
        'time': '11:40 - 12:10',
        'name': 'Helen Li',
        'title': gettext('Nucleus: an open-source library for genomics data and machine learning'),
        'avatar': '/static/images/speakers/li.jpg',
        'speaker': 'li',
    },
    {
        'time': '12:10 - 13:10',
        'title': gettext('Lunch break'),
    },
    {
        'time': '13:10 - 13:40',
        'name': 'Honza Král',
        'title': gettext('So you want to be an Engineer?'),
        'avatar': '/static/images/speakers/kral.jpg',
        'speaker': 'kral',
    },
    {
        'time': '13:45 - 14:15',
        'name': 'Stéphane Wirtel',
        'title': gettext('What\'s new in Python 3.7?'),
        'avatar': '/static/images/speakers/wirtel.jpg',
        'speaker': 'wirtel',
    },
    {
        'time': '14:30 - 15:15',
        'name': 'Gabriel Lachmann, Jano Suchal',
        'title': gettext('Ako prestať kradnúť v štátnom IT?'),
        'avatar': '/static/images/speakers/lachmann.jpg',
        'speaker': 'lachmann',
    },
    {
        'time': '15:20 - 15:50',
        'name': 'Petra Dzurovcinova',
        'title': gettext('Inovacie v meste Bratislava'),
        'avatar': '/static/images/speakers/dzurovcinova.jpg',
        'speaker': 'dzurovcinova',
    },
    {
        'time': '16:05 - 16:50',
        'name': 'František Benko',
        'title': gettext('We run huge in-memory databases in GKE and we love it!'),
        'avatar': '/static/images/speakers/benko.jpg',
        'speaker': 'benko',
    },
    {
        'time': '16:55 - 17:25',
        'name': 'Martin Strýček',
        'title': gettext('Your flight ticket is just the tip of the iceberg!'),
    },
    {
        'time': '17:30 - 18:00',
        'name': 'Ján Gordulič',
        'title': 'QUIZ!',
    },
    {
        'time': '18:05 - 18:30',
        'name': 'Ján Gordulič',
        'title': 'Lightning talks',
    },
)
SATURDAY2 = (
    {
        'time': '09:30 - 10:00',
        'name': 'Světlana Hrabinová',
        'title': gettext('Nenuťte uživatele přemýšlet'),
        'avatar': '/static/images/speakers/hrabinova.jpg',
        'speaker': 'hrabinova',
    },
    {
        'time': '10:05 - 10:50',
        'name': 'Samuel Hopko',
        'title': gettext('Amazon Web Services - Alexa skills'),
        'avatar': '/static/images/speakers/hopko.jpg',
        'speaker': 'hopko',
    },
    {
        'time': '11:05 - 11:35',
        'name': 'Radoslav Kokuľa',
        'title': gettext('Robot Framework – univerzálny nástroj pre automatizované testovanie'),
        'avatar': '/static/images/speakers/kokula.png',
        'speaker': 'kokula',
    },
    {
        'time': '11:40 - 12:10',
        'name': 'Manoj Pandey',
        'title': gettext('Gotchas and Landmines in Python'),
        'avatar': '/static/images/speakers/pandey.jpg',
        'speaker': 'pandey',
    },
    {
        'time': '12:10 - 13:10',
        'title': gettext('Lunch break'),
    },
    {
        'time': '13:45 - 14:15',
        'name': 'Mislav Cimperšak',
        'title': gettext('On the Edge of Leadership'),
        'avatar': '/static/images/speakers/cimpersak.jpg',
        'speaker': 'cimpersak',
    },
    {
        'time': '14:30 - 15:15',
        'name': 'Ondrej Sika',
        'title': gettext('Deploy your Python application into Kubernetes'),
        'avatar': '/static/images/speakers/sika.jpg',
        'speaker': 'sika',
    },
    {
        'time': '15:20 - 15:50',
        'name': 'Dmitry Dygalo',
        'title': gettext('Testing network interactions in Python'),
        'avatar': '/static/images/speakers/dygalo.jpg',
        'speaker': 'dygalo',
    },
    {
        'time': '16:05 - 16:50',
        'name': 'Paweł Lewtak',
        'title': gettext('Long term IT projects'),
        'avatar': '/static/images/speakers/lewtak.jpg',
        'speaker': 'lewtak',
    },
    {
        'time': '16:55 - 17:25',
        'name': 'Luke Spademan',
        'title': gettext('Controling a robotic arm with micro:bits. '
                         'How to make computer science eduction more interesting'),
        'avatar': '/static/images/speakers/spademan.jpg',
        'speaker': 'spademan',
    },
)
SATURDAY3 = (
    {
        'time': '9:00 - 10:00',
        'name': '',
        'title': gettext('Young Coders Day - micro:bit'),
    },
    {
        'time': '10:05 - 12:15',
        'name': '',
        'title': gettext('Young Coders Day - Coder Dojo'),
    },
    {
        'time': '14:15 - 16:00',
        'name': '',
        'title': gettext('Job Fair'),
    },
)
SATURDAY4 = (
    {
        'time': '09:00 - 11:00',
        'name': 'Marek Mansell',
        'title': 'Pokročilé medzipredmetové projekty s BBC micro:bit',
        'avatar': '',
    },
)
SATURDAY5 = (
    {
        'time': '09:00 - 10:50',
        'name': 'Magdaléna Bellayová, Eva Kupčová',
        'title': 'Programovať môže každý. Fakt alebo mýtus?',
        'avatar': '',
        'speaker': 'bellayova',
    },
    {
        'time': '11:05 - 12:10',
        'name': 'Miroslav Biňas',
        'title': 'Dobrodružstvá v Minecrafte s jazykom Python',
        'avatar': '',
    },
    {
        'time': '13:10 - 15:15',
        'name': 'Tobias Kohn, Dennis Komm',
        'title': 'Using Python to Teach Algorithmic Efficiency',
        'avatar': '/static/images/speakers/kohn-komm.png',
        'speaker': 'kohn',
    },
    {
        'time': '15:20 - 16:40',
        'name': 'Miroslav Biňas',
        'title': 'Výučba programovania pomocou tvorby hier v PyGame Zero',
        'avatar': '',
    },
)
SUNDAY1 = (
    {
        'time': '09:30 - 10:00',
        'name': 'Jakub Mertus',
        'title': gettext('Automatická korekcia písaného prejavu prirodzeného jazyka '
                         's využitím znakových a kontextuálnych modelov'),
        'avatar': '/static/images/speakers/mertus.jpg',
        'speaker': 'mertus',
    },
    {
        'time': '10:05 - 10:35',
        'name': 'Suryansh Tibarewala',
        'title': gettext('MVP, is never just a MVP'),
        'avatar': '/static/images/speakers/tibarewala.jpg',
        'speaker': 'tibarewala',
    },
    {
        'time': '10:50 - 11:20',
        'name': 'Stanislava Sojáková',
        'title': gettext('Lessons Learned from Leading Bratislava Peer Python Learning Group'),
        'avatar': '/static/images/speakers/sojakova.jpg',
        'speaker': 'sojakova',
    },
    {
        'time': '11:25 - 11:55',
        'name': 'Tibor Frank',
        'title': gettext('Automated visualization and presentation of tests results'),
        'avatar': '/static/images/speakers/frank.jpg',
        'speaker': 'frank',
    },
    {
        'time': '11:55 - 12:55',
        'title': gettext('Lunch break'),
    },
    {
        'time': '12:55 - 13:25',
        'name': 'Hans Christian Feßl',
        'title': gettext('Think about the user'),
        'avatar': '/static/images/speakers/fessl.jpg',
        'speaker': 'fessl',
    },
    {
        'time': '13:30 - 14:00',
        'name': 'Ingrid Budau',
        'title': gettext('The Apprentice\'s Enthusiastic Guide to pandas '
                         '(or how to look at the world through the gentle eyes of one)'),
        'avatar': '/static/images/speakers/budau.jpg',
        'speaker': 'budau',
    },
    {
        'time': '14:15 - 15:00',
        'name': 'Petr Stehlík',
        'title': gettext('The dos and don\'ts of task queues'),
        'avatar': '/static/images/speakers/stehlik.png',
        'speaker': 'stehlik',
    },
    {
        'time': '15:05 - 15:35',
        'name': 'Christoph Ritzer',
        'title': gettext('Intro to Blockchain with Python'),
        'avatar': '/static/images/speakers/ritzer.jpg',
        'speaker': 'ritzer',
    },
    {
        'time': '15:50 - 16:20',
        'name': 'Kalyan Dikshit',
        'title': gettext('Smart Homes + Tor = SSH [Secure Smart Home]'),
        'avatar': '/static/images/speakers/dikshit.jpg',
        'speaker': 'dikshit',
    },
    {
        'time': '16:20 - 16:30',
        'name': 'Richard Kellner',
        'title': gettext('Conference closing'),
        # 'avatar': '/static/images/speakers/kellner.jpg',
    },
)
SUNDAY2 = (
    {
        'time': '10:00 - 12:00',
        'name': 'Mridul Seth',
        'title': gettext('Network Science, Game of Thrones and US Airports'),
        'avatar': '/static/images/speakers/seth.jpg',
        'speaker': 'seth',
    },
    {
        'time': '12:00 - 13:00',
        'title': gettext('Lunch break'),
    },
    {
        'time': '13:00 - 15:00',
        'name': 'Sviatoslav Sydorenko',
        'title': gettext('Hands-on: Creating GitHub Bots 🤖 to deal with boring routines'),
        'avatar': '/static/images/speakers/sydorenko.jpg',
        'speaker': 'sydorenko',
    },
)
SUNDAY3 = (
    {
        'time': '10:00 - 14:00',
        'name': 'Karol Hrubjak, Veronika Žatková',
        'title': gettext('Machine learning workshop in Python'),
        'avatar': '/static/images/speakers/hrubjak-zatkova.jpg',
        'speaker': 'hrubjak',
    },
)
SUNDAY4 = (
    {
        'time': '09:00 - 17:00',
        'name': '',
        'title': 'Bratislavský Open Data Hackathon',
        'desc': 'Máte nápad na zaujímavý projekt? Chcete urobiť niečo užitočné pre svoje mesto? Príďte navrhnúť '
                'experiment, vytvoriť malý prototyp a diskutovať s tými, čo majú radi Bratislavu. Celý deň strávi s '
                'nami šéfka inovácií na magistráte, Petra Dzurovčinová. Tí, ktorí sa na hackathon vopred zaregistrujú, '
                'čaká okrem priestoru na kreativitu tiež niečo dobré na zahryznutie. Dokonca aj bratislavské rožky!',
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


@app.route('/chat/')
def chat():
    return render_template('chat.html', **_get_template_variables(li_index='active', redirect=True))


@app.route('/<lang_code>/chat.html')
def chat2():
    return render_template('chat.html', **_get_template_variables(li_index='active'))


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
                                                                      minor=FRIDAY2, babbageovaA=FRIDAY3,
                                                                      babbageovaB=FRIDAY4, day=gettext('Friday')))

@app.route('/<lang_code>/saturday.html')
def saturday():
    return render_template('schedule.html', **_get_template_variables(li_schedule='active', magna=SATURDAY1,
                                                                      minor=SATURDAY2, babbageovaA=SATURDAY3,
                                                                      babbageovaB=SATURDAY4, digilab=SATURDAY5,
                                                                      day=gettext('Saturday')))

@app.route('/<lang_code>/sunday.html')
def sunday():
    return render_template('schedule.html', **_get_template_variables(li_schedule='active', magna=SUNDAY1,
                                                                      minor=SUNDAY2, babbageovaA=SUNDAY3,
                                                                      babbageovaB=SUNDAY4, day=gettext('Sunday')))

@app.route('/<lang_code>/job-fair.html')
def jobfair():
    return render_template('job-fair.html', **_get_template_variables(li_jobfair='active'))


@app.route('/<lang_code>/job-fair-form.html')
def jobfair_form():
    return render_template('job-fair_form.html', **_get_template_variables(li_jobfair='active'))


@app.route('/<lang_code>/coc.html')
def coc():
    return render_template('coc.html', **_get_template_variables(li_coc='active'))


@app.route('/<lang_code>/faq.html')
def faq():
    return render_template('faq.html', **_get_template_variables(li_faq='active'))


@app.route('/<lang_code>/venue.html')
def venue():
    return render_template('venue.html', **_get_template_variables(li_venue='active'))


@app.route('/<lang_code>/about-us.html')
def aboutus():
    return render_template('about-us.html', **_get_template_variables(li_aboutus='active'))


@app.route('/<lang_code>/privacy-policy.html')
def privacy_policy():
    return render_template('privacy-policy.html', **_get_template_variables(li_privacy='active'))


@app.route('/<lang_code>/sponsoring.html')
def sponsoring():
    return render_template('sponsoring.html', **_get_template_variables(li_sponsoring='active'))


@app.route('/<lang_code>/hackaton-form.html')
def hackaton_form():
    return render_template('hackaton_form.html', **_get_template_variables(li_index='active'))


@app.route('/<lang_code>/recording.html')
def recording():
    return render_template('recording.html', **_get_template_variables(li_recording='active'))


@app.route('/<lang_code>/live.html')
def live():
    return render_template('livestream.html', **_get_template_variables(li_live='active'))


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
