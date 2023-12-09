# coding: utf-8
"""
Created on 19/05/2013
@author: Óscar Gómez Alcañiz <oscar.gomez.alcaniz@gmail.com>
"""

import csv
from random import choice


class Palabras:
    emojis = "🎸🪕🎻🎶🎙🥁🎵🎼🎹🎷🎺🎸"

    def _carga_csv(self, archivo, genero=True):
        if genero:
            items = {}
        else:
            items = []

        with open(archivo, "r") as f:
            reader = csv.reader(f, delimiter=";")
            for row in reader:
                if genero:
                    items[row[0]] = row[1]
                else:
                    items.append(row[0])
        return items

    def _poner_genero(self, adj, gen):
        if gen == "f":
            if adj[-1] == "o":
                adj = f"{adj[:-1]}a"
            elif adj[-2:] == "or":
                adj = f"{adj[:-2]}ora"
            elif adj[-2:] == "ón":
                adj = f"{adj[:-2]}ona"
        return adj

    def generar_nombres(self, numero=1, cortos=False, largos=False, compuestos=False):
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
                choice(tipos)
                if len(tipos) > 0
                else choice(["corto", "largo", "compuesto"])
            )

            emoji = choice(list(self.emojis))

            if tipo == "largo" or tipo == "compuesto":
                obj = choice(list(self.comunes.keys()))
                gen = self.comunes[obj]
                art = "El" if gen == "m" else "La"
                nom = choice(list(self.propios.keys()))

                if tipo == "compuesto":
                    adj = choice(self.adjetivos)

                    adj = self._poner_genero(adj, gen)

                    nombre = f"{art} {adj.capitalize()} {obj.capitalize()} de {nom}"
                else:
                    nombre = f"{art} {obj.capitalize()} de {nom}"
            else:
                adj = choice(self.adjetivos)
                nom = choice(list(self.propios.keys()))
                gen = self.propios[nom]

                adj = self._poner_genero(adj, gen)

                nombre = f"{adj.capitalize()} {nom.capitalize()}"
            nombres.append(nombre)
            emojis.append(emoji)
        return nombres, emojis

    def __init__(self, propios=None, comunes=None, adjetivos=None, emojis=None):
        self.propios = self._carga_csv("data/propios.csv")
        self.comunes = self._carga_csv("data/comunes.csv")
        self.adjetivos = self._carga_csv("data/adjetivos.csv", genero=False)

        if propios != None:
            self.propios = dict(self.propios.items() + propios.items())
        if comunes != None:
            self.comunes = dict(self.comunes.items() + comunes.items())
        if adjetivos != None:
            self.adjetivos = dict(self.adjetivos.items() + adjetivos.items())
        if emojis != None:
            self.emojis = self.emojis.items() + emojis.items()
