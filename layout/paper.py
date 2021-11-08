
from typing import List
from dataclasses import dataclass

import dash_html_components as html
from .main import get_header


BASE_SCENARIO_IDS = [183, 184, 197, 214, 215, 216, 225, 230, 231, 237, 238, 239, 240, 241, 249, 250]
SCENARIO_VARIATIONS_IDS = [208, 258, 259, 260, 261, 262, 263, 267, 268, 269, 270, 271]


@dataclass
class Figure:
    image: str
    title: str
    figure_number: int
    page_number: int
    scenario_ids: List[int]
    filter_name: str
    description: str = "No description"
    color_map: str = "No custom color mapping applied"
    labels: str = "No custom label mapping applied"


FIGURES = [
    Figure(
        image="generation_all.svg",
        title="Generation for all power plants of the base scenario, divided into the years 2016,2030, and 2050.",
        figure_number=7,
        page_number=15,
        scenario_ids=BASE_SCENARIO_IDS,
        filter_name="full_generation_V1",
        color_map="energy_sources_new",
        labels="energies_new"
    ),
]


def get_paper_layout(app):
    return html.Div(
        children=[
            get_header(app),
            html.Section(
                className="paper",
                children=[
                    html.Div(
                        [
                            html.H1("Modex results"),
                            html.P(
                                "Most figures from paper "
                                "'Comparing Open Source energy system models - a case study focusing on the transition of the German power sector by applying emission reduction targets' "
                                "have been created using the MODEX dashboard. "
                                "Some of the used scenario IDs and filter settings together with resulting charts can be seen below. "
                                "In order to recreate figures from below, following steps have to be done:"
                            ),
                            html.Ul(
                                [
                                    html.Li("choose given scenario IDs in dropdown 'Scenario',"),
                                    html.Li("load given filter name in dropdown 'Load filters' (left panel, tab 'FILTERS'),"),
                                    html.Li("if color mapping is given, select color mapping in dropdown 'Load colors' (left panel, tab 'PRESENTATION'),"),
                                    html.Li("if label mapping is given, select label mapping in dropdown 'Load labels' (left panel, tab 'PRESENTATION'),"),
                                    html.Li("click on 'REFRESH' button at scalar chart.")
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Hr(),
                                    html.Img(src=app.get_asset_url(f"figures/{figure.image}")),
                                    html.Table(
                                        [
                                            html.Tr(
                                                [
                                                    html.Td("Reference:"),
                                                    html.Td(f"Page {figure.page_number}, Fig. {figure.figure_number}")
                                                ]
                                            ),
                                            html.Tr(
                                                [
                                                    html.Td("Title:"),
                                                    html.Td(figure.title)
                                                ]
                                            ),
                                            html.Tr(
                                                [
                                                    html.Td("Description:"),
                                                    html.Td(figure.description)
                                                ]
                                            ),
                                            html.Tr(
                                                [
                                                    html.Td("Scenario IDs:"),
                                                    html.Td(", ".join(map(str, figure.scenario_ids)))
                                                ]
                                            ),
                                            html.Tr(
                                                [
                                                    html.Td("Filter:"),
                                                    html.Td(figure.filter_name)
                                                ]
                                            ),
                                            html.Tr(
                                                [
                                                    html.Td("Color Map:"),
                                                    html.Td(figure.color_map)
                                                ]
                                            ),
                                            html.Tr(
                                                [
                                                    html.Td("Labels:"),
                                                    html.Td(figure.labels)
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                            for figure in FIGURES
                        ]
                    )
                ]
            )
        ]
    )
