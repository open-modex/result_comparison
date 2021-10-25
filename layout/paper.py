
from typing import List
from dataclasses import dataclass

import dash_html_components as html


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
        image="cost_all.svg",
        title="Variable costs in 2016, 2030, and 2050 for all frameworks.",
        figure_number=4,
        page_number=11,
        scenario_ids=[3, 4, 5],
        filter_name="cost"
    ),
    Figure(
        image="cost_all.svg",
        title="Variable costs in 2016, 2030, and 2050 for all frameworks.",
        figure_number=4,
        page_number=11,
        scenario_ids=[3, 4, 5],
        filter_name="cost"
    )
]


def get_paper_layout(app):
    return html.Section(
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
