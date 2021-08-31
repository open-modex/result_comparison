import uuid
import json
from collections import ChainMap, defaultdict

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table

from graphs import get_empty_fig
from settings import (
    VERSION, SC_FILTERS, TS_FILTERS, UNITS, GRAPHS_DEFAULT_OPTIONS, GRAPHS_DEFAULT_COLOR_MAP, GRAPHS_DEFAULT_LABELS
)
from models import get_model_options, Filter, Colors, Labels


DEFAULT_LAYOUT = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

IMPRINT_LAYOUT = html.Section(
    className="legal",
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1("Imprint"),
                        html.P(
                            [
                                "Publisher:",html.Br(),"This website is operated by the Reiner Lemoine Institut gGmbH",html.Br(),html.Br(),"Management:",html.Br(),"Dr. Kathrin Goldammer",html.Br(),html.Br(),"Postal address:",html.Br(),"Reiner Lemoine Institut gGmbH",html.Br(),"Rudower Chaussee 12",html.Br(),"12489 Berlin",html.Br(),html.Br(),"Telephone +49 (0)30 1208 434 0",html.Br(),"Fax +49 (0)30 1208 434 99",html.Br(),html.Br(),"Handelsregister Berlin – HRB 124659 B",html.Br(),html.Br(),"Tax number: 27/602/55211",html.Br(),html.Br(),"VAT-Id.: DE274491408",html.Br(),html.Br(),"Disclaimer:",html.Br(),html.Br(),"1. Haftungshinweis",html.Br(),"Die Inhalte sind mit größter Sorgfalt recherchiert. Dennoch übernimmt der Autor keinerlei Gewähr für die Aktualität, Korrektheit, Vollständigkeit oder Qualität der bereitgestellten Informationen. Haftungsansprüche gegen den Autor, welche sich auf Schäden materieller oder ideeller Art beziehen die durch die Nutzung oder Nichtnutzung der dargebotenen Informationen bzw. durch die Nutzung fehlerhafter und unvollständiger Informationen verursacht wurden, sind grundsätzlich ausgeschlossen, sofern seitens des Autors kein nachweislich vorsätzliches oder grob fahrlässiges Verschulden vorliegt. Alle Angebote sind freibleibend und unverbindlich. Der Autor behält es sich ausdrücklich vor, Teile der Seiten oder das gesamte Angebot ohne gesonderte Ankündigung zu verändern, zu ergänzen, zu löschen oder die Veröffentlichung zeitweise oder endgültig einzustellen.",html.Br(),html.Br(),"2. Verweise und Links",html.Br(),"Bei direkten oder indirekten Verweisen auf fremde Internetseiten („Links”), die außerhalb des Verantwortungsbereiches des Autors liegen, würde eine Haftungsverpflichtung ausschließlich in dem Fall in Kraft treten, in dem der Autor von den Inhalten Kenntnis hat und es ihm technisch möglich und zumutbar wäre, die Nutzung im Falle rechtswidriger Inhalte zu verhindern. Der Autor erklärt daher ausdrücklich, dass zum Zeitpunkt der Linksetzung die entsprechenden verlinkten Seiten frei von illegalen Inhalten waren. Der Autor hat keinerlei Einfluss auf die aktuelle und zukünftige Gestaltung und auf die Inhalte der gelinkten/verknüpften Seiten. Deshalb distanziert er sich hiermit ausdrücklich von allen Inhalten aller gelinkten /verknüpften Seiten, die nach der Linksetzung verändert wurden. Diese Feststellung gilt für alle innerhalb des eigenen Internetangebotes gesetzten Links und Verweise sowie für Fremdeinträge in vom Autor eingerichteten Gästebüchern, Diskussionsforen und Mailinglisten. Für illegale, fehlerhafte oder unvollständige Inhalte und insbesondere für Schäden, die aus der Nutzung oder Nichtnutzung solcherart dargebotener Informationen entstehen, haftet allein der Anbieter der Seite, auf welche verwiesen wurde, nicht derjenige, der über Links auf die jeweilige Veröffentlichung lediglich verweist.",html.Br(),html.Br(),"3. Urheber- und Kennzeichenrecht",html.Br(),"Der Autor ist bestrebt, in allen Publikationen die Urheberrechte der verwendeten Grafiken, Tondokumente, Videosequenzen und Texte zu beachten, von ihm selbst erstellte Grafiken, Tondokumente, Videosequenzen und Texte zu nutzen oder auf lizenzfreie Grafiken, Tondokumente, Videosequenzen und Texte zurückzugreifen. Alle innerhalb des Internetangebotes genannten und ggf. durch Dritte geschützten Marken- und Warenzeichen unterliegen uneingeschränkt den Bestimmungen des jeweils gültigen Kennzeichenrechts und den Besitzrechten der jeweiligen eingetragenen Eigentümer. Allein aufgrund der bloßen Nennung ist nicht der Schluss zu ziehen, dass Markenzeichen nicht durch Rechte Dritter geschützt sind! Das Copyright für veröffentlichte, vom Autor selbst erstellte Objekte bleibt allein beim Autor der Seiten. Eine Vervielfältigung oder Verwendung solcher Grafiken, Tondokumente, Videosequenzen und Texte in anderen elektronischen oder gedruckten Publikationen ist ohne ausdrückliche Zustimmung des Autors nicht gestattet.",html.Br(),html.Br(),"4. Rechtswirksamkeit dieses Haftungsausschlusses",html.Br(),"Dieser Haftungsausschluss ist als Teil des Internetangebotes zu betrachten, von dem aus auf diese Seite verwiesen wurde. Sofern Teile oder einzelne Formulierungen dieses Textes der geltenden Rechtslage nicht, nicht mehr oder nicht vollständig entsprechen sollten, bleiben die übrigen Teile des Dokumentes in ihrem Inhalt und ihrer Gültigkeit davon unberührt."
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

dataProcessing = [
    "Informationen über den Browsertyp und die verwendete Version",
    "Das Betriebssystem",
    "Den Internet-Service-Provider",
    "Die IP-Adresse der Nutzer*in",
    "Datum und Uhrzeit des Zugriffs",
    "Websites, von denen das System der Nutzer*in auf unsere Internetseite gelangt",
    "Websites, die vom System der Nutzer*in über unsere Website aufgerufen werden"
    ]

PRIVACY_LAYOUT = html.Section(
    className="legal",
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1("Data Protection"),
                        html.H4("I. Name und Anschrift der Verantwortlichen"),
                        html.P(
                            [
                                "Der Verantwortliche im Sinne der Datenschutz-Grundverordnung und anderer nationaler Datenschutzgesetze der Mitgliedsstaaten sowie sonstiger datenschutzrechtlicher Bestimmungen ist die:",html.Br(),html.Br(),"Reiner Lemoine Institut gGmbH",html.Br(),"Rudower Chaussee 12",html.Br(),"12489 Berlin",html.Br(),"Telefon +49 (0)30 1208 434 0",html.Br(),"Fax +49 (0)30 1208 434 99",html.Br(),"E-Mail: info@rl-institut.de",html.Br(),"Website: https://reiner-lemoine-institut.de/"
                            ]
                        ),
                        html.H4("II. Datenschutzbeauftragte"),
                        html.P(
                            [
                                "Dr. Christine Kühnel",html.Br(),"Reiner Lemoine Institut gGmbH",html.Br(),"Rudower Chaussee 12",html.Br(),"12489 Berlin",html.Br(),"Telefon +49 (0)30 1208 434 17",html.Br(),"Fax +49 (0)30 1208 434 99",html.Br(),"E-Mail: datenschutz@rl-institut.de"
                            ]
                        ),
                        html.H4("III. Allgemeines zur Datenverarbeitung"),
                        html.P(
                            [
                                html.Strong("1. Umfang der Verarbeitung personenbezogener Daten"),html.Br(),html.Br(),"Wir verarbeiten personenbezogene Daten unserer Nutzer*innen grundsätzlich nur, soweit dies zur Bereitstellung einer funktionsfähigen Website sowie unserer Inhalte und Leistungen erforderlich ist. Die Verarbeitung personenbezogener Daten unserer Nutzer*innen erfolgt regelmäßig nur nach deren Einwilligung. Eine Ausnahme gilt in solchen Fällen, in denen eine vorherige Einholung einer Einwilligung aus tatsächlichen Gründen nicht möglich ist und die Verarbeitung der Daten durch gesetzliche Vorschriften gestattet ist. ",html.Br(),html.Br(),html.Strong(" 2. Rechtsgrundlage für die Verarbeitung personenbezogener Daten"),html.Br(),html.Br(),"Soweit wir für Verarbeitungsvorgänge personenbezogener Daten eine Einwilligung der betroffenen Person einholen, dient Art. 6 Abs. 1 lit. a EU-Datenschutzgrundverordnung (DSGVO) als Rechtsgrundlage. ",html.Br(),"Bei der Verarbeitung von personenbezogenen Daten, die zur Erfüllung eines Vertrages, dessen Vertragspartei die betroffene Person ist, erforderlich ist, dient Art. 6 Abs. 1 lit. b DSGVO als Rechtsgrundlage. Dies gilt auch für Verarbeitungsvorgänge, die zur Durchführung vorvertraglicher Maßnahmen erforderlich sind. ",html.Br(),"Soweit eine Verarbeitung personenbezogener Daten zur Erfüllung einer rechtlichen Verpflichtung erforderlich ist, der unser Unternehmen unterliegt, dient Art. 6 Abs. 1 lit. c DSGVO als Rechtsgrundlage. ",html.Br(),"Für den Fall, dass lebenswichtige Interessen der betroffenen Person oder einer anderen natürlichen Person eine Verarbeitung personenbezogener Daten erforderlich machen, dient Art. 6 Abs. 1 lit. d DSGVO als Rechtsgrundlage. ",html.Br(),"Ist die Verarbeitung zur Wahrung eines berechtigten Interesses unseres Unternehmens oder eines Dritten erforderlich und überwiegen die Interessen, Grundrechte und Grundfreiheiten des Betroffenen das erstgenannte Interesse nicht, so dient Art. 6 Abs. 1 lit. f DSGVO als Rechtsgrundlage für die Verarbeitung.",html.Br(),html.Br(),html.Strong(" 3. Datenlöschung und Speicherdauer"),html.Br(),html.Br(),"Die personenbezogenen Daten der betroffenen Person werden gelöscht oder gesperrt, sobald der Zweck der Speicherung entfällt. Eine Speicherung kann darüber hinaus erfolgen, wenn dies durch den europäischen oder nationalen Gesetzgeber in unionsrechtlichen Verordnungen, Gesetzen oder sonstigen Vorschriften, denen der Verantwortliche unterliegt, vorgesehen wurde. Eine Sperrung oder Löschung der Daten erfolgt auch dann, wenn eine durch die genannten Normen vorgeschriebene Speicherfrist abläuft, es sei denn, dass eine Erforderlichkeit zur weiteren Speicherung der Daten für einen Vertragsabschluss oder eine Vertragserfüllung besteht."
                            ]
                        ),
                        html.H4("IV. Bereitstellung der Website und Erstellung von Logfiles"),
                        html.Div(
                            children=[
                                html.H5(" 1. Beschreibung und Umfang der Datenverarbeitung"),html.P("Bei jedem Aufruf unserer Internetseite erfasst unser System automatisiert Daten und Informationen vom Computersystem des aufrufenden Rechners. Folgende Daten werden hierbei erhoben:"),html.Ul(id='my-list', children=[html.Li(i) for i in dataProcessing]),html.P("Die Daten werden ebenfalls in den Logfiles unseres Systems gespeichert. Eine Speicherung dieser Daten zusammen mit anderen personenbezogenen Daten findet nicht statt."),html.H5(" 2. Rechtsgrundlage für die Datenverarbeitung "),html.P("Rechtsgrundlage für die vorübergehende Speicherung der Daten und der Logfiles ist Art. 6 Abs. 1 lit. f DSGVO."),html.H5(" 3. Zweck der Datenverarbeitung"),html.P("Die vorübergehende Speicherung der IP-Adresse durch das System ist notwendig, um eine Auslieferung der Website an den Rechner der Nutzer*in zu ermöglichen. Hierfür muss die IP-Adresse der Nutzer*in für die Dauer der Sitzung gespeichert bleiben. <br>Die Speicherung in Logfiles erfolgt, um die Funktionsfähigkeit der Website sicherzustellen. Zudem dienen uns die Daten zur Optimierung der Website und zur Sicherstellung der Sicherheit unserer informationstechnischen Systeme. Eine Auswertung der Daten zu Marketingzwecken findet in diesem Zusammenhang nicht statt. <br>In diesen Zwecken liegt auch unser berechtigtes Interesse an der Datenverarbeitung nach Art. 6 Abs. 1 lit. f DSGVO. "),html.H5(" 4. Dauer der Speicherung"),html.P("Die Daten werden gelöscht, sobald sie für die Erreichung des Zweckes ihrer Erhebung nicht mehr erforderlich sind. Im Falle der Erfassung der Daten zur Bereitstellung der Website ist dies der Fall, wenn die jeweilige Sitzung beendet ist. <br>Im Falle der Speicherung der Daten in Logfiles ist dies nach spätestens sieben Tagen der Fall. Eine darüberhinausgehende Speicherung ist möglich. In diesem Fall werden die IP-Adressen gelöscht oder verfremdet, sodass eine Zuordnung des aufrufenden Clients nicht mehr möglich ist."),html.H5(" 5. Widerspruchs- und Beseitigungsmöglichkeit"),html.P("Die Erfassung der Daten zur Bereitstellung der Website und die Speicherung der Daten in Logfiles ist für den Betrieb der Internetseite zwingend erforderlich. Es besteht folglich seitens des Nutzer*ins keine Widerspruchsmöglichkeit.")
                            ]
                        ),
                    ]
                )
            ]
        )
    ]
)


