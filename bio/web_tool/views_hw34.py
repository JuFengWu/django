from django.shortcuts import render
from web_tool.request_data import *
from web_tool.hw_34_transcript import get_exon_and_other,convert_to_dict_list,get_filtered_data,expand_position_value

def transcript(request, gene_sequence_name):

    print(gene_sequence_name)
    bedgraph = './web_tool/data/SRR20334757_m0_bedgraph.csv'
    result = get_filtered_data(bedgraph,gene_sequence_name)
    barData = expand_position_value(result)

    file_path = './web_tool/data/spliced_codingtranscript_293.csv'
    exon_list, other_list = get_exon_and_other(gene_sequence_name,file_path)
    new_exon_list=convert_to_dict_list(exon_list)

    barHorizontal = [
        {"type": "UTR", "start": 0, "end": 300, "color": "gray"},
        {"type": "CDS", "start": 300, "end": 1000, "color": "green"},
        {"type": "EXON", "start": 100, "end": 400, "color": "orange"},
        {"type": "EXON", "start": 500, "end": 800, "color": "yellow"}
    ]
    context = {'barData': barData, 'barHorizontal':new_exon_list ,
               "gene_sequence_name" : gene_sequence_name}
    
    return render(request, 'transcript.html', context)


