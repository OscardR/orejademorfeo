# coding=utf-8
#
#   La Oreja de Morfeo: Tu nombre de banda de pop español en segundos!
#   @author: Óscar Gómez <oscar.gomez.alcaniz@gmail.com>
#

import os
from random import choice

import jinja2
from flask import Flask, request

from palabras import Palabras

# Init app
app = Flask(__name__, static_url_path="/static/")

# Set Jinja environment
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
)
PORT = os.environ.get("ODM_PORT", 5000)
DEBUG = os.environ.get("ODM_DEBUG", False)

collections = [2227687, 9757292, 1656221, 8647462, 326214, 9297490, 1980161]


def generar_nombres(numero=1, cortos=False, largos=False, compuestos=False):
    p = Palabras()
    nombres = []
    emojis = []
    tipos = []

    if cortos == "on":
        tipos.append("corto")
    if largos == "on":
        tipos.append("largo")
    if compuestos == "on":
        tipos.append("compuesto")

    for _ in range(numero):
        tipo = (
            choice(tipos) if len(tipos) > 0 else choice(["corto", "largo", "compuesto"])
        )

        emoji = choice(list(p.emojis))

        if tipo == "largo" or tipo == "compuesto":
            obj = choice(list(p.comunes.keys()))
            gen = p.comunes[obj]
            art = "El" if gen == "m" else "La"
            nom = choice(list(p.propios.keys()))

            if tipo == "compuesto":
                adj = choice(p.adjetivos)
                if gen == "f" and adj[-1] == "o":
                    adj = f"{adj[:-1]}a"
                nombre = f"{art} {adj.capitalize()} {obj.capitalize()} de {nom}"
            else:
                nombre = f"{art} {obj.capitalize()} de {nom}"
        else:
            adj = choice(p.adjetivos)
            nom = choice(list(p.propios.keys()))
            gen = p.propios[nom]

            if gen == "f":
                if adj[-1] == "o":
                    adj = f"{adj[:-1]}a"
                elif adj[-2:] == "or":
                    adj = f"{adj[:-2]}ora"
                elif adj[-2:] == "ón":
                    adj = f"{adj[:-2]}ona"

            nombre = f"{adj.capitalize()} {nom.capitalize()}"
        nombres.append(nombre)
        emojis.append(emoji)
    return nombres, emojis


@app.route("/")
def index():
    errores = {}
    try:
        numero = int(request.args.get("numero"))
        if numero > 1000 or numero < 0:
            errores["numero"] = numero
            numero = 1
    except:
        numero = 1
    cortos = request.args.get("cortos")
    largos = request.args.get("largos")
    compuestos = request.args.get("compuestos")

    nombres, emojis = generar_nombres(numero, cortos, largos, compuestos)

    template_values = {
        "nombres": nombres,
        "numero": numero,
        "cortos": cortos,
        "largos": largos,
        "compuestos": compuestos,
        "emojis": emojis,
        "collection": choice(collections),
        "errores": errores,
        "DEBUG": DEBUG,
    }
    template = JINJA_ENVIRONMENT.get_template("index.jinja2.html")
    return template.render(template_values)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)
