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

privacyDataProcessing = [
    "Informationen über den Browsertyp und die verwendete Version",
    "Das Betriebssystem",
    "Den Internet-Service-Provider",
    "Die IP-Adresse der Nutzer*in",
    "Datum und Uhrzeit des Zugriffs",
    "Websites, von denen das System der Nutzer*in auf unsere Internetseite gelangt",
    "Websites, die vom System der Nutzer*in über unsere Website aufgerufen werden"
    ]

privacyCookies = [
    "Informationen über den Browsertyp und die verwendete Version",
    "Das Betriebssystem",
    "Den Internet-Service-Provider",
    "Die IP-Adresse der Nutzer*in",
    "Datum und Uhrzeit des Zugriffs",
    "Websites, von denen das System der Nutzer*in auf unsere Internetseite gelangt",
    "Websites, die vom System der Nutzer*in über unsere Website aufgerufen werden",
    "Eingegebene Suchbegriffe",
    "Häufigkeit von Seitenaufrufen",
    "Inanspruchnahme von Website-Funktionen"
]

privacyWebAnalysis = [
    "Zwei Bytes der IP-Adresse des aufrufenden Systems",
    "Die aufgerufene Webseite",
    "Die Website, von der die Nutzer*in auf die aufgerufene Webseite gelangt ist (Referrer)",
    "Die Unterseiten, die von der aufgerufenen Webseite aus aufgerufen werden",
    "Die Verweildauer auf der Webseite",
    "Die Häufigkeit des Aufrufs der Webseite"
]

privacyRights = [
    "die Zwecke, zu denen die personenbezogenen Daten verarbeitet werden;",
    "die Kategorien von personenbezogenen Daten, welche verarbeitet werden;",
    "die Empfänger*innen bzw. die Kategorien von Empfänger*innen, gegenüber denen die Sie betreffenden personenbezogenen Daten offengelegt wurden oder noch offengelegt werden;",
    "die geplante Dauer der Speicherung der Sie betreffenden personenbezogenen Daten oder, falls konkrete Angaben hierzu nicht möglich sind, Kriterien für die Festlegung der Speicherdauer;",
    "das Bestehen eines Rechts auf Berichtigung oder Löschung der Sie betreffenden personenbezogenen Daten, eines Rechts auf Einschränkung der Verarbeitung durch die verantwortliche Person oder eines Widerspruchsrechts gegen diese Verarbeitung;",
    "das Bestehen eines Beschwerderechts bei einer Aufsichtsbehörde;",
    "alle verfügbaren Informationen über die Herkunft der Daten, wenn die personenbezogenen Daten nicht bei der betroffenen Person erhoben werden;",
    "das Bestehen einer automatisierten Entscheidungsfindung einschließlich Profiling gemäß Art. 22 Abs. 1 und 4 DSGVO und – zumindest in diesen Fällen – aussagekräftige Informationen über die involvierte Logik sowie die Tragweite und die angestrebten Auswirkungen einer derartigen Verarbeitung für die betroffene Person."
]

privacyDataProcessingRights = [
    "wenn Sie die Richtigkeit der Sie betreffenden personenbezogenen für eine Dauer bestreiten, die es den verantwortlichen Personen ermöglicht, die Richtigkeit der personenbezogenen Daten zu überprüfen;",
    "die Verarbeitung unrechtmäßig ist und Sie die Löschung der personenbezogenen Daten ablehnen und stattdessen die Einschränkung der Nutzung der personenbezogenen Daten verlangen;",
    "die verantwortliche Person die personenbezogenen Daten für die Zwecke der Verarbeitung nicht länger benötigt, Sie diese jedoch zur Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen benötigen, oder",
    "wenn Sie Widerspruch gegen die Verarbeitung gemäß Art. 21 Abs. 1 DSGVO eingelegt haben und noch nicht feststeht, ob die berechtigten Gründe der Verantwortlichen gegenüber Ihren Gründen überwiegen."
]

privacyDataDeletion = [
    "Die Sie betreffenden personenbezogenen Daten sind für die Zwecke, für die sie erhoben oder auf sonstige Weise verarbeitet wurden, nicht mehr notwendig.",
    "Sie widerrufen Ihre Einwilligung, auf die sich die Verarbeitung gem. Art. 6 Abs. 1 lit. a oder Art. 9 Abs. 2 lit. a DSGVO stützte, und es fehlt an einer anderweitigen Rechtsgrundlage für die Verarbeitung.",
    "Sie legen gem. Art. 21 Abs. 1 DSGVO Widerspruch gegen die Verarbeitung ein und es liegen keine vorrangigen berechtigten Gründe für die Verarbeitung vor, oder Sie legen gem. Art. 21 Abs. 2 DSGVO Widerspruch gegen die Verarbeitung ein.",
    "Die Sie betreffenden personenbezogenen Daten wurden unrechtmäßig verarbeitet.",
    "Die Löschung der Sie betreffenden personenbezogenen Daten ist zur Erfüllung einer rechtlichen Verpflichtung nach dem Unionsrecht oder dem Recht der Mitgliedstaaten erforderlich, dem die verantwortliche Person unterliegt.",
    "Die Sie betreffenden personenbezogenen Daten wurden in Bezug auf angebotene Dienste der Informationsgesellschaft gemäß Art. 8 Abs. 1 DSGVO erhoben."
]

