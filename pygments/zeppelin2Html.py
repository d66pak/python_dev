import json
import codecs
import click
from pygments.styles import get_all_styles
from pygments import highlight
from pygments.lexers import ScalaLexer
from pygments.lexers import BashLexer
from pygments.lexers import PythonConsoleLexer
from pygments.formatters import HtmlFormatter

STYLES = list(get_all_styles())


@click.command()
@click.argument('zeppelin_file', type=click.Path(exists=True))
@click.option('-s', '--style', type=click.Choice(STYLES), default='monokai')
def convert(zeppelin_file, style):
    click.echo('Converting Zeppelin file: %s to PDF using style: %s' % (zeppelin_file, style))

    with codecs.open(zeppelin_file, 'r', 'utf-8-sig') as z:
        d_zeppelin = json.load(z)
        formatter = HtmlFormatter(full=False, style=style)
        html = []
        html += '<link rel="stylesheet" type="text/css" href="style.css">'
        for d_para in d_zeppelin['paragraphs']:
            lang = d_zeppelin['config']['editorSetting']['language']
            if lang == 'markdown':
                html.extend(markdown2Html(formatter, d_para))
            elif lang == 'sh':
                html.extend(bash2Html(formatter, d_para))
            elif lang == 'scala':
                html.extend(scala2Html(formatter, d_para))
            else:
                html.extend(text2Html(formatter, d_para))
                html.extend(result2Html(formatter, d_para))
        with open('style.css', 'w') as f:
            f.write(formatter.get_style_defs('body'))


def scala2Html(formatter, d_para):
    html = []
    html += highlight(d_para['text'], ScalaLexer(), formatter)
    html.extend(result2Html(formatter, d_para))
    return html


def markdown2Html(formatter, d_para):
    html = [d_msg['data'] for d_msg in d_para['results']['msg']]
    return "\n".join(html)


def text2Html(formatter, d_para):
    html = []
    html += highlight(d_para['text'], PythonConsoleLexer(), formatter)
    return html


def result2Html(formatter, d_para):
    html = [highlight(d_msg['data'], PythonConsoleLexer(), formatter) for d_msg in d_para['results']['msg']]
    return "\n".join(html)


def bash2Html(formatter, d_para):
    html = []
    html += highlight(d_para['text'].strip('%sh '), BashLexer(), formatter)
    html.extend(result2Html(formatter, d_para))
    return html


if __name__ == '__main__':
    convert()
