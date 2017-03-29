# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, invalid-name, import-error

import os
import jinja2
import webapp2

from google.appengine.api import images
from google.appengine.ext import ndb

from model import Professor

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        professor_key = ndb.Key(urlsafe=self.request.get('img_id'))
        professor = professor_key.get()
        if professor.foto:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(professor.foto)
        else:
            self.response.out.write('No image')

class MainHandler(Handler):
    def get(self):
        self.write("Olá Mundo!")

class ProfessorHandler(Handler):
    def get(self):
        professores = Professor.query()

        self.render("professor.html", professores=professores)

    def post(self):
        nome   = self.request.get("nome")
        area   = self.request.get("area")
        perfil = self.request.get("perfil")
        email  = self.request.get("email")
        foto   = self.request.get("img")

        professor = Professor(nome=nome, area=area, perfil=perfil,
                              email=email, foto=foto)
        professor.put()

class CursoHandler(Handler):
    def get(self):
        cursos = Curso.query()

        self.render("curso.html", cursos=cursos)

    def post(self):
        nome      = self.request.get("nome")
        periodos  = self.request.get("periodos")
        semestral = self.request.get("semestral")

        curso = Curso(nome=nome, periodos=periodos, semestral=semestral)
        curso.put()

class DisciplinaHandler(Handler):
    def get(self):
        disciplinas = Disciplina.query()

        self.render("disciplina.html", disciplinas=disciplinas)

    def post(self):
        nome     = self.request.get("nome")
        periodos = self.request.get("periodos")

        disciplina = Disciplina(nome=nome, periodos=periodos)
        disciplina.put()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/professor', ProfessorHandler),
    ('/cuso', CursoHandler),
    ('/disciplina', DisciplinaHandler),
    ('/img', ImageHandler)
], debug=True)
