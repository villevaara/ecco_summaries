import csv
# import plotly
# from plotly.graph_objs import Bar, Layout
from lib.octavo_api_client import OctavoEccoClient
from lib.text_reuse_common import (
    load_good_metadata,
    get_year_from_estc,
    )


ecco_api_client = OctavoEccoClient()
fields = ["ESTCID", "documentID", "documentLength", "contentTokens",
          "totalParagraphs", "totalPages"]
pampflet_totals = ecco_api_client.get_documents_by_length(
    length=10407, fields=fields, operator="<")
other_totals = ecco_api_client.get_documents_by_length(
    length=10407, fields=fields, operator=">=")
good_metadata_jsonfile = "data/estc_metadata.json"
good_metadata = load_good_metadata(good_metadata_jsonfile)

years_p = []
years_o = []
for pampflet in pampflet_totals:
    pampflet['year'] = get_year_from_estc(pampflet.get('documentID'),
                                          good_metadata)
    years_p.append(pampflet.get('year'))

for other in other_totals:
    other['year'] = get_year_from_estc(other.get('documentID'), good_metadata)
    years_o.append(other.get('year'))


def get_variable_sum_for_year(year, dataset, variable_name):
    total = 0
    for entry in dataset:
        if entry['year'] == year:
            total += entry.get(variable_name)
    return total


years_x = list(range(1700, 1800))
total_pamph_y = []
total_pamph_pages = []
total_pamph_paras = []
total_pamph_token = []
total_pamph_chars = []
total_other_y = []
total_other_pages = []
total_other_paras = []
total_other_token = []
total_other_chars = []

for year in years_x:
    total_pamph_y.append(years_p.count(year))
    total_pamph_pages.append(
        get_variable_sum_for_year(year, pampflet_totals, 'totalPages'))
    total_pamph_paras.append(
        get_variable_sum_for_year(year, pampflet_totals, 'totalParagraphs'))
    total_pamph_token.append(
        get_variable_sum_for_year(year, pampflet_totals, 'contentTokens'))
    total_pamph_chars.append(
        get_variable_sum_for_year(year, pampflet_totals, 'documentLength'))
    total_other_y.append(years_o.count(year))
    total_other_pages.append(
        get_variable_sum_for_year(year, other_totals, 'totalPages'))
    total_other_paras.append(
        get_variable_sum_for_year(year, other_totals, 'totalParagraphs'))
    total_other_token.append(
        get_variable_sum_for_year(year, other_totals, 'contentTokens'))
    total_other_chars.append(
        get_variable_sum_for_year(year, other_totals, 'documentLength'))

csv_file = "./totals_by_year.csv"
with open(csv_file, 'w') as outfile:
    csvwriter = csv.writer(outfile)
    csvwriter.writerow(["year",
                        "pamphlet_titles",
                        "pamphlet_pages",
                        "pamphlet_paragraphs",
                        "pamphlet_tokens",
                        "pamphlet_characters",
                        "other_titles",
                        "other_pages",
                        "other_paragraphs",
                        "other_tokens",
                        "other_characters"])
    for i in range(0, len(years_x)):
        csvwriter.writerow([years_x[i],
                           total_pamph_y[i],
                           total_pamph_pages[i],
                           total_pamph_paras[i],
                           total_pamph_token[i],
                           total_pamph_chars[i],
                           total_other_y[i],
                           total_other_pages[i],
                           total_other_paras[i],
                           total_other_token[i],
                           total_other_chars[i]])

dec_indices = list(range(0, 101, 10))

decs = ["1700-1709",
        "1710-1719",
        "1720-1729",
        "1730-1739",
        "1740-1749",
        "1750-1759",
        "1760-1769",
        "1770-1779",
        "1780-1789",
        "1790-1799"]
total_dec_pamph_y = []
total_dec_pamph_pages = []
total_dec_pamph_paras = []
total_dec_pamph_token = []
total_dec_pamph_chars = []
total_dec_other_y = []
total_dec_other_pages = []
total_dec_other_paras = []
total_dec_other_token = []
total_dec_other_chars = []

for i in range(0, len(dec_indices) - 1):
    total_dec_pamph_y.append(
        sum(total_pamph_y[dec_indices[i]:dec_indices[i+1]]))
    total_dec_pamph_pages.append(
        sum(total_pamph_pages[dec_indices[i]:dec_indices[i+1]]))
    total_dec_pamph_paras.append(
        sum(total_pamph_paras[dec_indices[i]:dec_indices[i+1]]))
    total_dec_pamph_token.append(
        sum(total_pamph_token[dec_indices[i]:dec_indices[i+1]]))
    total_dec_pamph_chars.append(
        sum(total_pamph_chars[dec_indices[i]:dec_indices[i+1]]))
    total_dec_other_y.append(
        sum(total_other_y[dec_indices[i]:dec_indices[i+1]]))
    total_dec_other_pages.append(
        sum(total_other_pages[dec_indices[i]:dec_indices[i+1]]))
    total_dec_other_paras.append(
        sum(total_other_paras[dec_indices[i]:dec_indices[i+1]]))
    total_dec_other_token.append(
        sum(total_other_token[dec_indices[i]:dec_indices[i+1]]))
    total_dec_other_chars.append(
        sum(total_other_chars[dec_indices[i]:dec_indices[i+1]]))

csv_file = "./totals_by_decade.csv"
with open(csv_file, 'w') as outfile:
    csvwriter = csv.writer(outfile)
    csvwriter.writerow(["decade",
                        "pamphlet_titles",
                        "pamphlet_pages",
                        "pamphlet_paragraphs",
                        "pamphlet_tokens",
                        "pamphlet_characters",
                        "other_titles",
                        "other_pages",
                        "other_paragraphs",
                        "other_tokens",
                        "other_characters"])
    for i in range(0, len(decs)):
        csvwriter.writerow([decs[i],
                           total_dec_pamph_y[i],
                           total_dec_pamph_pages[i],
                           total_dec_pamph_paras[i],
                           total_dec_pamph_token[i],
                           total_dec_pamph_chars[i],
                           total_dec_other_y[i],
                           total_dec_other_pages[i],
                           total_dec_other_paras[i],
                           total_dec_other_token[i],
                           total_dec_other_chars[i]])
