"""Ampliar el catálogo de juegos conservando fichas y publicación existentes."""
from alembic import op
import sqlalchemy as sa

revision = '0009_more_games'
down_revision = '0008_games'
branch_labels = None
depends_on = None

ADDITIONAL_GAMES = [{'slug': 'sudoku',
  'title': 'Sudoku sencillo',
  'description': 'Completa un tablero de 4 por 4 con números del 1 al 4.',
  'category': 'Lógica',
  'target_url': '/static/juegos/sudoku/index.html'},
 {'slug': 'torres-hanoi',
  'title': 'Torres de Hanói',
  'description': 'Mueve los discos entre torres, uno a uno y sin poner uno grande sobre uno '
                 'pequeño.',
  'category': 'Lógica',
  'target_url': '/static/juegos/torres-hanoi/index.html'},
 {'slug': 'balanza',
  'title': 'Equilibra la balanza',
  'description': 'Combina pesas para conseguir el mismo peso en ambos lados.',
  'category': 'Cálculo',
  'target_url': '/static/juegos/balanza/index.html'},
 {'slug': 'secuencia-luces',
  'title': 'Secuencia de luces',
  'description': 'Observa las figuras iluminadas a tu ritmo y repite el orden.',
  'category': 'Memoria',
  'target_url': '/static/juegos/secuencia-luces/index.html'},
 {'slug': 'bolos',
  'title': 'Bolos tranquilos',
  'description': 'Elige dirección y fuerza para derribar los bolos en dos lanzamientos.',
  'category': 'Coordinación',
  'target_url': '/static/juegos/bolos/index.html'},
 {'slug': 'une-puntos',
  'title': 'Une los puntos',
  'description': 'Toca los números en orden y descubre un dibujo, sin arrastrar.',
  'category': 'Percepción',
  'target_url': '/static/juegos/une-puntos/index.html'},
 {'slug': 'refranes',
  'title': 'Completa el refrán',
  'description': 'Elige la expresión que completa un refrán conocido y descubre su significado.',
  'category': 'Lenguaje',
  'target_url': '/static/juegos/refranes/index.html'},
 {'slug': 'dibujo-cuadricula',
  'title': 'Descubre el dibujo',
  'description': 'Pinta una cuadrícula pequeña siguiendo las pistas de sus filas y columnas.',
  'category': 'Lógica',
  'target_url': '/static/juegos/dibujo-cuadricula/index.html'},
 {'slug': 'codigo-secreto',
  'title': 'Código secreto',
  'description': 'Deduce una combinación de tres figuras usando las pistas de cada intento.',
  'category': 'Lógica',
  'target_url': '/static/juegos/codigo-secreto/index.html'},
 {'slug': 'tesoro',
  'title': 'El tesoro escondido',
  'description': 'Explora casillas y usa las distancias para localizar el tesoro.',
  'category': 'Orientación',
  'target_url': '/static/juegos/tesoro/index.html'}]


def upgrade():
    # RLS está forzado: establecer la organización al insertar su catálogo.
    # No se alteran las fichas que la organización ya tenga configuradas.
    for game in ADDITIONAL_GAMES:
        escaped = {key: value.replace("'", "''") for key, value in game.items()}
        op.execute(sa.text("""
            DO $games$
            DECLARE tenant uuid;
            BEGIN
                FOR tenant IN SELECT id FROM admin.tenants LOOP
                    PERFORM set_config('app.tenant_id', tenant::text, true);
                    INSERT INTO admin.games_apps (tenant_id, slug, title, description, category, target_url)
                    VALUES (tenant, '%(slug)s', '%(title)s', '%(description)s', '%(category)s', '%(target_url)s')
                    ON CONFLICT (tenant_id, slug) DO NOTHING;
                END LOOP;
            END $games$;
        """ % escaped))
    op.execute("SELECT set_config('app.tenant_id', '', true)")


def downgrade():
    raise RuntimeError('El catálogo puede tener cambios de usuarios; no se elimina automáticamente.')