def get_header(app):
    return html.Section(
        className="header",
        children=[
            html.Div(
                className="header__content",
                children=[
                    html.Div(
                        className="header__logo",
                        children=[
                            html.Img(
                                src=app.get_asset_url("open_Modex-logo.png")
                            )
                        ],
                    ),
                    html.Div(
                        className="header__heading",
                        children=[
                            html.P(
                                children=f"Version v{VERSION}",
                                className="version"
                                ),
                            html.H1(
                                children="Energy Frameworks to Germany",
                                className="title"
                                ),
                            html.P(
                                children="How to efficiently sustain Germany's energy "
                                "\n usage with efficient parameters based on regions.",
                                className="subtitle"
                            ),
                        ],
                    ),
                ]
            ),
            dbc.NavbarSimple(
                className="header__nav",
                children=[
                    dbc.NavItem(dbc.NavLink("About", href="#")),
                    dbc.NavItem(dbc.NavLink("Contact", href="#"))
                ],
                dark=False,
                expand="xl"
            )
        ],
    )


def get_scenario_column(scenarios):
    return html.Div(
        className="scenarios",
        style={"padding-bottom": "50px"},
        children=[
            html.Label("Scenario"),
            dcc.Dropdown(
                id="dd_scenario",
                className="scenarios__dropdown",  # This is a dash component with additonal class name
                multi=True,
                options=[
                    {
                        "label": f"{scenario['id']}, {scenario['scenario']}, {scenario['source']}",
                        "value": scenario["id"],
                    }
                    for scenario in scenarios
                ],
            ),
            dbc.Button(
                "Reload",
                id="scenario_reload",
                className="scenarios__btn btn btn--refresh disabled"
            ), # This is bootstrap component with additional class
            html.Div(
                className="scenarios__views",
                children=[
                    html.Div(
                        className="view view--dashboard active"
                    ),
                    html.Div(
                        className="view view--data"
                    ),
                    html.Div(
                        className="view view--dashboard-data"
                    )
                ]
            )
        ],
    )