privacyDataDeletionExceptions = [
    "zur Ausübung des Rechts auf freie Meinungsäußerung und Information;",
    "zur Erfüllung einer rechtlichen Verpflichtung, die die Verarbeitung nach dem Recht der Union oder der Mitgliedstaaten, dem der Verantwortliche unterliegt, erfordert, oder zur Wahrnehmung einer Aufgabe, die im öffentlichen Interesse liegt oder in Ausübung öffentlicher Gewalt erfolgt, die dem Verantwortlichen übertragen wurde;",
    "aus Gründen des öffentlichen Interesses im Bereich der öffentlichen Gesundheit gemäß Art. 9 Abs. 2 lit. h und i sowie Art. 9 Abs. 3 DSGVO;",
    "für im öffentlichen Interesse liegende Archivzwecke, wissenschaftliche oder historische Forschungszwecke oder für statistische Zwecke gem. Art. 89 Abs. 1 DSGVO, soweit das unter Abschnitt a) genannte Recht voraussichtlich die Verwirklichung der Ziele dieser Verarbeitung unmöglich macht oder ernsthaft beeinträchtigt, oder",
    "zur Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen."
]

privacyDataTransfer = [
    "die Verarbeitung auf einer Einwilligung gem. Art. 6 Abs. 1 lit. a DSGVO oder Art. 9 Abs. 2 lit. a DSGVO oder auf einem Vertrag gem. Art. 6 Abs. 1 lit. b DSGVO beruht und",
    "die Verarbeitung mithilfe automatisierter Verfahren erfolgt."
]

privacyProfiling = [
    "für den Abschluss oder die Erfüllung eines Vertrags zwischen Ihnen und der verantwortlichen Person erforderlich ist,",
    "aufgrund von Rechtsvorschriften der Union oder der Mitgliedstaaten, denen der Verantwortliche unterliegt, zulässig ist und diese Rechtsvorschriften angemessene Maßnahmen zur Wahrung Ihrer Rechte und Freiheiten sowie Ihrer berechtigten Interessen enthalten oder",
    "mit Ihrer ausdrücklichen Einwilligung erfolgt."
]

cookies_table_header = [
    html.Thead(html.Tr([html.Th("Cookie-Name"), html.Th("Zweck"), html.Th("Aufbewahrungszeit")]))
]

row1 = html.Tr([html.Td("_pk_id.x.xxxx"), html.Td("Diese Cookies werden von der Open-Source-Software Matomo (Piwik) für die statistische Auswertung der Besucherzugriffe verwendet. Sollte sich ein Besucher gegen die statistische Auswertung seines Besucherzugriffs durch Matomo (Piwik) entscheiden, wird das Cookie piwik_ignore gesetzt."), html.Td("13 Monate")])
row2 = html.Tr([html.Td("_pk_ses.x.xxxx"), html.Td("Diese Cookies werden von der Open-Source-Software Matomo (Piwik) für die statistische Auswertung der Besucherzugriffe verwendet. Sollte sich ein Besucher gegen die statistische Auswertung seines Besucherzugriffs durch Matomo (Piwik) entscheiden, wird das Cookie piwik_ignore gesetzt."), html.Td("30 Minuten")])
row3 = html.Tr([html.Td("PIWIK_SESSID"), html.Td("ID der Sitzung des Analysediensts Matomo."), html.Td("Bis zum Ende der Browsersitzung")])
row4 = html.Tr([html.Td("piwik_ignore"), html.Td("Sollte sich ein Besucher gegen die statistische Auswertung seines Besucherzugriffs durch Matomo (Piwik) entscheiden, wird dieses Cookie gesetzt."), html.Td("24 Monate")])

