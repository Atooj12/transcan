from transcan import ocr, traducao, reinsercao

def processar_lote(scan, obra, capitulo):
    ocr.run(scan, obra, capitulo)
    traducao.run(scan, obra, capitulo)
    reinsercao.run(scan, obra, capitulo)

# Depois cria o loop por pasta/capítulo