def get_graph_options(data_type, graph_type, preset_options=None):
    preset_options = preset_options or {}
    chosen_options = ChainMap(preset_options, GRAPHS_DEFAULT_OPTIONS[data_type][graph_type].get_defaults())
    if data_type == "scalars":
        dd_options = [{"label": "value", "value": "value"}] + [
            {"label": filter_, "value": filter_} for filter_ in SC_FILTERS
        ]
    else:
        dd_options = [{"label": "series", "value": "series"}] + [
            {"label": filter_, "value": filter_} for filter_ in TS_FILTERS
        ]

    tabs = defaultdict(list)
    for option, value in chosen_options.items():
        if GRAPHS_DEFAULT_OPTIONS[data_type][graph_type][option].from_filter:
            options = dd_options
        else:
            options = GRAPHS_DEFAULT_OPTIONS[data_type][graph_type][option].default
        component_type = GRAPHS_DEFAULT_OPTIONS[data_type][graph_type][option].type
        if component_type == "dropdown":
            component = dcc.Dropdown(
                id=f"{data_type}-{option}",
                options=options,
                value=value,
                clearable=GRAPHS_DEFAULT_OPTIONS[data_type][graph_type][option].clearable
            )
        elif component_type in ("input", "number"):
            component = dcc.Input(
                id=f"{data_type}-{option}",
                value=value,
                type="text" if component_type == "input" else "number"
            )
        elif component_type == "bool":
            component = dcc.Checklist(
                id=f"{data_type}-{option}",
                options=options,
                value=[value],
            )
        else:
            raise ValueError("Unknown dcc component")
        tabs[GRAPHS_DEFAULT_OPTIONS[data_type][graph_type][option].category] += [
            html.Label(GRAPHS_DEFAULT_OPTIONS[data_type][graph_type][option].label),
            component
        ]
    tabs[next(iter(tabs.keys()))].insert(0, dcc.Input(type="hidden", name="graph_type", value=graph_type))
    return dbc.Tabs(
        [dbc.Tab(tab, label=label) for label, tab in tabs.items()]
    )