cookies_table_body = [html.Tbody([row1, row2, row3, row4])]

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
                                html.H5("1. Umfang der Verarbeitung personenbezogener Daten"),
                                html.P("Wir verarbeiten personenbezogene Daten unserer Nutzer*innen grundsätzlich nur, soweit dies zur Bereitstellung einer funktionsfähigen Website sowie unserer Inhalte und Leistungen erforderlich ist. Die Verarbeitung personenbezogener Daten unserer Nutzer*innen erfolgt regelmäßig nur nach deren Einwilligung. Eine Ausnahme gilt in solchen Fällen, in denen eine vorherige Einholung einer Einwilligung aus tatsächlichen Gründen nicht möglich ist und die Verarbeitung der Daten durch gesetzliche Vorschriften gestattet ist."),
                                html.H5("2. Rechtsgrundlage für die Verarbeitung personenbezogener Daten"),
                                html.P("Soweit wir für Verarbeitungsvorgänge personenbezogener Daten eine Einwilligung der betroffenen Person einholen, dient Art. 6 Abs. 1 lit. a EU-Datenschutzgrundverordnung (DSGVO) als Rechtsgrundlage. Bei der Verarbeitung von personenbezogenen Daten, die zur Erfüllung eines Vertrages, dessen Vertragspartei die betroffene Person ist, erforderlich ist, dient Art. 6 Abs. 1 lit. b DSGVO als Rechtsgrundlage. Dies gilt auch für Verarbeitungsvorgänge, die zur Durchführung vorvertraglicher Maßnahmen erforderlich sind. Soweit eine Verarbeitung personenbezogener Daten zur Erfüllung einer rechtlichen Verpflichtung erforderlich ist, der unser Unternehmen unterliegt, dient Art. 6 Abs. 1 lit. c DSGVO als Rechtsgrundlage. Für den Fall, dass lebenswichtige Interessen der betroffenen Person oder einer anderen natürlichen Person eine Verarbeitung personenbezogener Daten erforderlich machen, dient Art. 6 Abs. 1 lit. d DSGVO als Rechtsgrundlage. Ist die Verarbeitung zur Wahrung eines berechtigten Interesses unseres Unternehmens oder eines Dritten erforderlich und überwiegen die Interessen, Grundrechte und Grundfreiheiten des Betroffenen das erstgenannte Interesse nicht, so dient Art. 6 Abs. 1 lit. f DSGVO als Rechtsgrundlage für die Verarbeitung."),
                                html.H5("3. Datenlöschung und Speicherdauer"),
                                html.P("Die personenbezogenen Daten der betroffenen Person werden gelöscht oder gesperrt, sobald der Zweck der Speicherung entfällt. Eine Speicherung kann darüber hinaus erfolgen, wenn dies durch den europäischen oder nationalen Gesetzgeber in unionsrechtlichen Verordnungen, Gesetzen oder sonstigen Vorschriften, denen der Verantwortliche unterliegt, vorgesehen wurde. Eine Sperrung oder Löschung der Daten erfolgt auch dann, wenn eine durch die genannten Normen vorgeschriebene Speicherfrist abläuft, es sei denn, dass eine Erforderlichkeit zur weiteren Speicherung der Daten für einen Vertragsabschluss oder eine Vertragserfüllung besteht.")
                            ]
                        ),
                        html.H4("IV. Bereitstellung der Website und Erstellung von Logfiles"),
                        html.Div(
                            children=[
                                html.H5(" 1. Beschreibung und Umfang der Datenverarbeitung"),
                                html.P("Bei jedem Aufruf unserer Internetseite erfasst unser System automatisiert Daten und Informationen vom Computersystem des aufrufenden Rechners. Folgende Daten werden hierbei erhoben:"),
                                html.Ol(id='my-list', children=[html.Li(i) for i in privacyDataProcessing]),
                                html.P("Die Daten werden ebenfalls in den Logfiles unseres Systems gespeichert. Eine Speicherung dieser Daten zusammen mit anderen personenbezogenen Daten findet nicht statt."),
                                html.H5(" 2. Rechtsgrundlage für die Datenverarbeitung "),
                                html.P("Rechtsgrundlage für die vorübergehende Speicherung der Daten und der Logfiles ist Art. 6 Abs. 1 lit. f DSGVO."),
                                html.H5(" 3. Zweck der Datenverarbeitung"),
                                html.P("Die vorübergehende Speicherung der IP-Adresse durch das System ist notwendig, um eine Auslieferung der Website an den Rechner der Nutzer*in zu ermöglichen. Hierfür muss die IP-Adresse der Nutzer*in für die Dauer der Sitzung gespeichert bleiben. <br>Die Speicherung in Logfiles erfolgt, um die Funktionsfähigkeit der Website sicherzustellen. Zudem dienen uns die Daten zur Optimierung der Website und zur Sicherstellung der Sicherheit unserer informationstechnischen Systeme. Eine Auswertung der Daten zu Marketingzwecken findet in diesem Zusammenhang nicht statt. <br>In diesen Zwecken liegt auch unser berechtigtes Interesse an der Datenverarbeitung nach Art. 6 Abs. 1 lit. f DSGVO. "),
                                html.H5(" 4. Dauer der Speicherung"),
                                html.P("Die Daten werden gelöscht, sobald sie für die Erreichung des Zweckes ihrer Erhebung nicht mehr erforderlich sind. Im Falle der Erfassung der Daten zur Bereitstellung der Website ist dies der Fall, wenn die jeweilige Sitzung beendet ist. <br>Im Falle der Speicherung der Daten in Logfiles ist dies nach spätestens sieben Tagen der Fall. Eine darüberhinausgehende Speicherung ist möglich. In diesem Fall werden die IP-Adressen gelöscht oder verfremdet, sodass eine Zuordnung des aufrufenden Clients nicht mehr möglich ist."),
                                html.H5(" 5. Widerspruchs- und Beseitigungsmöglichkeit"),
                                html.P("Die Erfassung der Daten zur Bereitstellung der Website und die Speicherung der Daten in Logfiles ist für den Betrieb der Internetseite zwingend erforderlich. Es besteht folglich seitens des Nutzer*ins keine Widerspruchsmöglichkeit.")
                            ]
                        ),
                        html.H4("V. Verwendung von Cookies"),
                        html.Div(
                            children=[
                                html.H5("a) Beschreibung und Umfang der Datenverarbeitung"),
                                html.P("Unsere Webseite verwendet Cookies. Bei Cookies handelt es sich um Textdateien, die im Internetbrowser bzw. vom Internetbrowser auf dem Computersystem der Nutzer*in gespeichert werden. Ruft eine Person eine Website auf, so kann ein Cookie auf dem Betriebssystem der Person gespeichert werden. Dieser Cookie enthält eine charakteristische Zeichenfolge, die eine eindeutige Identifizierung des Browsers beim erneuten Aufrufen der Website ermöglicht. Wir verwenden auf unserer Website darüber hinaus Cookies, die eine Analyse des Surfverhaltens der Nutzer*innen ermöglichen."),
                                html.P("Auf diese Weise können folgende Daten übermittelt werden:"),
                                html.Ol(id='my-list', children=[html.Li(i) for i in privacyCookies]),
                                html.P("Die auf diese Weise erhobenen Daten werden durch technische Vorkehrungen pseudonymisiert. Daher ist eine Zuordnung der Daten zur aufrufenden Person nicht mehr möglich. Die Daten werden nicht gemeinsam mit sonstigen personenbezogenen Daten gespeichert. Beim Aufruf unserer Website werden die Nutzer*innen durch einen Infobanner über die Verwendung von Cookies zu Analysezwecken informiert und auf diese Datenschutzerklärung verwiesen. Es erfolgt in diesem Zusammenhang auch ein Hinweis darauf, wie die Speicherung von Cookies in den Browsereinstellungen unterbunden werden kann."),
                                html.H5("b) Rechtsgrundlage für die Datenverarbeitung"),
                                html.P("Die Rechtsgrundlage für die Verarbeitung personenbezogener Daten unter Verwendung von Cookies ist Art. 6 Abs. 1 lit. f DSGVO."),
                                html.H5("c) Zweck der Datenverarbeitung"),
                                html.P("Die Verwendung der Analyse-Cookies erfolgt zu dem Zweck, die Qualität unserer Website und ihre Inhalte zu verbessern. Durch die Analyse-Cookies erfahren wir, wie die Website genutzt wird und können so unser Angebot stetig optimieren. Dies betrifft etwa Herkunftsländer der Nutzerinnen und Nutzer sowie die Häufigkeit von Publikations-Downloads."),
                                dbc.Table(cookies_table_header + cookies_table_body, bordered=True),
                                html.P("In diesen Zwecken liegt auch unser berechtigtes Interesse in der Verarbeitung der personenbezogenen Daten nach Art. 6 Abs. 1 lit. f DSGVO."),
                                html.H5("d) Dauer der Speicherung, Widerspruchs- und Beseitigungsmöglichkeit"),
                                html.P("Cookies werden auf dem Rechner der Nutzer*in gespeichert und von diesem an unserer Seite übermittelt. Daher haben Sie als Nutzer*in auch die volle Kontrolle über die Verwendung von Cookies. Durch eine Änderung der Einstellungen in Ihrem Internetbrowser können Sie die Übertragung von Cookies deaktivieren oder einschränken. Bereits gespeicherte Cookies können jederzeit gelöscht werden. Dies kann auch automatisiert erfolgen. Werden Cookies für unsere Website deaktiviert, können möglicherweise nicht mehr alle Funktionen der Website vollumfänglich genutzt werden.")
                            ]
                        ),
                        html.H4("VI. Geschäftskontakte"),
                        html.Div(
                            children=[
                                html.H5("1. Beschreibung und Umfang der Datenverarbeitung"),
                                html.P("Auf unserer Internetseite werden die E-Mail-Adressen aller Mitarbeitenden zur Möglichkeit der Kontaktaufnahme genannt. Nimmt ein*e Nutzer*in diese Möglichkeit wahr, so werden die mit der E-Mail übermittelten personenbezogenen Daten der Nutzer*in gespeichert. Es erfolgt in diesem Zusammenhang keine Weitergabe der Daten an Dritte. Die Daten werden ausschließlich für die Verarbeitung der Konversation verwendet."),
                                html.P("Auch Kontaktdaten, die persönlich, telefonisch oder auf anderem Wege zum Zweck der Führung von Geschäften oder zum Austausch von Informationen im Rahmen der Forschungsarbeit an das RLI übermittelt werden, können elektronisch gespeichert werden. Auch hier erfolgt keine Weitergabe an Dritte."),
                                html.H5("2. Rechtsgrundlage für die Datenverarbeitung"),
                                html.P("Rechtsgrundlage für die Verarbeitung der Daten ist bei Vorliegen einer Einwilligung der Nutzer*in Art. 6 Abs. 1 lit. a DSGVO. Rechtsgrundlage für die Verarbeitung der Daten, die im Zuge einer Übersendung einer E-Mail, telefonisch oder persönlich übermittelt werden, ist Art. 6 Abs. 1 lit. f DSGVO. Zielt die Kontaktaufnahme auf den Abschluss eines Vertrages ab, so ist zusätzliche Rechtsgrundlage für die Verarbeitung Art. 6 Abs. 1 lit. b DSGVO."),
                                html.H5("3. Zweck der Datenverarbeitung"),
                                html.P("Im Falle einer Kontaktaufnahme per E-Mail, telefonisch oder persönlich liegt hieran auch das erforderliche berechtigte Interesse an der Verarbeitung der Daten. Die Verarbeitung personenbezogener Daten dient der Auftragsanbahnung und -erfüllung sowie dem Aufbau und der Pflege von Geschäftsbeziehungen und somit der Durchführung unserer geschäftlichen oder akademischen Arbeit."),
                                html.H5("4. Dauer der Speicherung"),
                                html.P("Die Daten werden gelöscht, sobald sie für die Erreichung des Zweckes ihrer Erhebung nicht mehr erforderlich sind. Für die personenbezogenen Daten, die per E-Mail übersandt wurden, ist dies dann der Fall, wenn die jeweilige Konversation beendet ist. Beendet ist die Konversation dann, wenn sich aus den Umständen entnehmen lässt, dass der betroffene Sachverhalt abschließend geklärt ist."),
                                html.H5("5. Widerspruchs- und Beseitigungsmöglichkeit"),
                                html.P("Die Nutzer*innen haben jederzeit die Möglichkeit, ihre Einwilligung zur Verarbeitung der personenbezogenen Daten zu widerrufen. Nimmt ein*e Nutzer*in per E-Mail Kontakt mit uns auf, so kann er/sie der Speicherung von personenbezogenen Daten jederzeit widersprechen. In einem solchen Fall kann die Konversation nicht fortgeführt werden. Gleiches gilt für die Übermittlung persönlicher Daten auf telefonischem, persönlichem oder anderem Wege. Der Widerruf der Einwilligung kann formlos per E-Mail oder schriftlich erfolgen. Alle personenbezogenen Daten, die im Zuge der Kontaktaufnahme gespeichert wurden, werden in diesem Fall gelöscht.")
                            ]
                        ),
                        html.H4("VII. Webanalyse durch Matomo (ehemals PIWIK)"),
                        html.Div(
                            children=[
                                html.H5("1. Umfang der Verarbeitung personenbezogener Daten"),
                                html.P("Wir nutzen auf unserer Website das Open-Source-Software-Tool Matomo (ehemals PIWIK) zur Analyse des Surfverhaltens unserer Nutzer*innen. Die Software setzt ein Cookie auf dem aufrufenden Rechner (zu Cookies siehe bereits oben). Werden Einzelseiten unserer Website aufgerufen, so werden folgende Daten gespeichert:"),
                                html.Ol(id='my-list', children=[html.Li(i) for i in privacyWebAnalysis]),
                                html.P("Die Software läuft dabei ausschließlich auf den Servern unserer Webseite. Eine Speicherung der personenbezogenen Daten findet nur dort statt. Eine Weitergabe der Daten an Dritte erfolgt nicht. Die Software ist so eingestellt, dass die IP-Adressen nicht vollständig gespeichert werden, sondern 2 Bytes der IP-Adresse maskiert werden (Bsp.: 192.168.xxx.xxx). Auf diese Weise ist eine Zuordnung der gekürzten IP-Adresse zum aufrufenden Rechner nicht mehr möglich."),
                                html.H5("2. Rechtsgrundlage für die Verarbeitung personenbezogener Daten"),
                                html.P("Rechtsgrundlage für die Verarbeitung der personenbezogenen Daten der Nutzer*in ist Art. 6 Abs. 1 lit. f DSGVO."),
                                html.H5("3. Zweck der Datenverarbeitung"),
                                html.P("Die Verarbeitung der personenbezogenen Daten ermöglicht uns eine Analyse des Surfverhaltens unserer Nutzer*innen. Wir sind in durch die Auswertung der gewonnen Daten in der Lage, Informationen über die Nutzung der einzelnen Komponenten unserer Webseite zusammenzustellen. Dies hilft uns dabei unsere Webseite und deren Benutzungsfreundlichkeit stetig zu verbessern. In diesen Zwecken liegt auch unser berechtigtes Interesse in der Verarbeitung der Daten nach Art. 6 Abs. 1 lit. f DSGVO. Durch die Anonymisierung der IP-Adresse wird dem Interesse der Nutzer*innen an deren Schutz personenbezogener Daten hinreichend Rechnung getragen."),
                                html.H5("4. Dauer der Speicherung"),
                                html.P("Die Daten werden gelöscht, sobald sie für unsere Aufzeichnungszwecke nicht mehr benötigt werden. In unserem Fall ist dies nach 180 Tagen der Fall."),
                                html.H5("5. Widerspruchs- und Beseitigungsmöglichkeit"),
                                html.P("Cookies werden auf dem aufrufenden Rechner gespeichert und von diesem an unserer Seite übermittelt. Daher haben Sie als Nutzer*in auch die volle Kontrolle über die Verwendung von Cookies. Durch eine Änderung der Einstellungen in Ihrem Internetbrowser können Sie die Übertragung von Cookies deaktivieren oder einschränken. Bereits gespeicherte Cookies können jederzeit gelöscht werden. Dies kann auch automatisiert erfolgen. Werden Cookies für unsere Website deaktiviert, können möglicherweise nicht mehr alle Funktionen der Website vollumfänglich genutzt werden."),
                                html.P("Nähere Informationen zu den Privatsphäreeinstellungen der Matomo Software finden Sie unter folgendem Link: https://matomo.org/docs/privacy/")
                            ]
                        ),
                        html.H4("VIII. Rechte der betroffenen Person"),
                        html.Div(
                            children=[
                                html.H5("1. Auskunftsrecht"),
                                html.P("Sie können von dem Verantwortlichen eine Bestätigung darüber verlangen, ob personenbezogene Daten, die Sie betreffen, von uns verarbeitet werden. Liegt eine solche Verarbeitung vor, können Sie von dem Verantwortlichen über folgende Informationen Auskunft verlangen:"),
                                html.Ol(id='my-list', children=[html.Li(i) for i in privacyRights]),
                                html.P("Ihnen steht das Recht zu, Auskunft darüber zu verlangen, ob die Sie betreffenden personenbezogenen Daten in ein Drittland oder an eine internationale Organisation übermittelt werden. In diesem Zusammenhang können Sie verlangen, über die geeigneten Garantien gem. Art. 46 DSGVO im Zusammenhang mit der Übermittlung unterrichtet zu werden. Dieses Auskunftsrecht kann insoweit beschränkt werden, als es voraussichtlich die Verwirklichung von Forschungszwecken unmöglich macht oder ernsthaft beeinträchtigt und die Beschränkung für die Erfüllung der Forschungswecke notwendig ist."),
                                html.H5("2. Recht auf Berichtigung"),
                                html.P("Sie haben ein Recht auf Berichtigung und/oder Vervollständigung gegenüber der verantwortlichen Person, sofern die verarbeiteten personenbezogenen Daten, die Sie betreffen, unrichtig oder unvollständig sind. Der/die Verantwortliche hat die Berichtigung unverzüglich vorzunehmen. Ihr Recht auf Berichtigung kann insoweit beschränkt werden, als es voraussichtlich die Verwirklichung von Forschungszwecken unmöglich macht oder ernsthaft beeinträchtigt und die Beschränkung für die Erfüllung der Forschungszwecke notwendig ist."),
                                html.H5("3. Recht auf Einschränkung der Verarbeitung"),
                                html.P("Unter den folgenden Voraussetzungen können Sie die Einschränkung der Verarbeitung der Sie betreffenden personenbezogenen Daten verlangen:"),
                                html.Ol(id='my-list', children=[html.Li(i) for i in privacyDataProcessingRights]),
                                html.P("Wurde die Verarbeitung der Sie betreffenden personenbezogenen Daten eingeschränkt, dürfen diese Daten – von ihrer Speicherung abgesehen – nur mit Ihrer Einwilligung oder zur Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen oder zum Schutz der Rechte einer anderen natürlichen oder juristischen Person oder aus Gründen eines wichtigen öffentlichen Interesses der Union oder eines Mitgliedstaats verarbeitet werden."),
                                html.P("Wurde die Einschränkung der Verarbeitung nach den o.g. Voraussetzungen eingeschränkt, werden Sie von der verantwortlichen Person unterrichtet bevor die Einschränkung aufgehoben wird. Ihr Recht auf Einschränkung der Verarbeitung kann insoweit beschränkt werden, als es voraussichtlich die Verwirklichung von Forschungszwecken unmöglich macht oder ernsthaft beeinträchtigt und die Beschränkung für die Erfüllung der Forschungszwecke notwendig ist."),
                                html.H5("4. Recht auf Löschung"),
                                html.H6("a) Löschungspflicht"),
                                html.P("Sie können von der verantwortlichen Person verlangen, dass die Sie betreffenden personenbezogenen Daten unverzüglich gelöscht werden, und die Verantwortlichen sind verpflichtet, diese Daten unverzüglich zu löschen, sofern einer der folgenden Gründe zutrifft:"),
                                html.Ol(id='my-list', children=[html.Li(i) for i in privacyDataDeletion]),
                                html.H6("b) Information an Dritte"),
                                html.P("Hat die verantwortliche Person die Sie betreffenden personenbezogenen Daten öffentlich gemacht und ist sie gem. Art. 17 Abs. 1 DSGVO zu deren Löschung verpflichtet, so trifft sie unter Berücksichtigung der verfügbaren Technologie und der Implementierungskosten angemessene Maßnahmen, auch technischer Art, um für die Datenverarbeitung Verantwortliche, die die personenbezogenen Daten verarbeiten, darüber zu informieren, dass Sie als betroffene Person von ihnen die Löschung aller Links zu diesen personenbezogenen Daten oder von Kopien oder Replikationen dieser personenbezogenen Daten verlangt haben."),
                                html.H6("c) Ausnahmen"),
                                html.P("Das Recht auf Löschung besteht nicht, soweit die Verarbeitung erforderlich ist"),
                                html.Ul(id='my-list', children=[html.Li(i) for i in privacyDataDeletionExceptions]),
                                html.H5("5. Recht auf Unterrichtung"),
                                html.P("Haben Sie das Recht auf Berichtigung, Löschung oder Einschränkung der Verarbeitung gegenüber den verantwortlichen Personen geltend gemacht, sind diese verpflichtet, allen Empfängern, denen die Sie betreffenden personenbezogenen Daten offengelegt wurden, diese Berichtigung oder Löschung der Daten oder Einschränkung der Verarbeitung mitzuteilen, es sei denn, dies erweist sich als unmöglich oder ist mit einem unverhältnismäßigen Aufwand verbunden. Ihnen steht gegenüber den Verantwortlichen das Recht zu, über diese Empfänger unterrichtet zu werden."),
                                html.H5("6. Recht auf Datenübertragbarkeit"),
                                html.P("Sie haben das Recht, die Sie betreffenden personenbezogenen Daten, die Sie bereitgestellt haben, in einem strukturierten, gängigen und maschinenlesbaren Format zu erhalten. Außerdem haben Sie das Recht diese Daten einer anderen verantwortlichen Person ohne Behinderung durch die verantwortliche Person, der die personenbezogenen Daten bereitgestellt wurden, zu übermitteln, sofern"),
                                html.Ol(id='my-list', children=[html.Li(i) for i in privacyDataTransfer]),
                                html.P("In Ausübung dieses Rechts haben Sie ferner das Recht, zu erwirken, dass die Sie betreffenden personenbezogenen Daten direkt von einer verantwortlichen Person einer anderen verantwortlichen Person übermittelt werden, soweit dies technisch machbar ist. Freiheiten und Rechte anderer Personen dürfen hierdurch nicht beeinträchtigt werden. Das Recht auf Datenübertragbarkeit gilt nicht für eine Verarbeitung personenbezogener Daten, die für die Wahrnehmung einer Aufgabe erforderlich ist, die im öffentlichen Interesse liegt oder in Ausübung öffentlicher Gewalt erfolgt, die dem Verantwortlichen übertragen wurde."),
                                html.H5("7. Widerspruchsrecht"),
                                html.P("Sie haben das Recht, aus Gründen, die sich aus ihrer besonderen Situation ergeben, jederzeit gegen die Verarbeitung der Sie betreffenden personenbezogenen Daten, die aufgrund von Art. 6 Abs. 1 lit. e oder f DSGVO erfolgt, Widerspruch einzulegen; dies gilt auch für ein auf diese Bestimmungen gestütztes Profiling. Die verantwortliche Person verarbeitet die Sie betreffenden personenbezogenen Daten nicht mehr, es sei denn, sie kann zwingende schutzwürdige Gründe für die Verarbeitung nachweisen, die Ihre Interessen, Rechte und Freiheiten überwiegen, oder die Verarbeitung dient der Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen."),
                                html.P("Werden die Sie betreffenden personenbezogenen Daten verarbeitet, um Direktwerbung zu betreiben, haben Sie das Recht, jederzeit Widerspruch gegen die Verarbeitung der Sie betreffenden personenbezogenen Daten zum Zwecke derartiger Werbung einzulegen; dies gilt auch für das Profiling, soweit es mit solcher Direktwerbung in Verbindung steht. Widersprechen Sie der Verarbeitung für Zwecke der Direktwerbung, so werden die Sie betreffenden personenbezogenen Daten nicht mehr für diese Zwecke verarbeitet. Sie haben die Möglichkeit, im Zusammenhang mit der Nutzung von Diensten der Informationsgesellschaft – ungeachtet der Richtlinie 2002/58/EG – Ihr Widerspruchsrecht mittels automatisierter Verfahren auszuüben, bei denen technische Spezifikationen verwendet werden."),
                                html.P("Sie haben auch das Recht, aus Gründen, die sich aus Ihrer besonderen Situation ergeben, bei der Verarbeitung Sie betreffender personenbezogener Daten, die zu wissenschaftlichen oder historischen Forschungszwecken oder zu statistischen Zwecken gem. Art. 89 Abs. 1 DSGVO erfolgt, dieser zu widersprechen. Ihr Widerspruchsrecht kann insoweit beschränkt werden, als es voraussichtlich die Verwirklichung der Forschungs- oder Statistikzwecke unmöglich macht oder ernsthaft beeinträchtigt und die Beschränkung für die Erfüllung der Forschungs- oder Statistikzwecke notwendig ist."),
                                html.H5("8. Recht auf Widerruf der datenschutzrechtlichen Einwilligungserklärung"),
                                html.P("Sie haben das Recht, Ihre datenschutzrechtliche Einwilligungserklärung jederzeit zu widerrufen. Durch den Widerruf der Einwilligung wird die Rechtmäßigkeit der aufgrund der Einwilligung bis zum Widerruf erfolgten Verarbeitung nicht berührt."),
                                html.H5("9. Automatisierte Entscheidung im Einzelfall einschließlich Profiling"),
                                html.P("Sie haben das Recht, nicht einer ausschließlich auf einer automatisierten Verarbeitung – einschließlich Profiling – beruhenden Entscheidung unterworfen zu werden, die Ihnen gegenüber rechtliche Wirkung entfaltet oder Sie in ähnlicher Weise erheblich beeinträchtigt. Dies gilt nicht, wenn die Entscheidung"),
                                html.Ol(id='my-list', children=[html.Li(i) for i in privacyProfiling]),
                                html.P("Allerdings dürfen diese Entscheidungen nicht auf besonderen Kategorien personenbezogener Daten nach Art. 9 Abs. 1 DSGVO beruhen, sofern nicht Art. 9 Abs. 2 lit. a oder g DSGVO gilt und angemessene Maßnahmen zum Schutz der Rechte und Freiheiten sowie Ihrer berechtigten Interessen getroffen wurden. Hinsichtlich der in (1) und (3) genannten Fälle trifft die verantwortliche Person angemessene Maßnahmen, um die Rechte und Freiheiten sowie Ihre berechtigten Interessen zu wahren, wozu mindestens das Recht auf Erwirkung des Eingreifens einer Person seitens der Verantwortlichen, auf Darlegung des eigenen Standpunkts und auf Anfechtung der Entscheidung gehört."),
                                html.H5("10. Recht auf Beschwerde bei einer Aufsichtsbehörde"),
                                html.P("Unbeschadet eines anderweitigen verwaltungsrechtlichen oder gerichtlichen Rechtsbehelfs steht Ihnen das Recht auf Beschwerde bei einer Aufsichtsbehörde, insbesondere in dem Mitgliedstaat ihres Aufenthaltsorts, ihres Arbeitsplatzes oder des Orts des mutmaßlichen Verstoßes, zu, wenn Sie der Ansicht sind, dass die Verarbeitung der Sie betreffenden personenbezogenen Daten gegen die DSGVO verstößt. Die Aufsichtsbehörde, bei der die Beschwerde eingereicht wurde, unterrichtet die beschwerdeführende Person über den Stand und die Ergebnisse der Beschwerde einschließlich der Möglichkeit eines gerichtlichen Rechtsbehelfs nach Art. 78 DSGVO."),
                                html.H5("Gültigkeit der Datenschutzerklärung"),
                                html.P("Wir behalten uns vor, diese Datenschutzerklärung von Zeit zu Zeit zu verändern oder anzupassen. Diese Erklärung wurde zuletzt geändert am 11.08.2020")
                            ]
                        )
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
                className="scenarios__btn btn btn--refresh"
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
                id={"name": option, "type": f"graph_{data_type}_option"},
                options=options,
                value=value,
                clearable=GRAPHS_DEFAULT_OPTIONS[data_type][graph_type][option].clearable
            )
        elif component_type in ("input", "number"):
            component = dcc.Input(
                id={"name": option, "type": f"graph_{data_type}_option"},
                value=value,
                type="text" if component_type == "input" else "number"
            )
        elif component_type == "bool":
            component = dcc.Checklist(
                id={"name": option, "type": f"graph_{data_type}_option"},
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
                        id={"name": unit_name, "type": "unit-dropdown"},
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
                        id={"name": filter_, "type": "filter-dropdown"}, multi=True, clearable=True
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
                                    html.Button(f"Refresh", id=f"refresh_{graph}", className="btn btn--refresh")
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
