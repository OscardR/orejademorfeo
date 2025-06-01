#
#   La Oreja de Morfeo: Tu nombre de banda de pop español en segundos!
#
#   @author: Óscar Gómez <oscar.gomez.alcaniz@gmail.com>
#

import os
from random import choice

from flask import Flask, request, render_template

from palabras import Palabras

#
#   Init app
#
app = Flask(__name__)

#
#   Configuration
#
PORT = int(os.environ.get("PORT", os.environ.get("ODM_PORT", 5000)))
DEBUG = os.environ.get("ODM_DEBUG", "False").lower() in ("true", "1", "yes")

# Backgrounds from https://source.unsplash.com/
collections = [
    "https://images.pexels.com/photos/1105666/pexels-photo-1105666.jpeg",
    "https://images.pexels.com/photos/1763075/pexels-photo-1763075.jpeg",
    "https://images.pexels.com/photos/1763067/pexels-photo-1763067.jpeg",
    "https://images.pexels.com/photos/849/people-festival-party-dancing.jpg",
    "https://images.pexels.com/photos/2747449/pexels-photo-2747449.jpeg",
    "https://images.pexels.com/photos/1047442/pexels-photo-1047442.jpeg",
    "https://images.pexels.com/photos/3661650/pexels-photo-3661650.jpeg",
    "https://images.pexels.com/photos/2735037/pexels-photo-2735037.jpeg",
    "https://images.pexels.com/photos/2728557/pexels-photo-2728557.jpeg",
    "https://images.pexels.com/photos/2990835/pexels-photo-2990835.jpeg",
    "https://images.pexels.com/photos/1120162/pexels-photo-1120162.jpeg",
]

# Initialize name generator module
palabras = Palabras()


@app.route("/")
def index():
    errores = {}

    # Get configuration from form
    try:
        numero = int(request.args.get("numero", 1))
        if numero > 1000 or numero < 0:
            errores["numero"] = numero
            numero = 1
    except (TypeError, ValueError):
        numero = 1

    cortos = request.args.get("cortos") == "on"
    largos = request.args.get("largos") == "on"
    compuestos = request.args.get("compuestos") == "on"

    # Generate names
    nombres, emojis = palabras.generar_nombres(numero, cortos, largos, compuestos)

    # Prepare template variables
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

    # Use Flask's built-in template rendering
    return render_template("index.jinja2.html", **template_values)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