def get_save_load_column(app):
    with app.server.app_context():
        options = get_model_options(Filter)
    return html.P(
        children=[
            html.P(id=f"save_load_errors", children=""),
            html.Label("Save filters as:"),
            dcc.Input(id="save_filters_name", type="text"),
            html.Button("Save", id="save_filters"),
            html.Label("Load filters"),
            dcc.Dropdown(
                id="load_filters",
                options=options,
                clearable=True
            )
        ]
    )


def get_aggregation_order_column():
    return html.Div(
        className="filter-section",
        children=[
            html.P("Order/Aggregation"),
            html.Label("Order-By:"),
            dcc.Dropdown(
                id="order_by",
                multi=True,
                clearable=True,
                options=[{"label": filter_, "value": filter_} for filter_ in SC_FILTERS],
            ),
            html.Label("Group-By:"),
            dcc.Dropdown(
                id="aggregation_group_by",
                multi=True,
                clearable=True,
                options=[{"label": filter_, "value": filter_} for filter_ in SC_FILTERS],
            )
        ]
    )


def get_units_column():
    return html.Div(
        id="units",
        className="filter-section",
        children=sum(
            (
                [
                    html.Label(unit_name),
                    dcc.Dropdown(
                        options=[
                            {"label": unit, "value": unit}
                            for unit in unit_data["units"]
                        ],
                        value=unit_data["default"],
                        clearable=False,
                    ),
                ]
                for unit_name, unit_data in UNITS.items()
            ),
            [html.P("Units")],
        ),
    )


