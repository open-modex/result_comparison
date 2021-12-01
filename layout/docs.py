
import dash_html_components as html
import dash_core_components as dcc

from .main import get_header
from .main import get_footer
from settings import DOCUMENTATION


def get_docs_layout(app):
    return html.Div(
        children=[
            get_header(app),
            html.Section(
                className="legal",
                children=[
                    html.Div(
                        [
                            html.H2("Documentation"),
                            html.P(
                                children=[
                                    dcc.Markdown(DOCUMENTATION)
                                ]
                            ),
                            get_footer()
                        ]
                    )
                ]
            )
        ]
    )
