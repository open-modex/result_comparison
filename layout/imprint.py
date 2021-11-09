
import dash_html_components as html
from .main import get_header


def get_imprint_layout(app):
    return html.Div(
        children=[
            get_header(app),
            html.Section(
                className="legal",
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.H2("Imprint"),
                                    html.P(
                                        [
                                            "Publisher:",
                                            html.Br(),
                                            "This website is operated by the Reiner Lemoine Institut gGmbH",
                                            html.Br(),
                                            html.Br(),
                                            "Management:",
                                            html.Br(),
                                            "Dr. Kathrin Goldammer",
                                            html.Br(),
                                            html.Br(),
                                            "Postal address:",
                                            html.Br(),
                                            "Reiner Lemoine Institut gGmbH",
                                            html.Br(),
                                            "Rudower Chaussee 12",
                                            html.Br(),
                                            "12489 Berlin",
                                            html.Br(),
                                            html.Br(),
                                            "Telephone +49 (0)30 1208 434 0",
                                            html.Br(),
                                            "Fax +49 (0)30 1208 434 99",
                                            html.Br(),
                                            html.Br(),
                                            "Handelsregister Berlin – HRB 124659 B",
                                            html.Br(),
                                            html.Br(),
                                            "Tax number: 27/602/55211",
                                            html.Br(),
                                            html.Br(),
                                            "VAT-Id.: DE274491408",
                                            html.Br(),
                                            html.Br(),
                                            "Disclaimer:",
                                            html.Br(),
                                            html.Br(),
                                            "1. Haftungshinweis",
                                            html.Br(),
                                            "Die Inhalte sind mit größter Sorgfalt recherchiert. Dennoch übernimmt der Autor keinerlei Gewähr für die Aktualität, Korrektheit, Vollständigkeit oder Qualität der bereitgestellten Informationen. Haftungsansprüche gegen den Autor, welche sich auf Schäden materieller oder ideeller Art beziehen die durch die Nutzung oder Nichtnutzung der dargebotenen Informationen bzw. durch die Nutzung fehlerhafter und unvollständiger Informationen verursacht wurden, sind grundsätzlich ausgeschlossen, sofern seitens des Autors kein nachweislich vorsätzliches oder grob fahrlässiges Verschulden vorliegt. Alle Angebote sind freibleibend und unverbindlich. Der Autor behält es sich ausdrücklich vor, Teile der Seiten oder das gesamte Angebot ohne gesonderte Ankündigung zu verändern, zu ergänzen, zu löschen oder die Veröffentlichung zeitweise oder endgültig einzustellen.",
                                            html.Br(),
                                            html.Br(),
                                            "2. Verweise und Links",
                                            html.Br(),
                                            "Bei direkten oder indirekten Verweisen auf fremde Internetseiten („Links”), die außerhalb des Verantwortungsbereiches des Autors liegen, würde eine Haftungsverpflichtung ausschließlich in dem Fall in Kraft treten, in dem der Autor von den Inhalten Kenntnis hat und es ihm technisch möglich und zumutbar wäre, die Nutzung im Falle rechtswidriger Inhalte zu verhindern. Der Autor erklärt daher ausdrücklich, dass zum Zeitpunkt der Linksetzung die entsprechenden verlinkten Seiten frei von illegalen Inhalten waren. Der Autor hat keinerlei Einfluss auf die aktuelle und zukünftige Gestaltung und auf die Inhalte der gelinkten/verknüpften Seiten. Deshalb distanziert er sich hiermit ausdrücklich von allen Inhalten aller gelinkten /verknüpften Seiten, die nach der Linksetzung verändert wurden. Diese Feststellung gilt für alle innerhalb des eigenen Internetangebotes gesetzten Links und Verweise sowie für Fremdeinträge in vom Autor eingerichteten Gästebüchern, Diskussionsforen und Mailinglisten. Für illegale, fehlerhafte oder unvollständige Inhalte und insbesondere für Schäden, die aus der Nutzung oder Nichtnutzung solcherart dargebotener Informationen entstehen, haftet allein der Anbieter der Seite, auf welche verwiesen wurde, nicht derjenige, der über Links auf die jeweilige Veröffentlichung lediglich verweist.",
                                            html.Br(),
                                            html.Br(),
                                            "3. Urheber- und Kennzeichenrecht",
                                            html.Br(),
                                            "Der Autor ist bestrebt, in allen Publikationen die Urheberrechte der verwendeten Grafiken, Tondokumente, Videosequenzen und Texte zu beachten, von ihm selbst erstellte Grafiken, Tondokumente, Videosequenzen und Texte zu nutzen oder auf lizenzfreie Grafiken, Tondokumente, Videosequenzen und Texte zurückzugreifen. Alle innerhalb des Internetangebotes genannten und ggf. durch Dritte geschützten Marken- und Warenzeichen unterliegen uneingeschränkt den Bestimmungen des jeweils gültigen Kennzeichenrechts und den Besitzrechten der jeweiligen eingetragenen Eigentümer. Allein aufgrund der bloßen Nennung ist nicht der Schluss zu ziehen, dass Markenzeichen nicht durch Rechte Dritter geschützt sind! Das Copyright für veröffentlichte, vom Autor selbst erstellte Objekte bleibt allein beim Autor der Seiten. Eine Vervielfältigung oder Verwendung solcher Grafiken, Tondokumente, Videosequenzen und Texte in anderen elektronischen oder gedruckten Publikationen ist ohne ausdrückliche Zustimmung des Autors nicht gestattet.",
                                            html.Br(),
                                            html.Br(),
                                            "4. Rechtswirksamkeit dieses Haftungsausschlusses",
                                            html.Br(),
                                            "Dieser Haftungsausschluss ist als Teil des Internetangebotes zu betrachten, von dem aus auf diese Seite verwiesen wurde. Sofern Teile oder einzelne Formulierungen dieses Textes der geltenden Rechtslage nicht, nicht mehr oder nicht vollständig entsprechen sollten, bleiben die übrigen Teile des Dokumentes in ihrem Inhalt und ihrer Gültigkeit davon unberührt.",
                                        ]
                                    ),
                                ]
                            )
                        ]
                    )
                ],
            )
        ]
    )
