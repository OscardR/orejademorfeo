#
#   Created on 19/05/2013
#
#   @author: Óscar Gómez Alcañiz <oscar.gomez.alcaniz@gmail.com>
#

import csv
from random import choice
from enum import Enum


class Tipo(Enum):
    CORTO = "corto"
    LARGO = "largo"
    COMPUESTO = "compuesto"


class Palabras:
    emojis = "🎸🪕🎻🎶🎙🥁🎵🎼🎹🎷🎺🎸"

    def _carga_csv(self, archivo: str, genero: bool = True) -> dict | list:
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

    def _poner_genero(self, adj: str, gen: str) -> str:
        if gen == "f":
            if adj[-1] == "o":
                adj = f"{adj[:-1]}a"
            elif adj[-2:] == "or":
                adj = f"{adj[:-2]}ora"
            elif adj[-2:] == "ón":
                adj = f"{adj[:-2]}ona"
        return adj

    def _generar_nombre(self, tipo: str = Tipo.CORTO) -> str:
        if tipo == Tipo.LARGO or tipo == Tipo.COMPUESTO:
            obj = choice(list(self.comunes.keys()))
            gen = self.comunes[obj]
            art = "El" if gen == "m" else "La"
            nom = choice(list(self.propios.keys()))

            if tipo == Tipo.COMPUESTO:
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

        return nombre

    def generar_nombres(
        self,
        numero: int = 1,
        cortos: bool = False,
        largos: bool = False,
        compuestos: bool = False,
    ) -> list[str]:
        nombres = []
        emojis = []
        tipos = []

        # Configurar tipos
        if cortos:
            tipos.append(Tipo.CORTO)
        if largos:
            tipos.append(Tipo.LARGO)
        if compuestos:
            tipos.append(Tipo.COMPUESTO)

        for _ in range(numero):
            tipo = choice(tipos) if len(tipos) > 0 else choice(list(Tipo))

            emoji = choice(list(self.emojis))
            nombre = self._generar_nombre(tipo)

            nombres.append(nombre)
            emojis.append(emoji)

        return nombres, emojis

    def __init__(
        self,
        propios: dict = None,
        comunes: dict = None,
        adjetivos: list = None,
        emojis: str = None,
    ):
        # Leer nombres y adjetivos
        self.propios = self._carga_csv("data/propios.csv")
        self.comunes = self._carga_csv("data/comunes.csv")
        self.adjetivos = self._carga_csv("data/adjetivos.csv", genero=False)

        # Añadir las palabras pasadas al inicializar
        if propios:
            self.propios = {**self.propios, **propios}
        if comunes:
            self.comunes = {**self.comunes, **comunes}
        if adjetivos:
            self.adjetivos = self.adjetivos + adjetivos
        if emojis:
            self.emojis = list(self.emojis) + list(emojis)
