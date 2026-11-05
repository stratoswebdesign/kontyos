{% extends get_layout() %}

{% block content_declare %}
    {{ add_body_class("home-body ky-body") }}
{% endblock %}

{% block page_head %}{% endblock %}

{% block content %}
    {# Kontyos főoldal – a demó főoldala; a szezont (forralt / újbor / Black Friday / karácsony) a kontyos.js dátum szerint váltja #}
    {% include 'snippets/ky-home.tpl' %}
{% endblock %}
