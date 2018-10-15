from flask_babel import gettext

EVENT = gettext('PyCon SK 2019')
DOMAIN = 'https://2019.pycon.sk'
API_DOMAIN = 'https://api.pycon.sk'

LANGS = ('en', 'sk')
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+00:00'


LDJSON_SPY = {
    "@type": "Organization",
    "name": "SPy o. z.",
    "url": "https://spy.pycon.sk",
    "logo": "https://spy.pycon.sk/img/logo/spy-logo.png",
    "sameAs": [
        "https://facebook.com/pyconsk",
        "https://twitter.com/pyconsk",
        "https://www.linkedin.com/company/spy-o--z-",
        "https://github.com/pyconsk",
    ]
}

LDJSON_PYCON = {
    "@context": "http://schema.org",
    "@type": "Event",
    "name": EVENT,
    "description": gettext("The PyCon SK 2019 conference, which will take place in Bratislava, is the annual gathering "
                           "for the community using and developing the open-source Python programming language. It is "
                           "organized by the volunteers from the SPy o.z., civic association dedicated to advancing "
                           "and promoting Python and other Open Source technologies and ideas. Through PyCon, "
                           "the SPy o.z. advances its mission of growing the Slovak (and also international) community "
                           "of Python programmers and Open Source supporters."),
    "startDate": "2019-03-22T9:00:00+01:00",
    "endDate": "2019-03-24T18:00:00+01:00",
    "image": "/static/img/logo/pycon_long_2019.png",
    "location": {
        "@type": "Place",
        "name": gettext("Faculty of Informatics and Information Technologies - Slovak University of Technology in "
                        "Bratislava"),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Ilkovičova 2",
            "addressLocality": "Bratislava 4",
            "postalCode": "842 16",
            "addressCountry": gettext("Slovak Republic")
        },
    },
    "url": DOMAIN,
    "workPerformed": {
        "@type": "CreativeWork",
        "name": EVENT,
        "creator": LDJSON_SPY
    }
}
