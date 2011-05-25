Real life twitter
==================
Este proyecto concentra sus esfuerzos en acercar twitter al mundo real, demostrar que nó solo estamos en internet.
RLT descarga los tweets sobre un tema espeficico (busqueda), una persona, y combinaciones entre estos, o grupos.
Despues crea una plantilla de pegatinas con esos tweets, directas para imprimir.

¡Expande tus pensamientos IRL!

Uso
====
git clone https://github.couuuuuOn/RealLifeTwitter.git
cd RealLifeTwitter/
python RealLifeTweeter.py --hashtag notenemosmiedo --user tomalaplaza --destfile notenemosmiedo.html --timeout 60
> Cuando termine, pulsa "f"
firefox notenemosmiedo.html
ó:
wkhtmltopdf notenemosmiedo.html notenemosmiedo.pdf

incluso puedes hacer despues un
print notenemosmiedo.pdf
a partir de la última version puedes iniciar un servidor web desde el que satisfacer las peticiones, con:
python RealLifeTwitter --server True

Dependencias
=============
Este software depende de python2.7 (o python2.6 con algunos módulos extra), python-twitter, y un navegador, o wkhtmltopdf (wkhtmltopdf package on debian)


Real life twitter
=================
This project aims to get the most important tweets about a subject, a group or subjects, a person or group of persons (even mixed!).
Then it'll create stickers, allowing you to "Real Life Tweet", and spread your tweet-toughs in real world.


Usage
======
git clone https://github.com/XayOn/RealLifeTwitter.git
cd RealLifeTwitter/
python RealLifeTweeter.py --hashtag notenemosmiedo --user tomalaplaza --destfile notenemosmiedo.html --timeout 60
> Then press "f"
firefox notenemosmiedo_tomalaplaza.html
or:
wkhtmltopdf notenemosmiedo.html notenemosmiedo.pdf

you can even execute this after to print it:
print notenemosmiedo.pdf

Dependencias
=============
this software dependes on python2.7 (or python2.6 with some extra modules), python-twitter, and a web browser, or wkhtmltopdf (wkhtmltopdf package on debian)