def get_filter_column():
    return html.Div(
        id="filters",
        className="filter-section",
        children=sum(
            (
                [
                    html.Label(f"Filter {filter_.capitalize()}"),
                    dcc.Dropdown(
                        id=f"filter-{filter_}", multi=True, clearable=True
                    ),
                ]
                for filter_ in SC_FILTERS
            ),
            [html.P("General")],
        ),
    )


def get_color_column(app):
    with app.server.app_context():
        options = get_model_options(Colors)
    return html.Div(
        className="filter__colors",
        children=[
            html.Label(f"Color Map"),
            dcc.Textarea(
                id="colors", value=json.dumps(GRAPHS_DEFAULT_COLOR_MAP), style={"width": "100%", "height": "50px"}
            ),
            html.Label("Save colors as:"),
            html.Div(
                className="save",
                children=[
                    dcc.Input(id="save_colors_name", type="text"),
                    html.Button("Save", id="save_colors"),
                ]
            ),
            html.Label("Load colors"),
            dcc.Dropdown(
                id="load_colors",
                options=options,
                clearable=True
            ),
            html.P(id="colors_error", children="")
        ]
    )


def get_label_column(app):
    with app.server.app_context():
        options = get_model_options(Labels)
    return html.Div(
        className="filter__labels",
        children=[
            html.Label(f"Labels"),
            dcc.Textarea(
                id="labels", value=json.dumps(GRAPHS_DEFAULT_LABELS), style={"width": "100%", "height": "50px"}
            ),
            html.Label("Save labels as:"),
            html.Div(
                className="save",
                children=[
                    dcc.Input(id="save_labels_name", type="text"),
                    html.Button("Save", id="save_labels"),
                ]
            ),
            html.Label("Load labels"),
            dcc.Dropdown(
                id="load_labels",
                options=options,
                clearable=True
            ),
            html.P(id="labels_error", children="")
        ]
    )


