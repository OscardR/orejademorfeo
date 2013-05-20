# coding: utf-8
# Generador de nombres de grupos Españoles
# @author: Óscar Gómez <oscar.gomez@uji.es>

import webapp2
import jinja2
import os
# import urllib

from random import choice
from palabras import Palabras

JINJA_ENVIRONMENT = jinja2.Environment( 
    loader=jinja2.FileSystemLoader( os.path.dirname( __file__ ) ),
    extensions=['jinja2.ext.autoescape'] )

class MainPage( webapp2.RequestHandler ):
    def generar_nombres( self, numero=1, cortos=False, largos=False, compuestos=False ):
        p = Palabras()
        nombres = []
        tipos = []
        if cortos == 'on': tipos.append( 'corto' )
        if largos == 'on': tipos.append( 'largo' )
        if compuestos == 'on': tipos.append( 'compuesto' )

        for _ in range( numero ):
            tipo = choice( tipos ) if len( tipos ) > 0 else choice( ['corto', 'largo', 'compuesto'] )

            if tipo == 'largo' or tipo == 'compuesto':
                obj = choice( p.comunes.keys() )
                gen = p.comunes[obj]
                art = "El" if gen == "m" else "La"
                nom = choice( p.propios.keys() )
                if tipo == 'compuesto':
                    adj = choice( p.adjetivos )
                    if gen == "f" and adj[-1] == "o":
                        adj = "{}a".format( adj[:-1] )
                    nombre = "{} {} {} de {}".format( art, adj.capitalize(), obj.capitalize(), nom )
                else:
                    nombre = "{} {} de {}".format( art, obj.capitalize(), nom )
            else:
                adj = choice( p.adjetivos )
                nom = choice( p.propios.keys() )
                gen = p.propios[nom]
                if gen == "f" and adj[-1] == "o":
                    adj = "{}a".format( adj[:-1] )
                nombre = "{} {}".format( adj.capitalize(), nom.capitalize() )
            nombres.append( unicode( nombre, "utf8" ) )
        return nombres

    def get( self ):
        try:
            numero = int( self.request.get( 'numero' ) )
        except:
            numero = 1
        cortos = self.request.get( 'cortos' )
        largos = self.request.get( 'largos' )
        compuestos = self.request.get( 'compuestos' )

        nombres = self.generar_nombres( numero, cortos, largos, compuestos )

        template_values = {
            'nombres' : nombres,
            'numero' : numero,
            'cortos' : cortos,
            'largos' : largos,
            'compuestos' : compuestos,
            'bg' : choice( range( 1, 38 ) ) }
        template = JINJA_ENVIRONMENT.get_template( 'index.html' )
        self.response.write( template.render( template_values ) )

application = webapp2.WSGIApplication( [
    ( '/', MainPage ), ], debug=True )