def get_graph_column():
    return html.Div(
        className="charts",
        children=[
            html.Div(
                className="charts__item",
                children=[
                    html.Div(
                        className="graph",
                        children=[
                            html.Div(
                                className="graph__view",
                                children=[
                                    dcc.Checklist(id=f"show_{graph}_data", options=[{"label": "Show Data", "value": "True"}]),
                                    dcc.RadioItems(
                                        id=f"graph_{graph}_plot_switch",
                                        options=[
                                            {"label": graph_type.capitalize(), "value": graph_type}
                                            for graph_type in GRAPHS_DEFAULT_OPTIONS[graph].keys()
                                        ],
                                        value=list(GRAPHS_DEFAULT_OPTIONS[graph].keys())[0]
                                    ),
                                    html.Button(f"Refresh", id=f"refresh_{graph}", className="btn btn--refresh disabled")
                                ]
                            ),
                            dcc.Loading(
                                style={"padding-bottom": "30px"},
                                type="default",
                                children=dbc.Tabs(
                                    [
                                        dbc.Tab(
                                            dcc.Graph(
                                                id=f"graph_{graph}",
                                                figure=get_empty_fig(),
                                                style={},
                                                config={
                                                    'toImageButtonOptions': {
                                                        'format': 'svg',
                                                    }
                                                }
                                            ),
                                            label="Chart"
                                        ),
                                        dbc.Tab(
                                            html.P(id=f"graph_{graph}_error", children=""),
                                            id=f"tab_{graph}_error",
                                            label="Errors",
                                        ),
                                    ]
                                )
                            ),
                            dash_table.DataTable(
                                id=f"table_{graph}",
                                export_format="csv",
                                style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                                style_cell={
                                    'backgroundColor': 'rgb(50, 50, 50)',
                                    'color': 'white'
                                },
                            )
                        ]
                    ),
                    html.Div(
                        className="chart-settings",
                        children=[
                            html.Div(
                                className="chart-settings__title",
                                children="Chart settings"
                            ),
                            html.Div(
                                className="chart-settings__form",
                                id=f"graph_{graph}_options",
                                children=get_graph_options(graph, list(GRAPHS_DEFAULT_OPTIONS[graph].keys())[0])
                            )
                        ]

                    )
                ]
            )
            for graph in ("scalars", "timeseries")
        ],
    )

def get_footer():
    return html.Div(
        className="footer",
        children=[
            html.A("Imprint", href="#", className="nav-link"),
            html.A("Data Privacy", href="#", className="nav-link")
        ]
    )

def get_layout(app, scenarios):
    session_id = str(uuid.uuid4())

    return html.Div(
        children=[
            html.Div(session_id, id="session-id", style={"display": "none"}),
            get_header(app),
            html.Main(
                className="dashboard",
                children=[
                    get_scenario_column(scenarios),
                    html.Div(
                        className="content",
                        children=[
                            dbc.Tabs(
                                [
                                    dbc.Tab(
                                        [
                                            get_filter_column(),
                                            get_aggregation_order_column(),
                                            get_save_load_column(app),
                                            get_units_column(),
                                        ],
                                        className="test",
                                        label="Filters"
                                    ),
                                    dbc.Tab(
                                        [
                                            get_color_column(app),
                                            get_label_column(app),
                                        ],
                                        label="Presentation"
                                    )
                                ],
                            ),
                            get_graph_column()
                        ]
                    ),
                    get_footer()
                ],
            ),
        ],
    )


def get_error_and_warnings_div(errors=None, warnings=None, infos=None):
    errors = errors or []
    warnings = warnings or []
    infos = infos or []
    return html.Div(
        children=(
            [html.P(error, style={"color": "red"}) for error in errors] +
            [html.P(warning, style={"color": "orange"}) for warning in warnings] +
            [html.P(info) for info in infos]
        )
    )
