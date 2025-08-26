from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import os
import itertools
from itertools import product, combinations
import re
from waitress import serve
from functools import wraps

app = Flask(__name__)
# A chave secreta será lida de uma Váriavel de Ambiente no Render
app.secret_key = os.environ.get('SECRET_KEY', 'uma-chave-padrao-para-testes-locais')
# A senha de acesso será lida de uma variável de ambiente também
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'senha123')


# --- Decorator de Login ---
# Esta função verifica se o usuário está logado antes de acessar uma página
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Rota de Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index')) # Redireciona para a página principal após login
        else:
            error = 'Senha inválida. Tente novamente.'
    return render_template('login.html', error=error)

# --- Rota de Logout ---
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))





'''
enzymes = {
    'AatII': ['GACGTC', 1, 5, 'p'],
    'Acc65I': ['GGTACC', 1, 5, 'p'],
    'AccI': ['GTMKAC', 1, 5, 'p'],
    'AciI': ['CCGC', -3, -1, 'np'],
    'AclI': ['AACGTT', 1, 5, 'p'],
    'AcuI': ['CTGAAG', 16, 14, 'np'],
    'AfeI': ['AGCGCT', 1, 5, 'p'],
    'AflII': ['CTTTAAG', 1, 6, 'np'],
    'AflIII': ['ACRYGT', 1, 6, 'p'],
    'AgeI-HF®': ['ACCGGT', 1, 5, 'p'],
    #'AhdI': ['GACNNNNNGTC', 1, 10, 'p'],
    #'AleI-v2': ['CACNNNNGTG', 1, 9, 'p'],
    'AluI': ['AGCT', 1, 3, 'p'],
    'AlwI': ['GGATC', 4, 5, 'np'], 
    #'AlwNI': ['CAGNNNCTG', 1, 8, 'p'],
    'ApaI': ['GGGCCC', 1, 5, 'p'],
    'ApaLI': ['GTGCAC', 1, 5, 'p'],
    'ApeKI': ['GCWGC', 1, 4, 'p'],
    'ApoI-HF': ['RAATTY', 1, 5, 'p'],
    'AscI': ['GGCGCGCC', 1, 7, 'p'],
    'AseI': ['ATTAAT', 1, 5, 'p'],
    'AsiSI': ['GCGATCGC', 1, 7, 'p'],
    'AvaII': ['GGWCC', 1, 4, 'p'],
    'AvrII': ['CCTAGG', 1, 5, 'p'],
    'BaeGI': ['GKGCMC', 1, 5, 'p'],
    #'BaeI': ['ACNNNNGTAYC', 12, 7, 'np'],
    'BamHI': ['GGATCC', 1, 5, 'p'],
    'BanI': ['GGYRCC', 1, 5, 'p'],
    'BbsI': ['GAAGAC', 2, 6, 'np'],
    'BbvCI': ['CCTCAGC', -5, -2, 'np'],
    'BbvI': ['GCAGC', 8, 12, 'np'],
    'BccI': ['CCATC', 4, 5, 'np'],
    'BceAI': ['ACGGC', 12, 14, 'np'],
    #'BcgI': ['CGANNNNNNTGC', 12, 10, 'np'],
    'BciVI': ['GTATCC', 6, 5, 'np'],
    'BclI': ['TGATCA', 1, 5, 'p'],
    'BfaI': ['CTAG', 1, 3, 'p'],
    'BfuAI': ['ACCTGC', 4, 8, 'np'],
    #'BglI': ['GCCNNNNNGGC', 1, 10, 'p'],
    'BglII': ['AGATCT', 1, 5, 'p'],
    'BlpI': ['GCTNAGC', 1, 6, 'p'],
    'BmgBI': ['CACGTC', -3, -3, 'np'],
    'BmrI': ['ACTGGG', 5, 4, 'np'],
    'BpmI': ['CTGGAG', 16, 14, 'np'],
    'Bpu10I': ['CCTNAGC', -5, -2, 'np'],
    'BpuEI': ['CTTGAG', 16, 14, 'np'],
    'BsaAI': ['YACGTR', 1, 5, 'p'],
    #'BsaBI': ['GATNNNNATC', 1, 9, 'p'],
    'BsaHI': ['GRCGYC', 1, 5, 'p'],
    'BsaI-HF®v2': ['GGTCTC', 1, 5, 'np'],
    'BsaJI': ['CCNNGG', 1, 5, 'p'],
    'BsaWI': ['WCCGGW', 1, 5, 'p'],
    #'BsaXI': ['ACNNNNNCTCC', 10, 7, 'np'],
    'BseRI': ['GAGGAG', 10, 8, 'np'],
    'BseYI': ['CCCAGC', -5, -1, 'np'],
    'BsgI': ['GTGCAG', 16, 14, 'np'],
    'BsiEI': ['CGRYCG', 1, 5, 'p'],
    'BsiHKAI': ['GWGCWC', 1, 5, 'p'],
    'BsiWI': ['CGTACG', 1, 5, 'p'],
    #'BslI': ['CCNNNNNNNGG', 1, 10, 'p'],
    'BsmAI': ['GTCTC', 1, 5, 'np'],
    'BsmBI-v2': ['CGTCTC', 1, 5, 'np'],
    'BsmFI': ['GGGAC', 10, 14, 'np'],
    'BsmI': ['GAATGC', 1, -1, 'np'],
    'BsoBI': ['CYCGRG', 1, 5, 'p'],
    'Bsp1286I': ['GDGCHC', 1, 5, 'p'],
    'BspCNI': ['CTCAG', 9, 7, 'np'],
    'BspDI': ['ATCGAT', 1, 5, 'p'],
    'BspEI': ['TCCGGA', 1, 5, 'p'],
    'BspHI': ['TCATGA', 1, 5, 'p'],
    'BspMI': ['ACCTGC', 4, 8, 'np'],
    'BspQI': ['GCTCTTC', 1, 4, 'np'],
    'BsrBI': ['CCGCTC', -3, -3, 'np'],
    'BsrDI': ['GCAATG', 2, 0, 'np'],
    'BsrFI-v2': ['RCCGGY', 1, 5, 'p'],
    'BsrGI-HF®': ['TGTACA', 1, 5, 'p'],
    'BsrI': ['ACTGG', 1, -1, 'np'],
    'BssHII': ['GCGCGC', 1, 5, 'p'],
    'BssSI-v2': ['CACGAG', -5, -1, 'np'],
    #'BstAPI': ['GCANNNNNTGC', 1, 10, 'p'],
    'BstBI': ['TTCGAA', 1, 5, 'p'],
    'BstEII-HF®': ['GGTNACC', 1, 6, 'p'],
    'BstNI': ['CCWGG', 1, 4, 'p'],
    'BstUI': ['CGCG', 1, 3, 'p'],
    #'BstXI': ['CCANNNNNTGG', 1, 10, 'p'],
    'BstYI': ['RGATCY', 1, 5, 'p'],
    'BstZ17I-HF®': ['GTATAC', 1, 5, 'p'],
    'Bsu36I': ['CCTNAGG', 1, 7, 'p'],
    'BtgI': ['CCRYGG', 1, 5, 'p'],
    'BtgZI': ['GCGATG', 10, 14, 'np'],
    'BtsCI': ['GGATG', 2, 0, 'np'],
    'BtsI-v2': ['GCAGTG', 2, 0, 'np'],
    'BtsIMutI': ['CAGTG', 2, 0, 'np'],
    #'Cac8I': ['GCNNGC', 1, 5, 'p'],
    'ClaI': ['ATCGAT', 1, 5, 'p'],
    #'CspCI': ['CAANNNNNGTGG', 12, 10, 'np'],
    'CviKI-1': ['RGCY', 1, 3, 'p'],
    'CviQI': ['GTAC', 1, 3, 'p'],
    'DdeI': ['CTNAG', 1, 4, 'p'],
    'DraI': ['TTTAAA', 1, 5, 'p'],
    #'DraIII-HF®': ['CACNNNGTG', 1, 8, 'p'],
    #'DrdI': ['GACNNNNNNGTC', 1, 11, 'p'],
    'EaeI': ['YGGCCR', 1, 5, 'p'],
    'EagI-HF®': ['CGGCCG', 1, 5, 'p'],
    'EarI': ['CTCTTC', 1, 4, 'np'],
    'EciI': ['GGCGGA', 11, 9, 'np'],
    'Eco53kI': ['GAGCTC', 1, 5, 'p'],
    #'EcoNI': ['CCTNNNNNAGG', 1, 10, 'p'],
    'EcoO109I': ['RGGNCCY', 1, 6, 'p'],
    'EcoP15I': ['CAGCAG', 25, 27, 'np'],
    'EcoRI': ['GAATTC', 1, 5, 'p'],
    'EcoRV': ['GATATC', 1, 5, 'p'],
    'Esp3I': ['CGTCTC', 1, 5, 'np'],
    'FauI': ['CCCGC', 4, 6, 'np'],
    'FatI': ['CATG', 1, 3, 'p'],
    'Fnu4HI': ['GCNGC', 1, 4, 'p'],
    'FokI': ['GGATG', 14, -13, 'np'],
    'FseI': ['GGCCGGCC', 1, 7, 'p'],
    'FspI': ['TGCGCA', 1, 5, 'p'],
    'HaeII': ['RGCGCY', 1, 5, 'p'],
    'HaeIII': ['GGCC', 1, 3, 'p'],
    'HgaI': ['GACGC', 5, 10, 'np'],
    'HhaI': ['GCGC', 1, 3, 'p'],
    'HincII': ['GTYRAC', 1, 5, 'p'],
    'HindIII': ['AAGCTT', 1, 5, 'p'],
    'HinfI': ['GANTC', 1, 4, 'p'],
    'HinP1I': ['GCGC', 1, 3, 'p'],
    'HpaI': ['GTTAAC', 1, 5, 'p'],
    'HphI': ['GGTGA', 8, 7, 'np'],
    #'Hpy166II': ['GTNNAC', 1, 5, 'p'],
    'Hpy188I': ['TCNGA', 1, 4, 'p'],
    #'Hpy188III': ['TCNNGA', 1, 5, 'p'],
    'Hpy99I': ['CGWCG', 1, 4, 'p'],
    'HpyAV': ['CCTTC', 6, 5, 'np'],
    'HpyCH4III': ['ACNGT', 1, 4, 'p'],
    'HpyCH4IV': ['ACGT', 1, 3, 'p'],
    'HpyCH4V': ['TGCAC', 1, 4, 'np'],
    'I-CeuI': ['TAACTATAACGGTCCTAAGGTAGCGAA', -9, -13, 'np'],
    'I-SceI': ['TAGGGATAACAGGGTAAT', -9, -13, 'np'],
    'KasI': ['GGCGCC', 1, 5, 'p'],
    'KpnI-HF®': ['GGTACC', 1, 5, 'p'],
    'MboI': ['GATC', 1, 3, 'p'],
    'MboII': ['GAAGA', 8, 7, 'np'],
    'MfeI-HF®': ['CAATTG', 1, 5, 'p'],
    'MluCI': ['AATT', 1, 3, 'p'],
    'MluI-HF®': ['ACGCGT', 1, 5, 'p'],
    'MmeI': ['TCCRAC', 20, 18, 'np'],
    'MscI': ['TGGCCA', 1, 5, 'p'],
    'MseI': ['TTAA', 1, 3, 'p'],
    #'MslI': ['CAYNNNNRTG', 1, 9, 'p'],
    'MspA1I': ['CMGCKG', 1, 5, 'p'],
    'MspI': ['CCGG', 1, 3, 'p'],
    #'MspJI': ['CNNR', 9, 13, 'np'],
    #'MwoI': ['GCNNNNNNNGC', 1, 10, 'p'],
    'NaeI': ['GCCGGC', 1, 5, 'p'],
    'NarI': ['GGCGCC', 1, 5, 'p'],
    'NciI': ['CCSGG', 1, 4, 'p'],
    'NcoI': ['CCATGG', 1, 5, 'p'],
    'NdeI': ['CATATG', 1, 5, 'p'],
    'NheI-HF®': ['GCTAGC', 1, 5, 'p'],
    'NlaIII': ['CATG', 1, 3, 'p'],
    #'NlaIV': ['GGNNCC', 1, 5, 'p'],
    'NotI': ['GCGGCCGC', 1, 7, 'p'],
    'NruI-HF®': ['TCGCGA', 1, 5, 'p'],
    'NsiI': ['ATGCAT', 1, 5, 'p'],
    'NspI': ['RCATGY', 1, 5, 'p'],
    'PacI': ['TTAATTAAT', 1, 8, 'np'],
    'PaeR7I': ['CTCGAG', 1, 5, 'p'],
    'PaqCI': ['CACCTGC', 4, 8, 'np'],
    'PciI': ['ACATGT', 1, 5, 'p'],
    #'PflFI': ['GACNNNGTC', 1, 8, 'p'],
    #'PflMI': ['CCANNNNTGG', 1, 9, 'p'],
    'PleI': ['GAGTC', 4, 5, 'np'],
    'PluTI': ['GGCGCC', 1, 5, 'p'],
    'PmeI': ['GTTTAAAC', 1, 7, 'p'],
    'PmlI': ['CACGTG', 1, 5, 'p'],
    #'PshAI': ['GACNNNNGTC', 1, 9, 'p'],
    'PsiI-v2': ['TTATAA', 1, 5, 'p'],
    'PspGI': ['CCWGG', 1, 4, 'p'],
    'PspOMI': ['GGGCCC', 1, 5, 'p'],
    'PspXI': ['VCTCGAGB', 1, 7, 'p'],
    'PstI': ['CTGCAG', 1, 5, 'p'],
    'PvuI-HF®': ['CGATCG', 1, 5, 'p'],
    'PvuII': ['CAGCTG', 1, 5, 'p'],
    'RsaI': ['GTAC', 1, 3, 'p'],
    'RsrII': ['CGGWCCG', 1, 6, 'p'],
    'SacI-HF®': ['GAGCTC', 1, 5, 'p'],
    'SacII': ['CCGCGG', 1, 5, 'p'],
    'SalI': ['GTCGAC', 1, 5, 'p'],
    'SanDI': ['GGGWCCC', 1, 6, 'p'],
    'SapI': ['GCTCTTC', 1, 4, 'np'],
    'Sau3AI': ['GATC', 1, 3, 'p'],
    'Sau96I': ['GGNCC', 1, 4, 'p'],
    'SbfI-HF®': ['CCTGCAGG', 1, 7, 'p'],
    'ScaI-HF®': ['AGTACT', 1, 5, 'p'],
    'ScrFI': ['CCNGG', 1, 4, 'p'],
    'SexAI': ['ACCWGGT', 1, 7, 'p'],
    'SfcI': ['CTRYAG', 1, 5, 'p'],
    #'SfiI': ['GGCCNNNNNGGCC', 1, 12, 'p'],
    'SfoI': ['GGCGCC', 1, 5, 'p'],
    'SgrAI': ['CRCCGGYG', 1, 7, 'p'],
    'SmaI': ['CCCGGG', 1, 5, 'p'],
    'SmlI': ['CTYRAG', 1, 5, 'p'],
    'SpeI-HF®': ['ACTAGT', 1, 5, 'p'],
    'SphI': ['GCATGC', 1, 5, 'p'],
    'SrfI': ['GCCCGGGC', 1, 7, 'p'],
    'SspI-HF®': ['AATATT', 1, 5, 'p'],
    'StuI': ['AGGCCT', 1, 5, 'p'],
    'StyD4I': ['CCNGG', 1, 4, 'p'],
    'StyI-HF®': ['CCWWGG', 1, 5, 'p'],
    'SwaI': ['ATTTAAAT', 1, 7, 'p'],
    'TaqI-v2': ['TCGA', 1, 3, 'p'],
    'TfiI': ['GAWTC', 1, 4, 'p'],
    'Tsp45I': ['GTSAC', 1, 4, 'p'],
    'TspMI': ['CCCGGG', 1, 5, 'p'],
    'TspRI': ['CASTG', 1, 9, 'p'],
    #'Tth111I': ['GACNNNGTC', 1, 8, 'p'],
    'XbaI': ['TCTAGA', 1, 5, 'p'],
    #'XcmI': ['CCANNNNNNNNNTGG', 1, 15, 'p'],
    'XhoI': ['CTCGAG', 1, 5, 'p'],
    'XmaI': ['CCCGGG', 1, 5, 'p'],
    #'XmnI': ['GAANNNNTTC', 1, 9, 'p'],
    'ZraI': ['GACGTC', 1, 5, 'p']
}
'''

# Seu dicionário de enzimas
enzymes = {
    'AatII': ['GACGTC', 1, 5, 'p'],
    'Acc65I': ['GGTACC', 1, 5, 'p'],
    'AccI': ['GTMKAC', 1, 5, 'p'],
    'AflIII': ['ACRYGT', 1, 6, 'p'],
    'AgeI-HF®': ['ACCGGT', 1, 5, 'p'],
    'ApaI': ['GGGCCC', 1, 5, 'p'],
    'AscI': ['GGCGCGCC', 1, 7, 'p'],
    'AvrII': ['CCTAGG', 1, 5, 'p'],
    'BamHI': ['GGATCC', 1, 5, 'p'],
    'BanI': ['GGYRCC', 1, 5, 'p'],
    'BbsI': ['GAAGAC', 2, 6, 'np'],
    'BclI': ['TGATCA', 1, 5, 'p'],
    'BfaI': ['CTAG', 1, 3, 'p'],
    'BglII': ['AGATCT', 1, 5, 'p'],
    'BsaI-HF®v2': ['GGTCTC', 1, 5, 'np'],
    'BsiWI': ['CGTACG', 1, 5, 'p'],
    'BsmBI-v2': ['CGTCTC', 1, 5, 'np'],
    'BssHII': ['GCGCGC', 1, 5, 'p'],
    'BstBI': ['TTCGAA', 1, 5, 'p'],
    'ClaI': ['ATCGAT', 1, 5, 'p'],
    'EcoRI': ['GAATTC', 1, 5, 'p'],
    'EcoRV': ['GATATC', 1, 5, 'p'],
    'FokI': ['GGATG', 14, -13, 'np'],
    'HincII': ['GTYRAC', 1, 5, 'p'],
    'HindIII': ['AAGCTT', 1, 5, 'p'],
    'KpnI-HF®': ['GGTACC', 1, 5, 'p'],
    'MluI-HF®': ['ACGCGT', 1, 5, 'p'],
    'NciI': ['CCSGG', 1, 4, 'p'],
    'NcoI': ['CCATGG', 1, 5, 'p'],
    'NdeI': ['CATATG', 1, 5, 'p'],
    'NheI-HF®': ['GCTAGC', 1, 5, 'p'],
    'NotI': ['GCGGCCGC', 1, 7, 'p'],
    'PstI': ['CTGCAG', 1, 5, 'p'],
    'SacI-HF®': ['GAGCTC', 1, 5, 'p'],
    'SapI': ['GCTCTTC', 1, 4, 'np'],
    'XbaI': ['TCTAGA', 1, 5, 'p'],
    'XhoI': ['CTCGAG', 1, 5, 'p']
    }

# Tabela de códons
codon_table = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
    'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
}

codon_usage_human = {
    'UUU': 17.6, 'UCU': 15.2, 'UAU': 12.2, 'UGU': 10.6,
    'UUC': 20.3, 'UCC': 17.7, 'UAC': 15.3, 'UGC': 12.6,
    'UUA': 7.7,  'UCA': 12.2, 'UAA': 1.0,  'UGA': 1.6,
    'UUG': 12.9, 'UCG': 4.4,  'UAG': 0.8,  'UGG': 13.2,
    'CUU': 13.2, 'CCU': 17.5, 'CAU': 10.9, 'CGU': 4.5,
    'CUC': 19.6, 'CCC': 19.8, 'CAC': 15.1, 'CGC': 10.4,
    'CUA': 7.2,  'CCA': 16.9, 'CAA': 12.3, 'CGA': 6.2,
    'CUG': 39.6, 'CCG': 6.9,  'CAG': 34.2, 'CGG': 11.4,
    'AUU': 16.0, 'ACU': 13.1, 'AAU': 17.0, 'AGU': 12.1,
    'AUC': 20.8, 'ACC': 18.9, 'AAC': 19.1, 'AGC': 19.5,
    'AUA': 7.5,  'ACA': 15.1, 'AAA': 24.4, 'AGA': 12.2,
    'AUG': 22.0, 'ACG': 6.1,  'AAG': 31.9, 'AGG': 12.0,
    'GUU': 11.0, 'GCU': 18.4, 'GAU': 21.8, 'GGU': 10.8,
    'GUC': 14.5, 'GCC': 27.7, 'GAC': 25.1, 'GGC': 22.2,
    'GUA': 7.1,  'GCA': 15.8, 'GAA': 29.0, 'GGA': 16.5,
    'GUG': 28.1, 'GCG': 7.4,  'GAG': 39.6, 'GGG': 16.5}
codon_usage_ecoli = {
    'UUU': 23.2, 'UCU': 8.7,  'UAU': 16.5, 'UGU': 5.5,
    'UUC': 16.9, 'UCC': 8.9,  'UAC': 12.1, 'UGC': 6.9,
    'UUA': 13.9, 'UCA': 7.8,  'UAA': 2.0,  'UGA': 1.1,
    'UUG': 14.0, 'UCG': 8.7,  'UAG': 0.3,  'UGG': 15.2,
    'CUU': 11.7, 'CCU': 7.3,  'CAU': 13.6, 'CGU': 20.3,
    'CUC': 11.0, 'CCC': 5.8,  'CAC': 9.8,  'CGC': 21.0,
    'CUA': 4.0,  'CCA': 8.5,  'CAA': 15.0, 'CGA': 3.9,
    'CUG': 50.9, 'CCG': 21.8, 'CAG': 29.5, 'CGG': 6.3,
    'AUU': 29.8, 'ACU': 9.1,  'AAU': 18.6, 'AGU': 9.5,
    'AUC': 24.2, 'ACC': 22.8, 'AAC': 21.4, 'AGC': 16.0,
    'AUA': 5.4,  'ACA': 8.2,  'AAA': 33.2, 'AGA': 2.9,
    'AUG': 27.0, 'ACG': 14.8, 'AAG': 10.7, 'AGG': 1.9,
    'GUU': 18.5, 'GCU': 15.6, 'GAU': 32.1, 'GGU': 24.4,
    'GUC': 15.1, 'GCC': 25.1, 'GAC': 18.6, 'GGC': 27.9,
    'GUA': 11.1, 'GCA': 20.6, 'GAA': 38.2, 'GGA': 9.0,
    'GUG': 25.5, 'GCG': 31.7, 'GAG': 17.7, 'GGG': 11.3}
codon_usage_yeast = { 
    'UUU': 26.1, 'UCU': 23.5, 'UAU': 18.8, 'UGU': 8.1,
    'UUC': 18.4, 'UCC': 14.2, 'UAC': 14.8, 'UGC': 4.8,
    'UUA': 26.2, 'UCA': 18.7, 'UAA': 1.1,  'UGA': 0.7,
    'UUG': 27.2, 'UCG': 8.6,  'UAG': 0.5,  'UGG': 10.4,
    'CUU': 12.3, 'CCU': 13.5, 'CAU': 13.6, 'CGU': 6.4,
    'CUC': 5.4,  'CCC': 6.8,  'CAC': 7.8,  'CGC': 2.6,
    'CUA': 13.4, 'CCA': 18.3, 'CAA': 27.3, 'CGA': 3.0,
    'CUG': 10.5, 'CCG': 5.3,  'CAG': 12.1, 'CGG': 1.7,
    'AUU': 30.1, 'ACU': 20.3, 'AAU': 35.7, 'AGU': 14.2,
    'AUC': 17.2, 'ACC': 12.7, 'AAC': 24.8, 'AGC': 9.8,
    'AUA': 17.8, 'ACA': 17.8, 'AAA': 41.9, 'AGA': 21.3,
    'AUG': 20.9, 'ACG': 8.0,  'AAG' :30.8, 'AGG': 9.2,
    'GUU': 22.1, 'GCU': 21.2, 'GAU': 37.6, 'GGU': 23.9,
    'GUC': 11.8, 'GCC': 12.6, 'GAC': 20.2, 'GGC': 9.8,
    'GUA': 11.8, 'GCA': 16.2, 'GAA': 45.6, 'GGA': 10.9,
    'GUG': 10.8, 'GCG': 6.2,  'GAG': 19.2, 'GGG': 6.0}

codon_usage_tables = {
    'Human': codon_usage_human,
    'E. coli': codon_usage_ecoli,
    'Yeast': codon_usage_yeast
}
'''
# https://www.kazusa.or.jp/codon/cgi-bin/showcodon.cgi?species=4932
codon_usage = {
    'UUU': 26.1, 'UCU': 23.5, 'UAU': 18.8, 'UGU': 8.1,
    'UUC': 18.4, 'UCC': 14.2, 'UAC': 14.8, 'UGC': 4.8,
    'UUA': 26.2, 'UCA': 18.7, 'UAA': 1.1,  'UGA': 0.7,
    'UUG': 27.2, 'UCG': 8.6,  'UAG': 0.5,  'UGG': 10.4,
    'CUU': 12.3, 'CCU': 13.5, 'CAU': 13.6, 'CGU': 6.4,
    'CUC': 5.4,  'CCC': 6.8,  'CAC': 7.8,  'CGC': 2.6,
    'CUA': 13.4, 'CCA': 18.3, 'CAA': 27.3, 'CGA': 3.0,
    'CUG': 10.5, 'CCG': 5.3,  'CAG': 12.1, 'CGG': 1.7,
    'AUU': 30.1, 'ACU': 20.3, 'AAU': 35.7, 'AGU': 14.2,
    'AUC': 17.2, 'ACC': 12.7, 'AAC': 24.8, 'AGC': 9.8,
    'AUA': 17.8, 'ACA': 17.8, 'AAA': 41.9, 'AGA': 21.3,
    'AUG': 20.9, 'ACG': 8.0,  'AAG' :30.8, 'AGG': 9.2,
    'GUU': 22.1, 'GCU': 21.2, 'GAU': 37.6, 'GGU': 23.9,
    'GUC': 11.8, 'GCC': 12.6, 'GAC': 20.2, 'GGC': 9.8,
    'GUA': 11.8, 'GCA': 16.2, 'GAA': 45.6, 'GGA': 10.9,
    'GUG': 10.8, 'GCG': 6.2,  'GAG': 19.2, 'GGG': 6.0}
'''
#sequencia
#TTTTTAATCGGTGGATGCCATCCGGATGCGGCGTGAATTTTT
#TTTTTAATCGGTGGATGCCATCCAGATGCGGCGTGAATTTTT

# DO CÓDIGO NOVO ============================================
# Dicionário IUPAC para bases degeneradas
degenerate_bases = {
    'R': ['A', 'G'], 'Y': ['C', 'T'], 'S': ['G', 'C'],
    'W': ['A', 'T'], 'K': ['G', 'T'], 'M': ['A', 'C'],
    'B': ['C', 'G', 'T'], 'D': ['A', 'G', 'T'],
    'H': ['A', 'C', 'T'], 'V': ['A', 'C', 'G'],
    'N': ['A', 'T', 'C', 'G','N'],
}

def rev_comp(seq):
    complement = {'A':'T', 'T':'A', 
                   'C':'G', 'G':'C',
                   'Y':'R', 'R':'Y',
                   'K':'M', 'M':'K',
                   'D':'H', 'H':'D',
                   'V':'B', 'B':'V',
                   'W':'W', 'S':'S',
                   'N':'N'}
    return ''.join([complement.get(base.upper(), 'N') for base in seq[::-1]])

'''
def rev_comp(seq):
    """Calcula o reverso complementar de uma sequência de DNA."""
    complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N': 'N'}
    return "".join(complement_map.get(base, 'N') for base in reversed(seq.upper()))
'''
def find_variable_region(seq1, seq2):
    len1, len2 = len(seq1), len(seq2)
    lcp_len = 0
    for i in range(min(len1, len2)):
        if seq1[i] == seq2[i]:
            lcp_len += 1
        else:
            break
    lcs_len = 0
    for i in range(min(len1, len2)):
        if lcp_len + lcs_len >= min(len1, len2):
            break
        if seq1[len1 - 1 - i] == seq2[len2 - 1 - i]:
            lcs_len += 1
        else:
            break
    return lcp_len, lcs_len

# pos_l_s1, base_l_s1, pos_l_s2, base_l_s2, pos_r_s1, base_r_s1, pos_r_s2, base_r_s2
def get_snp_positions(seq1, seq2):
    len1 = len(seq1)
    len2 = len(seq2)
    lcp_len, lcs_len = find_variable_region(seq1, seq2)
    pos_l_s1 = pos_l_s2 = lcp_len + 1
    base_l_s1 = seq1[lcp_len]
    base_l_s2 = seq2[lcp_len]
    pos_r_s1 = len1 - lcs_len
    base_r_s1 = seq1[pos_r_s1 - 1]
    pos_r_s2 = len2 - lcs_len
    base_r_s2 = seq2[pos_r_s2 - 1]
    return pos_l_s1, base_l_s1, pos_l_s2, base_l_s2, pos_r_s1, base_r_s1, pos_r_s2, base_r_s2

def highlight_changes(modified_seq, original_seq):
    """
    Compara duas sequências de mesmo comprimento e retorna uma string
    HTML com as diferenças destacadas em outra cor.
    """
    original_upper = original_seq.upper()
    modified_upper = modified_seq.upper()
    highlighted_output = ""
    
    if len(original_upper) != len(modified_upper):
        return modified_upper  # Se o tamanho for diferente, retorna sem comparação

    for i in range(len(original_upper)):
        if original_upper[i] != modified_upper[i]:
            # Usa <span> para colorir a base diferente
            highlighted_output += f'<span style="background-color:yellow">{modified_upper[i]}</span>'
        else:
            highlighted_output += original_upper[i]
    return highlighted_output
#REVISAR ESSA FUNÇÂO ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# (enzyme_name, site_pattern, i + 1, i + site_len, dna_segment, num_mismatches, mismatch_pos)
def find_rs_new(seq, enzymes, max_mismatch=3):
    rs_info = []
    for enzyme_name, enzyme_data in enzymes.items():
        site_pattern = enzyme_data[0].upper()
        site_len = len(site_pattern)
        for i in range(len(seq) - site_len + 1):
            dna_segment = seq[i : i + site_len]
            num_mismatches = 0
            mismatch_pos = []
            process = True
            for j in range(site_len):
                base_dna = dna_segment[j]
                base_enzyme = site_pattern[j]
                if base_enzyme in degenerate_bases:
                    if base_dna in degenerate_bases[base_enzyme]:
                        continue
                if base_dna != base_enzyme:
                    num_mismatches += 1
                    if num_mismatches > max_mismatch:
                        process = False 
                        break 
                    mismatch_pos.append(i + j + 1)
            if process: 
                results = (enzyme_name, site_pattern, i + 1, i + site_len, dna_segment, num_mismatches, mismatch_pos)
                rs_info.append(results)  
    return rs_info

# filter (SNP out of enzyme site) or (SNP = mismatch position) or (SNP between mismatches) 
def filter_rs(rs_seq, snp_position):
    resultados_filtrados = []
    for item in rs_seq:
        site_start = item[2]
        site_end = item[3]
        mismatch_positions = item[6]
        if not (site_start <= snp_position <= site_end):
            continue
        if snp_position in mismatch_positions:
            continue
        mismatch_before = any(p < snp_position for p in mismatch_positions)
        mismatch_after = any(p > snp_position for p in mismatch_positions)
        if mismatch_before and mismatch_after:
            continue
        resultados_filtrados.append(item)
    return resultados_filtrados

#find unique rs in seq
def find_unique_rs(rs_s1_filtered, rs_s2_filtered):
    def build_key(item):
        try:
            return (item[0], item[1], item[2], item[3], tuple(sorted(item[6])))
        except TypeError:
            return (item[0], item[1], item[2], item[3], item[6]) 
    keys_s2 = {build_key(item) for item in rs_s2_filtered}
    results = []
    for item in rs_s1_filtered:
        if build_key(item) not in keys_s2:
            results.append(item)
    return results

# (enzyme_name, enzyme_pattern, site_start, site_end, design_primer, test1, test2, primer_type)]
#test1 and test2 are relatives; for s1 test1~seq1, test2~seq2, but for s2 test1~seq2 and test2~seq1
def design_primers_dcaps_seq(seq1, seq2, unique_rs, snp_pos):
    results = [] 
    snp_pos_0 = snp_pos - 1
    for item in unique_rs: 
        enzyme_name = item[0]
        enzyme_pattern = item[1] 
        site_start = item[2]
        site_end = item[3]
        mismatch_pos = item[6]
        if not mismatch_pos:
            continue
        relevant_mismatch_pos = max(mismatch_pos) 
        design_primer = None
        primer_type = None
        test1 = None 
        test2 = None 
        if relevant_mismatch_pos < snp_pos:
            primer_type = "Forward"
            part1 = seq1[:site_start - 1]
            part2 = enzyme_pattern[:snp_pos - site_start]
            design_primer = part1 + part2
            test1 = design_primer + seq1[snp_pos_0:]
            test2 = design_primer + seq2[snp_pos_0:]
        else:
            primer_type = "Reverse"
            part1 = enzyme_pattern[snp_pos - site_start + 1 :]
            part2 = seq1[site_end:]
            design_primer = part1 + part2
            test1 = seq1[:snp_pos] + design_primer
            test2 = seq2[:snp_pos] + design_primer
        if design_primer: 
            results.append(
                (enzyme_name, enzyme_pattern, site_start, site_end, design_primer, test1, test2, primer_type))
    return results

#if enzyme_pattern in test1 != in test2, it is a dCAPS
def valid_primers(primers):
    results = []
    deg_bases = {
        'A': '[A]', 'T': '[T]', 'C': '[C]', 'G': '[G]', 
        'R': '[AGR]', 'Y': '[CTY]', 'S': '[GCS]', 'W': '[ATW]', 
        'K': '[GTK]', 'M': '[ACM]', 'B': '[CGTB]', 'D': '[AGTD]',
        'H': '[ACTH]', 'V': '[ACGV]', 'N': '[ATCGRYSWKMBDHVN]',
    }
    if not primers:
        return results
    for item in primers:
        enzyme_pattern = item[1]
        test1 = item[5]
        test2 = item[6]
        find_test1 = False
        find_test2 = False
        regex_pattern = ""
        is_degenerate = False
        for base in enzyme_pattern:
            if base in deg_bases:
                regex_pattern += deg_bases[base]
                is_degenerate = True
            else:
                regex_pattern += base # Adiciona bases literais como A, C, T, G
        if is_degenerate:
            find_test1 = bool(re.search(regex_pattern, test1))
            find_test2 = bool(re.search(regex_pattern, test2))
        else:
            find_test1 = enzyme_pattern in test1
            find_test2 = enzyme_pattern in test2
        if find_test1 != find_test2:
            results.append(item)        
    return results

# Natural logic
def get_final_primers(validated_primers, seq):
    results = []
    for item in validated_primers:
        enzyme_name = item[0]
        enzyme_pattern = item[1]
        site_start = item[2]
        site_end = item[3]
        design_primer = item[4]
        primer_type = item[7]
        if primer_type == "Forward":
            seq_cut = seq[:len(design_primer)]
            primer_h = highlight_changes(design_primer, seq_cut)
            final_list = (enzyme_name, enzyme_pattern, site_start, site_end, design_primer, primer_type, seq_cut, primer_h)
            results.append(final_list)
        elif primer_type == "Reverse":
            seq_rc = rev_comp(seq)
            design_primer = rev_comp(design_primer)
            seq_cut_rc = (seq_rc[:len(design_primer)])
            primer_h_rc = highlight_changes(design_primer, seq_cut_rc)
            final_list = (enzyme_name, enzyme_pattern, site_start, site_end, design_primer, primer_type, seq_cut_rc, primer_h_rc)
            results.append(final_list)        
    return results

# Rev-comp logic
def get_final_primers_rc(validated_primers, seq):
    results = []
    for item in validated_primers:
        enzyme_name = item[0]
        enzyme_pattern = item[1]
        site_start = item[2]
        site_end = item[3]
        design_primer = item[4]
        primer_type = item[7]
        if primer_type == "Reverse":
            seq_rc = rev_comp(seq)
            design_primer = rev_comp(design_primer)
            seq_cut_rc = (seq_rc[:len(design_primer)])
            primer_h_rc = highlight_changes (design_primer, seq_cut_rc)
            final_list = (enzyme_name, enzyme_pattern, site_start, site_end, design_primer, "Forward", seq_cut_rc, primer_h_rc)
            results.append(final_list) 
        elif primer_type == "Forward":
            seq_cut = seq[:len(design_primer)]
            primer_h = highlight_changes(design_primer, seq_cut)
            final_list = (enzyme_name, enzyme_pattern, site_start, site_end, design_primer, "Reverse", seq_cut, primer_h)
            results.append(final_list)        
    return results

# PARA GERAR ENZIMA NO DONOR
def expand_sites(pattern):
    expanded = []
    for base in pattern.upper():
        if base in degenerate_bases:
            expanded.append(degenerate_bases[base])
        else:
            expanded.append([base])
    return [''.join(comb) for comb in product(*list_of_possible_bases)]

def generate_modified_sequences(original_seq, rs_candidates):
    results = []
    for item in rs_candidates:
        enzyme_name = item[0]
        enzyme_pattern = item[1]
        start_pos_1based = item[2]
        end_pos_1based = item[3]
        possible_sites = expand_degenerate_site(enzyme_pattern)
        for concrete_site in possible_sites:
            prefix = original_seq[0 : start_pos_1based - 1]
            suffix = original_seq[end_pos_1based:]
            new_sequence = prefix + concrete_site + suffix
            output_tuple = (
                enzyme_name,
                enzyme_pattern, # Mantém o padrão original para referência
                start_pos_1based,
                end_pos_1based,
                new_sequence
            )
            results.append(output_tuple)        
    return results

# PARA TRABALHAR COM CODON USAGE
def get_codon_changes(original_seq, modified_seq_info_list, codon_usage_table):
    final_results_with_comparison = []

    # Itera sobre cada sequência modificada candidata
    for item in modified_seq_info_list:
        enzyme_name = item[0]
        enzyme_pattern = item[1]
        start_pos = item[2]
        end_pos = item[3]
        modified_seq = item[4]
        # Itera sobre os códons das sequências original e modificada
        for i in range(0, len(original_seq), 3):
            original_codon_dna = original_seq[i:i+3].upper()
            modified_codon_dna = modified_seq[i:i+3].upper()

            # Pula códons incompletos no final da sequência
            if len(original_codon_dna) < 3 or len(modified_codon_dna) < 3:
                continue
            
            # **LÓGICA PRINCIPAL: Executa apenas se os códons forem diferentes**
            if original_codon_dna != modified_codon_dna:
                original_codon_rna = original_codon_dna.replace('T', 'U')
                modified_codon_rna = modified_codon_dna.replace('T', 'U')

                original_usage = codon_usage_table.get(original_codon_rna, 0.0) # Usar 0.0 para facilitar o cálculo
                modified_usage = codon_usage_table.get(modified_codon_rna, 0.0)
                
                difference_str = ""
                # Garante que ambos os usos são numéricos para calcular a diferença
                if isinstance(original_usage, (int, float)) and isinstance(modified_usage, (int, float)):
                    if original_usage > 0 and modified_usage > 0:
                        if original_usage > modified_usage:
                            # Cálculo corrigido e mais intuitivo para diminuição
                            fold_change = original_usage / modified_usage
                            difference_str = f"-{fold_change:.1f}x"
                        elif modified_usage > original_usage:
                            # **CÁLCULO CORRIGIDO** para aumento
                            fold_change = modified_usage / original_usage
                            difference_str = f"+{fold_change:.1f}x"
                        else:
                            difference_str = "(=)"
                    elif original_usage > 0 and modified_usage == 0:
                        difference_str = "(Uso eliminado)"
                    elif original_usage == 0 and modified_usage > 0:
                        difference_str = "(Uso introduzido)"

                # **CORREÇÃO PRINCIPAL: O resultado é criado e adicionado AQUI**
                # Cada tupla representa uma única mudança de códon encontrada
                modified_seq_h = highlight_changes(modified_seq, original_seq)
                output_tuple = (
                    enzyme_name,
                    f"{original_codon_dna} ({original_usage}) → {modified_codon_dna} ({modified_usage})", # Mudança
                    difference_str, # Análise do uso
                    start_pos,
                    end_pos,
                    modified_seq_h,
                    enzyme_pattern
                )
                final_results_with_comparison.append(output_tuple)
                
    return final_results_with_comparison

#REVISAR ESSA FUNÇÂO ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


#PARA GRNAS

# Dicionário IUPAC para bases degeneradas, para validar a PAM
DEGENERATE_BASES = {
    'R': ['A', 'G'], 'Y': ['C', 'T'], 'S': ['G', 'C'],
    'W': ['A', 'T'], 'K': ['G', 'T'], 'M': ['A', 'C'],
    'B': ['C', 'G', 'T'], 'D': ['A', 'G', 'T'],
    'H': ['A', 'C', 'T'], 'V': ['A', 'C', 'G'],
    'N': ['A', 'T', 'C', 'G'],
}


#REVISAR ESSA FUNÇÂO ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

def match_degenerate(sequence, pattern):
    """
    Verifica se uma sequência de DNA corresponde a um padrão degenerado.
    Ex: match_degenerate('GGC', 'NGG') -> True
    """
    if len(sequence) != len(pattern):
        return False
    for i in range(len(pattern)):
        base_pattern = pattern[i]
        base_seq = sequence[i]
        if base_pattern == 'N':
            continue
        if base_pattern in DEGENERATE_BASES:
            if base_seq not in DEGENERATE_BASES[base_pattern]:
                return False
        elif base_pattern != base_seq:
            return False
    return True
#REVISAR ESSA FUNÇÂO ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

def find_pam_for_grnas(target_seq, grna_list):
    """
    Encontra a posição e a PAM para uma lista de gRNAs em uma sequência alvo.

    Args:
        target_seq (str): A sequência de DNA a ser pesquisada.
        grna_list (list): Uma lista de sequências de gRNA (20-nt).

    Returns:
        list: Uma lista de tuplas com os resultados.
              Formato: (gRNA, position_1_based, pam_type, pam_position_1_based)
    """
    results = []
    target_seq_upper = target_seq.upper()
    
    # Definindo os padrões PAM
    pam_forward_pattern = "NGG"
    pam_reverse_pattern = "CCN"

    for grna in grna_list:
        grna_upper = grna.upper()
        found = False

        # --- Busca na Fita Forward (PAM NGG depois do gRNA) ---
        # A sequência do gRNA deve corresponder diretamente à fita forward
        for match in re.finditer(grna_upper, target_seq_upper):
            grna_pos_0b = match.start()
            pam_start_0b = grna_pos_0b + len(grna_upper)
            
            # Verifica se a PAM está dentro dos limites da sequência
            if pam_start_0b + len(pam_forward_pattern) <= len(target_seq_upper):
                actual_pam_seq = target_seq_upper[pam_start_0b : pam_start_0b + len(pam_forward_pattern)]
                if match_degenerate(actual_pam_seq, pam_forward_pattern):
                    results.append(
                        (grna, grna_pos_0b + 1, pam_forward_pattern, pam_start_0b + 1)
                    )
                    found = True
                    break # Assume que encontraremos apenas a primeira ocorrência
        
        if found:
            continue

        # --- Busca na Fita Reverse (PAM CCN antes do alvo) ---
        # A sequência alvo na fita forward será o reverso complementar do gRNA
        target_on_fwd = rev_comp(grna_upper)
        for match in re.finditer(target_on_fwd, target_seq_upper):
            target_pos_0b = match.start()
            pam_start_0b = target_pos_0b - len(pam_reverse_pattern)

            # Verifica se a PAM está dentro dos limites da sequência
            if pam_start_0b >= 0:
                actual_pam_seq = target_seq_upper[pam_start_0b : pam_start_0b + len(pam_reverse_pattern)]
                if match_degenerate(actual_pam_seq, pam_reverse_pattern):
                    results.append(
                        (grna, target_pos_0b + 1, pam_reverse_pattern, pam_start_0b + 1)
                    )
                    found = True
                    break # Assume que encontraremos apenas a primeira ocorrência

    return results
#REVISAR ESSA FUNÇÂO ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


'''
def generate_and_analyze_pam_modifications(original_seq, pam_results):
    """
    Gera todas as mutações pontuais possíveis em uma PAM, analisa se a PAM
    foi destruída e qual o impacto na proteína.

    Args:
        original_seq (str): A sequência de DNA original.
        pam_results (list): Lista de tuplas com os resultados da busca de PAM.
            Formato: (gRNA, gRNA_pos, pam_type, pam_pos_1based)

    Returns:
        dict: Um dicionário onde as chaves são os gRNAs e os valores são listas
              de dicionários, cada um detalhando uma modificação válida.
    """
    all_results = {}
    
    for pam_info in pam_results:
        grna, _, pam_type, pam_pos_1based = pam_info
        
        if grna not in all_results:
            all_results[grna] = []

        pam_pos_0b = pam_pos_1based - 1
        pam_len = len(pam_type)
        
        # Pega o segmento original da PAM na sequência
        original_pam_segment = original_seq[pam_pos_0b : pam_pos_0b + pam_len].upper()

        # Itera sobre cada posição dentro do segmento da PAM (0, 1, 2)
        for i in range(pam_len):
            # Tenta substituir a base em cada posição por todas as outras bases
            for new_base in ['A', 'C', 'G', 'T']:
                original_base = original_pam_segment[i]
                
                # Pula se a "modificação" for igual à base original
                if new_base == original_base:
                    continue
                
                # Cria o novo segmento PAM modificado
                temp_list = list(original_pam_segment)
                temp_list[i] = new_base
                modified_pam_segment = "".join(temp_list)
                
                # 1. ANÁLISE: A PAM FOI REALMENTE REMOVIDA?
                # Se o novo segmento ainda corresponde ao padrão PAM, não é uma boa modificação.
                if match_degenerate(modified_pam_segment, pam_type):
                    continue
                    
                # 2. ANÁLISE: QUAL O IMPACTO NO CÓDON?
                mutation_pos_0b = pam_pos_0b + i
                codon_start_index = (mutation_pos_0b // 3) * 3
                
                # Garante que podemos extrair um códon completo
                if codon_start_index + 3 > len(original_seq):
                    continue

                # Constrói a sequência completa modificada
                modified_seq = original_seq[:mutation_pos_0b] + new_base + original_seq[mutation_pos_0b + 1:]
                
                original_codon = original_seq[codon_start_index : codon_start_index + 3]
                modified_codon = modified_seq[codon_start_index : codon_start_index + 3]
                
                original_aa = translate(original_codon, codon_table)
                modified_aa = translate(modified_codon, codon_table)
                
                is_silent = (original_aa == modified_aa)
                
                original_codon_rna = original_codon.replace('T', 'U')
                modified_codon_rna = modified_codon.replace('T', 'U')
                original_usage = codon_usage.get(original_codon_rna, 'N/A')
                modified_usage = codon_usage.get(modified_codon_rna, 'N/A')

                # Armazena todas as informações úteis
                if is_silent:  
                    modification_details = {
                        "modification": f"{original_base} -> {new_base}",
                        "mutation_position_1based": mutation_pos_0b + 1,
                        "original_pam_segment": original_pam_segment,
                        "modified_pam_segment": modified_pam_segment,
                        "pam_removed": True,
                        "codon_change": f"{original_codon}({original_aa}) -> {modified_codon}({modified_aa})",
                        "is_silent": is_silent,
                        "full_modified_sequence": modified_seq
                    }
                    all_results[grna].append(modification_details)

    return all_results
'''
'''
def generate_and_analyze_pam_modifications(original_seq, pam_results):
    all_results = {}
    for pam_info in pam_results:
        grna, _, pam_type, pam_pos_1based = pam_info
        if grna not in all_results:
            all_results[grna] = []
        pam_pos_0b = pam_pos_1based - 1
        pam_len = len(pam_type)
        if pam_pos_0b + pam_len > len(original_seq): continue
        original_pam_segment = original_seq[pam_pos_0b : pam_pos_0b + pam_len].upper()
        for i in range(pam_len):
            for new_base in ['A', 'C', 'G', 'T']:
                original_base = original_pam_segment[i]
                if new_base == original_base:
                    continue
                
                # Cria o novo segmento PAM modificado
                temp_list = list(original_pam_segment)
                temp_list[i] = new_base
                modified_pam_segment = "".join(temp_list)
                
                # 1. ANÁLISE: A PAM FOI REALMENTE REMOVIDA?
                if match_degenerate(modified_pam_segment, pam_type):
                    continue
                    
                # 2. ANÁLISE: QUAL O IMPACTO NO CÓDON?
                mutation_pos_0b = pam_pos_0b + i
                codon_start_index = (mutation_pos_0b // 3) * 3
                
                if codon_start_index + 3 > len(original_seq):
                    continue

                # Constrói a sequência completa modificada
                modified_seq = original_seq[:mutation_pos_0b] + new_base + original_seq[mutation_pos_0b + 1:]
                
                original_codon = original_seq[codon_start_index : codon_start_index + 3]
                modified_codon = modified_seq[codon_start_index : codon_start_index + 3]
                
                original_aa = translate(original_codon, codon_table)
                modified_aa = translate(modified_codon, codon_table)
                
                is_silent = (original_aa == modified_aa)
                
                # Filtra para manter apenas as modificações silenciosas
                if is_silent:
                    # Análise de uso de códons
                    original_codon_rna = original_codon.replace('T', 'U')
                    modified_codon_rna = modified_codon.replace('T', 'U')
                    original_usage = codon_usage.get(original_codon_rna, 'N/A')
                    modified_usage = codon_usage.get(modified_codon_rna, 'N/A')
                    
                    difference_str = ""
                    if isinstance(original_usage, (int, float)) and isinstance(modified_usage, (int, float)):
                        if original_usage > 0 and modified_usage > 0:
                            if original_usage > modified_usage:
                                fold_change = 1 / (original_usage / modified_usage)
                                difference_str = f" (Diminuição de {fold_change:.1f}x)"
                            elif modified_usage > original_usage:
                                fold_change = 1 / (original_usage / modified_usage)
                                difference_str = f" (Aumento de {fold_change:.1f}x)"
                        elif original_usage > 0 and modified_usage == 0:
                            difference_str = " (Uso eliminado)"
                    
                    modification_details = {
                        "modification": f"{original_base} -> {new_base}",
                        "mutation_position_1based": mutation_pos_0b + 1,
                        "original_pam_segment": original_pam_segment,
                        "modified_pam_segment": modified_pam_segment,
                        "pam_removed": True,
                        "codon_change": f"Codon at {codon_start_index+1}: {original_codon}({original_aa}) -> {modified_codon}({modified_aa}) | Usage: {original_usage} -> {modified_usage}{difference_str}",
                        "is_silent": True,
                        "full_modified_sequence": modified_seq
                    }
                    all_results[grna].append(modification_details)

    return all_results
#REVISAR ESSA FUNÇÂO ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
'''
'''
def generate_and_translate_all_variations(target_seq, gRNA_list, codon_table):
    """
    Gera todas as variações de PAM, descarta a que for idêntica à original,
    e traduz as restantes em proteína.
    """
    results_dict = {}
    for gRNA_info in gRNA_list:
        gRNA_sequence = gRNA_info[0]
        pam_pattern = gRNA_info[2]
        pam_start_pos = gRNA_info[3]
        nucleotides = ['A', 'C', 'G', 'T']
        pam_start_idx = pam_start_pos - 1
        
        indices_to_modify = []
        for i, base in enumerate(pam_pattern.upper()):
            if base != 'N':
                indices_to_modify.append(pam_start_idx + i)
        
        # Lista para guardar apenas as sequências que são DIFERENTES da original
        dna_variations = []

        # Apenas gera variações se houver posições a serem modificadas
        if indices_to_modify:
            num_to_modify = len(indices_to_modify)
            all_combinations = itertools.product(nucleotides, repeat=num_to_modify)
            
            for combo in all_combinations:
                # Cria a nova sequência candidata
                new_seq_list = list(target_seq)
                for i, index_to_change in enumerate(indices_to_modify):
                    new_seq_list[index_to_change] = combo[i]
                
                generated_seq = "".join(new_seq_list)
                
                # --- A MUDANÇA PRINCIPAL ESTÁ AQUI ---
                # Adiciona a sequência à lista apenas se ela for diferente da original
                if generated_seq != target_seq:
                    dna_variations.append(generated_seq)

        # Traduz apenas as sequências que passaram pelo filtro
        dna_and_protein_pairs = [{'dna': dna_seq, 'protein': translate(dna_seq, codon_table)} for dna_seq in dna_variations]
        results_dict[gRNA_sequence] = dna_and_protein_pairs
        
    return results_dict
'''
def matches_pam_pattern(dna_seq, pam_pattern):
    """
    Verifica se uma sequência de DNA corresponde a um padrão de PAM (com 'N').
    Retorna True se corresponder, False caso contrário.
    """
    # Garante que ambas tenham o mesmo comprimento para a comparação
    if len(dna_seq) != len(pam_pattern):
        return False
    
    # Compara base a base
    for dna_base, pattern_base in zip(dna_seq.upper(), pam_pattern.upper()):
        # Se a base do padrão não for 'N', as bases do DNA e do padrão devem ser iguais
        if pattern_base != 'N' and dna_base != pattern_base:
            return False
            
    # Se o loop terminar sem encontrar diferenças, então há uma correspondência
    return True
#REVISAR ESSA FUNÇÂO ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def generate_and_translate_synonymous_variations(target_seq, gRNA_list, codon_table):

    results_dict = {}

    # Mapa inverso: aminoácido -> lista de códons
    reverse_codon_table = {}
    for codon, aa in codon_table.items():
        reverse_codon_table.setdefault(aa, []).append(codon)

    for gRNA_info in gRNA_list:

        gRNA_sequence = gRNA_info[0]
        pam_pattern = gRNA_info[2]
        pam_start_pos = gRNA_info[3]

        pam_len = len(pam_pattern)
        pam_start_idx = pam_start_pos - 1
        pam_end_idx = pam_start_idx + pam_len - 1

        first_codon_start_idx = (pam_start_idx // 3) * 3
        last_codon_start_idx = (pam_end_idx // 3) * 3
        codon_block_start = first_codon_start_idx
        codon_block_end = last_codon_start_idx + 3

        original_codon_block = target_seq[codon_block_start:codon_block_end]
        num_codons_in_block = len(original_codon_block) // 3

        valid_dna_variations = []

        for i in range(num_codons_in_block):
            codon_start = codon_block_start + i * 3
            original_codon = target_seq[codon_start : codon_start + 3]
            aa = codon_table.get(original_codon, None)

            if not aa:
                continue  # Codon inválido

            synonymous_codons = reverse_codon_table[aa]

            for syn_codon in synonymous_codons:
                if syn_codon == original_codon:
                    continue  # Evita mutação trivial

                generated_seq = (
                    target_seq[:codon_start] +
                    syn_codon +
                    target_seq[codon_start + 3:]
                )

                new_pam_sequence = generated_seq[pam_start_idx : pam_start_idx + pam_len]

                if not matches_pam_pattern(new_pam_sequence, pam_pattern):
                    valid_dna_variations.append(generated_seq)

        # Traduz cada sequência DNA -> proteína
        dna_and_protein_pairs = [
            {'dna': dna_seq, 'protein': translate(dna_seq, codon_table)}
            for dna_seq in valid_dna_variations
        ]

        results_dict[gRNA_sequence] = dna_and_protein_pairs

    return results_dict
#REVISAR ESSA FUNÇÂO ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# <<< SUA NOVA FUNÇÃO DE FILTRO AQUI >>>
def filter_by_protein(results_dict, reference_protein):
    """
    Filtra os resultados para encontrar variações que geraram uma proteína específica
    e retorna APENAS as sequências de DNA correspondentes.

    Args:
        results_dict (dict): O dicionário completo {gRNA: [{'dna':..., 'protein':...}]}.
        reference_protein (str): A sequência de proteína usada como critério.

    Returns:
        dict: Um novo dicionário no formato {gRNA: ['dna_seq_1', 'dna_seq_2', ...]}.
    """
    filtered_results = {}
    for gRNA, results_list in results_dict.items():
        
        # --- A MUDANÇA ESTÁ AQUI ---
        # Extrai apenas o valor de 'dna' de cada 'pair' que corresponde à condição.
        matching_dna_sequences = [
            pair['dna'] for pair in results_list 
            if pair['protein'] == reference_protein
        ]
        
        # Se a lista de sequências de DNA não estiver vazia, adiciona ao dicionário final.
        if matching_dna_sequences:
            filtered_results[gRNA] = matching_dna_sequences
            
    return filtered_results
#REVISAR ESSA FUNÇÂO ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def count_and_sort_modifications(original_seq, modified_seq_dict):
    """
    Conta as modificações e retorna APENAS as de 1-nt. Se não houver nenhuma,
    retorna as de 2-nt. Descarta todas as outras.

    Args:
        original_seq (str): A sequência de DNA de referência.
        modified_seq_dict (dict): Dicionário no formato {gRNA: ['dna_1', 'dna_2', ...]}.

    Returns:
        dict: Um novo dicionário onde os valores são listas de dicionários,
              contendo apenas as modificações de maior prioridade (1-nt > 2-nt).
              Formato: {gRNA: [{'dna': ..., 'modifications': count}, ...]}.
    """
    final_results = {}

    # Itera sobre cada gRNA e sua lista de sequências de DNA
    for gRNA, dna_list in modified_seq_dict.items():
        
        # Listas temporárias para categorizar as modificações
        one_nt_changes = []
        two_nt_changes = []
        
        # Para cada sequência de DNA modificada...
        for modified_seq in dna_list:
            modification_count = 0
            
            # Compara base a base com a sequência original
            for original_char, modified_char in zip(original_seq, modified_seq):
                if original_char != modified_char:
                    modification_count += 1
            
            # Categoriza o resultado com base na contagem
            if modification_count == 1:
                one_nt_changes.append({
                    'dna': modified_seq,
                    'modifications': 1
                })
            elif modification_count == 2:
                two_nt_changes.append({
                    'dna': modified_seq,
                    'modifications': 2
                })
            # Modificações com mais de 2 nts são ignoradas
        
        # --- APLICA A REGRA DE PRIORIDADE ---
        # Se encontrámos qualquer modificação de 1-nt, elas são o resultado final.
        if one_nt_changes:
            final_results[gRNA] = one_nt_changes
        # Caso contrário, se não houver de 1-nt, usamos as de 2-nt.
        elif two_nt_changes:
            final_results[gRNA] = two_nt_changes
        
    return final_results
#REVISAR ESSA FUNÇÂO ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def analyze_codon_changes(original_seq, final_filtered_dict, codon_usage_table):
    """
    Versão Final: Analisa as mudanças de códon a partir de um dicionário que já
    contém o DNA e a contagem de modificações.

    Args:
        original_seq (str): A sequência de DNA de referência.
        final_filtered_dict (dict): Dicionário no formato {gRNA: [{'dna': ..., 'modifications': count}, ...]}.
        codon_usage_table (dict): Tabela com a frequência de uso de cada códon.

    Returns:
        dict: Um dicionário final com a análise completa, incluindo a contagem de
              modificações e a descrição das mudanças de códon.
    """
    analysis_results = {}

    # Itera sobre cada gRNA e sua lista de resultados
    for gRNA, results_list in final_filtered_dict.items():
        
        gRNA_analysis_list = []
        
        # 'result_item' agora é um dicionário: {'dna': '...', 'modifications': 1}
        for result_item in results_list:
            
            # --- A MUDANÇA PRINCIPAL ESTÁ AQUI ---
            # Extrai a sequência de DNA e a contagem do dicionário de entrada
            modified_seq = result_item['dna']
            modification_count = result_item['modifications']
            
            changes_found = []
            
            # O resto da lógica de comparação de códons permanece o mesmo
            for i in range(0, min(len(original_seq), len(modified_seq)), 3):
                original_codon_dna = original_seq[i:i+3].upper()
                modified_codon_dna = modified_seq[i:i+3].upper()

                if len(original_codon_dna) < 3 or len(modified_codon_dna) < 3:
                    continue

                if original_codon_dna != modified_codon_dna:
                    original_codon_rna = original_codon_dna.replace('T', 'U')
                    modified_codon_rna = modified_codon_dna.replace('T', 'U')
                    
                    original_usage = codon_usage_table.get(original_codon_rna, 0.0)
                    modified_usage = codon_usage_table.get(modified_codon_rna, 0.0)
                    
                    difference_str = ""
                    if original_usage > 0 and modified_usage > 0:
                        if original_usage > modified_usage:
                            # Cálculo corrigido e mais intuitivo para diminuição
                            fold_change = (original_usage / modified_usage)
                            difference_str = f"-{fold_change:.1f}x"
                        elif modified_usage > original_usage:
                            # **CÁLCULO CORRIGIDO** para aumento
                            fold_change = modified_usage / original_usage
                            difference_str = f"+{fold_change:.1f}x"
                        else:
                            difference_str = "(=)"
                    elif original_usage > 0 and modified_usage == 0:
                        difference_str = "(Uso eliminado)"
                    elif original_usage == 0 and modified_usage > 0:
                        difference_str = "(Uso introduzido)"


                    change_description = (
                        f"Posição {i+1}: '{original_codon_dna}' (uso: {original_usage}) -> "
                        f"'{modified_codon_dna}' (uso: {modified_usage}) = {difference_str}"
                    )
                    changes_found.append(change_description)
                    modified_seq_h = highlight_changes(modified_seq, original_seq)
            # A estrutura de saída agora contém TODAS as informações relevantes
            analyzed_pair = {
                'dna': modified_seq_h,
                'modifications': modification_count, # Mantém a contagem
                'changes': changes_found             # Adiciona a análise de códons
            }
            gRNA_analysis_list.append(analyzed_pair)
        
        analysis_results[gRNA] = gRNA_analysis_list
        
    return analysis_results
#REVISAR ESSA FUNÇÂO ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^





#ANTIGO
#BASIC FUNCTION ===========================================================================
def translate(seq, codon_table):
    protein = ''
    for i in range(0, len(seq), 3):
        codon = seq[i:i+3]
        amino_acid = codon_table.get(codon, 'X')  # 'X' para códons desconhecidos
        protein += amino_acid
    return protein

def find_last_shared_base(seq1, seq2):
    """Encontra a última posição onde as sequências são iguais"""
    if not seq1 or not seq2:
        return None
    for i in range(min(len(seq1), len(seq2))):
        if seq1[i].upper() != seq2[i].upper():
            return i  # Retorna a posição (base 0)
    return min(len(seq1), len(seq2)) - 1  # Todas as bases comparadas são iguais

def select_nucleotides_around(seq, snp_position, x=1):
    pos_index = snp_position - 1
    codon_frame = pos_index % 3
    start = max(0, pos_index - codon_frame - (3 * (x - 1)))
    end = min(len(seq), pos_index + (3 - codon_frame) + (3 * x))
    return seq[start:end]

#ENCONTRAR SITIO DE RESTRIÇÃO PRÒXIMO DO SNP =====================================================
def expand_degenerate_site(pattern):
    iupac = {
        'N': ['A', 'T', 'C', 'G'],
        'R': ['A', 'G'],
        'Y': ['C', 'T'],
        'S': ['G', 'C'],
        'W': ['A', 'T'],
        'K': ['G', 'T'],
        'M': ['A', 'C'],
        'B': ['C', 'G', 'T'], 
        'D': ['A', 'G', 'T'],
        'H': ['A', 'C', 'T'],
        'V': ['A', 'C', 'G'],
    }
    expanded = []
    for base in pattern:
        if base in iupac:
            expanded.append(iupac[base])
        else:
            expanded.append([base.upper()])
    return [''.join(comb) for comb in product(*expanded)]


## MAIS ANTIGO
def find_rs(sequence, enzymes):
    sequence = sequence.upper()
    sites_found = []
    for enz, info in enzymes.items():
        pattern = info[0]
        cut_pos_1 = info[1]
        cut_pos_2 = info[2]
        palindromic = info[3]
        all_patterns = expand_degenerate_site(pattern)
        for variant in all_patterns:
            start = 0
            while True:
                pos = sequence.find(variant, start)
                if pos == -1:
                    break
                sites_found.append((enz, variant, pattern, pos + 1, pos + len(variant), pos+cut_pos_1 + 1, pos + cut_pos_2 + 1))
                start = pos + 1  # Para encontrar próximas ocorrências
    return sites_found

def filter_common_sites(variations_list, reference_list):
    ref_sites = {(item[0], item[5], item[6]) for item in reference_list}
    filtered = []
    for item in variations_list:
        site_key = (item[0], item[5], item[6])  # enz, cut5, cut3
        if site_key not in ref_sites:
            filtered.append(item)
    return filtered

def filter_common_sites_revcomp(variations_list, reference_list):
    enzymes_in_forward = {item[0] for item in variations_list}
    filtered = [
        item for item in reference_list
        if item[0] not in enzymes_in_forward
    ]
    return filtered

#GERAR DONOR COM SITIO DE RESTRIÇÃO PRÒXIMO DO SNP ===============================================
def get_synonymous_codons(target_aa):
    return [codon for codon, aa in codon_table.items() if aa == target_aa]

def split_into_codons(dna_sequence):
    return [dna_sequence[i:i+3] for i in range(0, len(dna_sequence), 3)]

def generate_synonymous_variations(dna_sequence, window_size=15, step=3):
    if len(dna_sequence) < window_size:
        return []
    variations = set()
    total_codons = window_size // 3
    for i in range(0, len(dna_sequence) - window_size + 1, step):
        window = dna_sequence[i:i+window_size]
        if len(window) % 3 != 0:
            continue
        codons = [window[j:j+3] for j in range(0, window_size, 3)]
        amino_acids = [codon_table.get(codon, 'X') for codon in codons]
        synonymous_options = [get_synonymous_codons(aa) for aa in amino_acids]
        window_variations = [''.join(comb) for comb in product(*synonymous_options)]
        for var in window_variations:
            new_seq = dna_sequence[:i] + var + dna_sequence[i+window_size:]
            variations.add(new_seq)
    return variations

def find_rs_in_variations(variant_list, input_seq, enzymes):
    results = []
    for seq in variant_list:
        snps = sum(1 for a, b in zip(seq, input_seq) if a != b)
        sites = find_rs(seq, enzymes)
        for site in sites:
            results.append(site + (seq, snps)) # ((enz, variant, pattern, pos + 1, pos + len(variant), pos+cut_pos_1 + 1, pos + cut_pos_2 + 1, seq, snps))
    return results

def filter_by_snp_range(variations_list, min_snps=0, max_snps=1):
    return [item for item in variations_list if min_snps <= item[8] <= max_snps]

def filter_min_snp_variants(data):
    filtered = {}
    for item in data:
        enzyme = item[0]
        cut1 = item[5]
        cut2 = item[6]
        snps = item[-1]
        key = (enzyme, cut1, cut2)

        # Guarda somente a menor variação de SNPs por chave
        if key not in filtered or snps < filtered[key][-1]:
            filtered[key] = item

    return list(filtered.values())

#TRABALHANDO COM CODON USAGE ====================================================================
def get_codon_usage(codon_usage, codon1, codon2):
    codon1 = codon1.replace('T', 'U')
    codon2 = codon2.replace('T', 'U')
    usage1 = codon_usage.get(codon1)
    usage2 = codon_usage.get(codon2)
    return usage1, usage2

def find_changed_codons(seq1, seq2, codon_usage):
    if len(seq1) != len(seq2):
        raise ValueError("Sequences must be of equal length")
    changed_codons = []
    for i in range(0, len(seq1), 3):
        codon1 = seq1[i:i+3]
        codon2 = seq2[i:i+3]
        usage1, usage2 = get_codon_usage(codon_usage, codon1, codon2)
        if codon1 != codon2:
            changed_codons.append((i // 3 + 1, codon1, codon2, usage1, usage2))
    return changed_codons

def dna_to_rna(dna_seq):
    return dna_seq.replace('T', 'U')

def rna_to_dna(dna_seq):
    return dna_seq.replace('U', 'T')

def analyze_codon_usage_differences(ref_seq, variant_data, codon_usage):
    results = []
    ref_rna = dna_to_rna(ref_seq)

    for entry in variant_data:
        enzima, ref_site, mut_site, _, _, _, _, variant_seq, _ = entry
        variant_rna = dna_to_rna(variant_seq)

        try:
            changes = find_changed_codons(ref_rna, variant_rna, codon_usage)
            enriched_changes = []

            for codon_pos, ref_codon, var_codon, ref_usage, var_usage in changes:
                if ref_usage is not None and var_usage is not None and ref_usage != 0:
                    ratio = var_usage / ref_usage
                    if ratio >= 1:
                        fator = round(ratio, 2)  # Ex: +1.95x
                    else:
                        fator = round(-1 / ratio, 2)  # Ex: -1.76x
                else:
                    fator = None

                enriched_changes.append({
                    'codon_pos': codon_pos,
                    'ref_codon': rna_to_dna(ref_codon),
                    'var_codon': rna_to_dna(var_codon),
                    'ref_usage': ref_usage,
                    'var_usage': var_usage,
                    'usage_factor': fator
                })

            results.append({
                'enzima': enzima,
                'mut_site': mut_site,
                'variant_seq': variant_seq,
                'codon_changes': enriched_changes
            })

        except ValueError as e:
            results.append({
                'enzima': enzima,
                'mut_site': mut_site,
                'variant_seq': variant_seq,
                'error': str(e)
            })

    return results   

#BUSCAR dCAPS ORIGINAIS COM 1 BASE ==============================================================
degenerate_bases = {
        'A': 'A', 'T': 'T', 'C': 'C', 'G': 'G',
        'R': '[AG]', 'Y': '[CT]', 'S': '[GC]',
        'W': '[AT]', 'K': '[GT]', 'M': '[AC]',
        'B': '[CGT]', 'D': '[AGT]', 'H': '[ACT]',
        'V': '[ACG]', 'N': '[ATCG]'
    }

def generate_degenerate_enzymes(enzymes_dict):
    """Gera variações degeneradas para todas as enzimas no dicionário."""
    degenerate_enzymes = {}
    for enzyme, data in enzymes_dict.items():
        pattern, cut5, cut3,palindromic = data
        variations = []
        for i in range(len(pattern)):
            # Substitui cada posição por 'N' (exceto bases já degeneradas)
            if pattern[i] not in {'N'}:
                new_pattern = pattern[:i] + 'N' + pattern[i+1:]
                variations.append(new_pattern)
        # Adiciona o padrão original + variações
        degenerate_enzymes[enzyme] = [[pattern, cut5, cut3,palindromic]] + variations
    return degenerate_enzymes

def find_drs(sequence, enzymes_dict):
    results = []
    seq_upper = sequence.upper()
    for enzyme_name, patterns in enzymes_dict.items():
        original_data = patterns[0]  # [sequência, cut5, cut3]
        original_pattern = original_data[0]
        original_cut5 = original_data[1]
        original_cut3 = original_data[2]
        original_regex = re.compile(''.join([degenerate_bases.get(char, char) for char in original_pattern]))
        positions_checked = set()
        for match in original_regex.finditer(seq_upper):
            start = match.start()
            site_found = match.group()
            positions_checked.add(start)
            results.append([
                enzyme_name,
                original_pattern,
                site_found,
                start + 1,
                start + len(original_pattern),
                start + original_cut5 + 1,
                start + original_cut3 + 1,
                0,
                0
            ])
        for degenerate_pattern in patterns[1:]:
            regex = re.compile(''.join([degenerate_bases.get(char, char) for char in degenerate_pattern]))  
            for match in regex.finditer(seq_upper):
                start = match.start()
                if start not in positions_checked:
                    site_found = match.group()
                    positions_checked.add(start)
                    variant_pos_1 = 0
                    variant_pos_2 = 0
                    variant_count = 0
                    for i, (orig_char, deg_char) in enumerate(zip(original_pattern, degenerate_pattern)):
                        if deg_char in degenerate_bases and orig_char != deg_char:
                            variant_count += 1
                            if variant_count == 1:
                                variant_pos_1 = start + i + 1
                            elif variant_count == 2:
                                variant_pos_2 = start + i + 1
                    results.append([
                        enzyme_name,
                        original_pattern,
                        site_found,
                        start + 1,
                        start + len(original_pattern),
                        start + original_cut5 + 1,
                        start + original_cut3 + 1,
                        variant_pos_1,
                        variant_pos_2
                    ])
    return results

def generate_primer(input_seq, snp_position, drs_item, direction):
    pattern = drs_item[1]       # Ex: CTNAG
    real_seq = drs_item[2]      # Ex: CGAAG
    start_site = drs_item[3]    # Ex: 13
    variant1 = drs_item[7]      # Ex: 14
    variant2 = drs_item[8]      # Ex: 0
    start_index = start_site - 1
    end_index = start_index + len(real_seq)
    modified_seq = input_seq[:start_index] + pattern + input_seq[end_index:]
    corrected_seq = list(modified_seq)
    for i in range(len(corrected_seq)):
        if corrected_seq[i] not in {'A', 'C', 'T', 'G'}:
            corrected_seq[i] = input_seq[i]
    modified_seq = ''.join(corrected_seq)
    if direction == "forward":
        if variant2 == 0 and variant1 < snp_position:
            return modified_seq[:snp_position - 1]
        elif variant2 != 0 and variant2 < snp_position:
            return modified_seq[:snp_position - 1]
    elif direction == "reverse":
        if variant2 == 0 and variant1 > snp_position:
            return rev_comp(modified_seq[snp_position: - 1])
        elif variant2 != 0 and variant2 > snp_position:
            return rev_comp(modified_seq[snp_position: - 1])
    return None

def filter_intermediate_snps(sites_list, snp_position):
    filtered = []
    for site in sites_list:
        var1 = site[7]  # Penúltimo item = variante1
        var2 = site[8]  # Último item = variante2
        if var2 == 0 or not (var1 < snp_position < var2):
            filtered.append(site)
    return filtered



#BUSCAR dCAPS ORIGINAIS COM 2 BASES ==============================================================
def generate_double_degenerate_enzymes(enzymes_dict):
    degenerate_enzymes = {}
    for enzyme, data in enzymes_dict.items():
        pattern, cut5, cut3, palindromic = data
        variations = []
        length = len(pattern)
        positions = range(length)
        for i, j in combinations(positions, 2):
            # Pula se alguma das posições já for degenerada
            if pattern[i] in {'N'} or pattern[j] in {'N'}:
                continue
            new_pattern = list(pattern)
            new_pattern[i] = 'N'
            new_pattern[j] = 'N'
            variations.append(''.join(new_pattern))
        degenerate_enzymes[enzyme] = [[pattern, cut5, cut3, palindromic]] + variations
    return degenerate_enzymes


@app.route('/')
@login_required
def index():
    return render_template('index.html', enzymes=enzymes)


@app.route('/results', methods=['POST'])
@login_required
def results():
    try:
        #TRATANDO AS ENZIMAS ====================================================
        # Obter enzimas selecionadas em forma de lista
        selected_enzymes_list = request.form.getlist('enzymes')

        # Preparar informações das enzimas selecionadas (usando a nova estrutura)
        enzymes_info = []
        for enzyme_name in selected_enzymes_list:
            if enzyme_name in enzymes:
                seq, cut5, cut3, palindromic = enzymes[enzyme_name]
                enzymes_info.append({'name': enzyme_name,'sequence': seq,'cut_5': cut5,'cut_3': cut3,'palindromic': palindromic})
        
        # Obter enzimas selecionadas em forma de dictionary
        selected_enzymes = {e['name']: (e['sequence'], e['cut_5'], e['cut_3'], e['palindromic']) for e in enzymes_info}
        selected_enzymes_np = {name: data for name, data in selected_enzymes.items() if data[-1] == 'np'}
        # ====================================================

        # Recuperar a escolha do organismo
        organism_selected = request.form.get('organism', 'Yeast')
        codon_usage = codon_usage_tables.get(organism_selected, codon_usage_yeast)

        input_seq_1 = request.form.get("input_seq_1", "AGATGTCAAAAGGCTTGTGACCAAATGTGGAGAATCCTTATTGGGTTGGGTACCGGTCTAAGGTTGGCATGTTTGTATTTCAGATTAACTATTCCAGAA").upper().replace(" ", "")
        input_seq_2 = request.form.get("input_seq_2", "AGATGTCAAAAGGCTTGTGACCAAATGTGGAGAATCCTTATTGGGTTGGGTACCGTTCTAAGGTTGGCATGTTTGTATTTCAGATTAACTATTCCAGAA").upper().replace(" ", "")

        # Validação
        if not re.fullmatch(r"[ATCG]+", input_seq_1):
            return jsonify({"error": "Sequence 1 must contain only A, T, C or G."}), 400
        if len(input_seq_1) > 100:
            return jsonify({"error": "Sequence 1 is too long. Max = 100bp."}), 400

        if not re.fullmatch(r"[ATCG]+", input_seq_2):
            return jsonify({"error": "Sequence 2 must contain only A, T, C or G."}), 400
        if len(input_seq_2) > 100:
            return jsonify({"error": "Sequence 2 is too long. Max = 100bp."}), 400
        '''
        if input_seq_1 == input_seq_2:
            return jsonify({"error": "Sequences must be different."}), 400
        differences = sum(1 for a, b in zip(input_seq_1, input_seq_2) if a != b)

        if differences != 1:
            return jsonify({"error": "Sequences must differ by exactly 1 SNP."}), 400
        '''

        input_seq_1_h = highlight_changes(input_seq_1, input_seq_2)
        input_seq_2_h = highlight_changes(input_seq_2, input_seq_1)

        input_seq_1_rc = rev_comp(input_seq_1)
        input_seq_2_rc = rev_comp(input_seq_2)
        input_seq_1_rc_h = highlight_changes(input_seq_1_rc, input_seq_2_rc)
        input_seq_2_rc_h = highlight_changes(input_seq_2_rc, input_seq_1_rc)

        protein_1 = translate(input_seq_1, codon_table)
        protein_2 = translate(input_seq_2, codon_table)
        protein_1_h = highlight_changes(protein_1, protein_2)
        protein_2_h = highlight_changes(protein_2, protein_1)

        max_mismatch = request.form.get("max_mismatch", 2)  # valor padrão: 2
        try:
            max_mismatch = int(max_mismatch)
        except ValueError:
            max_mismatch = 2  # fallback de segurança

        seq_1_r = ""
        seq_2_r = ""
        seq_1_r_rc = ""
        seq_2_r_rc = ""
        snp_r_s1 = ""
        snp_r_s2 = ""
        protein_1r = ""
        protein_2r = ""
        rs_s1_r = ""
        rs_s2_r = ""
        rs_s1_r_rc = ""
        rs_s2_r_rc = ""
        rs_filtered_r_s1 = ""
        rs_filtered_r_s2 = ""
        unique_rs_r_s1 = ""
        unique_rs_r_s2 = ""
        primers_r_s1 = ""
        primers_r_s2 = ""
        validated_primers_r_s1 = ""
        validated_primers_r_s2 = ""
        lista_final_r_s1 = ""
        lista_final_r_s2 = ""
        rs_filtered_r_s1_rc = ""
        rs_filtered_r_s2_rc = ""
        unique_rs_r_s1_rc = ""
        unique_rs_r_s2_rc = ""
        primers_r_s1_rc = ""
        primers_r_s2_rc = ""
        validated_primers_r_s1_rc = ""
        validated_primers_r_s2_rc = ""
        lista_final_r_s1_rc = ""
        lista_final_r_s2_rc = ""
        lista_final_final_r_s1 = ""
        lista_final_final_r_s2 = ""


        #CONFIRMAR SE TUDO ESTÁ FUNCIONANDO NA SEQ2 PQ NÃO PARECE ESTAR

        snp_left_s1, bl1, snp_left_s2, bl2, snp_right_s1, br1, snp_right_s2, br2 = get_snp_positions(input_seq_1,input_seq_2)

        #REVCOMP
        snp_left_s1_rc, bl1_rc, snp_left_s2_rc, bl2_rc,snp_right_s1_rc, br1_rc, snp_right_s2_rc, br2_rc = get_snp_positions(input_seq_1_rc,input_seq_2_rc)

        # TRABAHANDO COM A SEQUENCIA PRÓXIMA DO SNP LEFT
        seq_1_l = select_nucleotides_around(input_seq_1, snp_left_s1 , 20)
        seq_2_l = select_nucleotides_around(input_seq_2, snp_left_s2 , 20)
        seq_1_l_rc = rev_comp(seq_1_l)
        seq_2_l_rc = rev_comp(seq_2_l)
        protein_1l = translate(seq_1_l, codon_table)
        protein_2l = translate(seq_2_l, codon_table)

        snp_l_s1, _, snp_l_s2, _, _, _, _, _ = get_snp_positions(seq_1_l,seq_2_l)

        rs_s1_l = find_rs_new(seq_1_l, selected_enzymes, max_mismatch=max_mismatch)
        rs_s2_l = find_rs_new(seq_2_l, selected_enzymes, max_mismatch=max_mismatch)

        rs_s1_l_rc = find_rs_new(seq_1_l_rc, selected_enzymes_np, max_mismatch=max_mismatch)
        rs_s2_l_rc = find_rs_new(seq_2_l_rc, selected_enzymes_np, max_mismatch=max_mismatch)

        rs_filtered_l_s1 = filter_rs(rs_s1_l, snp_l_s1)
        rs_filtered_l_s2 = filter_rs(rs_s2_l, snp_l_s2)

        unique_rs_l_s1 = find_unique_rs(rs_filtered_l_s1, rs_filtered_l_s2)
        unique_rs_l_s2 = find_unique_rs(rs_filtered_l_s2, rs_filtered_l_s1)

         # FAZER O MESMO PARA O LADO DIREITO
        natural_rs_s1_l = [item for item in unique_rs_l_s1 if item[5] == 0 ]
        natural_rs_s2_l = [item for item in unique_rs_l_s2 if item[5] == 0 ]
        
        primers_l_s1 = design_primers_dcaps_seq(seq_1_l, seq_2_l, unique_rs_l_s1, snp_l_s1)
        primers_l_s2 = design_primers_dcaps_seq(seq_2_l, seq_1_l, unique_rs_l_s2, snp_l_s2)

        validated_primers_l_s1 = valid_primers(primers_l_s1)
        validated_primers_l_s2 = valid_primers(primers_l_s2)

        lista_final_l_s1 = get_final_primers(validated_primers_l_s1, seq_1_l)
        lista_final_l_s2 = get_final_primers(validated_primers_l_s2, seq_2_l)

        #para rev-comp usando as enzimas não palindromicas
        snp_l_s1_rc, _, snp_l_s2_rc, _,_, _, _, _ = get_snp_positions(seq_1_l_rc,seq_2_l_rc)

        rs_filtered_l_s1_rc = filter_rs(rs_s1_l_rc, snp_l_s1_rc)
        rs_filtered_l_s2_rc = filter_rs(rs_s2_l_rc, snp_l_s2_rc)

        unique_rs_l_s1_rc = find_unique_rs(rs_filtered_l_s1_rc, rs_filtered_l_s2_rc)
        unique_rs_l_s2_rc = find_unique_rs(rs_filtered_l_s2_rc, rs_filtered_l_s1_rc)

        natural_rs_s1_l_rc = [item for item in unique_rs_l_s1_rc if item[5] == 0 ]
        natural_rs_s2_l_rc = [item for item in unique_rs_l_s2_rc if item[5] == 0 ]

        natural_rs_s1_l_final = natural_rs_s1_l + natural_rs_s1_l_rc
        natural_rs_s2_l_final = natural_rs_s2_l + natural_rs_s2_l_rc

        primers_l_s1_rc = design_primers_dcaps_seq(seq_1_l_rc, seq_2_l_rc, unique_rs_l_s1_rc, snp_l_s1_rc)
        primers_l_s2_rc = design_primers_dcaps_seq(seq_2_l_rc, seq_1_l_rc, unique_rs_l_s2_rc, snp_l_s2_rc)

        validated_primers_l_s1_rc = valid_primers(primers_l_s1_rc)
        validated_primers_l_s2_rc = valid_primers(primers_l_s2_rc)

        lista_final_l_s1_rc = get_final_primers_rc(validated_primers_l_s1_rc, seq_1_l_rc)
        lista_final_l_s2_rc = get_final_primers_rc(validated_primers_l_s2_rc, seq_2_l_rc)

        lista_final_final_l_s1 = lista_final_l_s1 + lista_final_l_s1_rc
        lista_final_final_l_s2 = lista_final_l_s2 + lista_final_l_s2_rc

        #GERAR SNP NO DONOR Left
        # A linha de código para filtrar a lista
        rs_s2_l_1m = [item for item in rs_s2_l if item[5] == 1]
        rs_s2_l_1m_rc = [item for item in rs_s2_l_rc if item[5] == 1]

        # Gera as sequências modificadas
        grs_s2_l = generate_modified_sequences(seq_2_l, rs_s2_l_1m)
        grs_s2_l_rc = generate_modified_sequences(seq_2_l_rc, rs_s2_l_1m_rc)
        grs_s2_l_t = [(item[0], item[1], item[2], item[3],item[4], translate(item[4],codon_table)) for item in grs_s2_l]
        grs_s2_l_rc_t = [(item[0], item[1], len(item[4])-item[3], len(item[4])-item[2],rev_comp(item[4]), translate(rev_comp(item[4]),codon_table)) for item in grs_s2_l_rc]
        grs_s2_l_final = grs_s2_l_t + grs_s2_l_rc_t
        grs_s2_l_final_final = [item for item in grs_s2_l_final if item[5] == protein_2l]
        grs_s2_l_final_final_cu = get_codon_changes(seq_2_l, grs_s2_l_final_final, codon_usage)


        #GRNAS E PAMS
        gRNA_input_string = request.form.get('gRNAs', 'CAAATGTGGAGAATCCTTAT, AAATGTGGAGAATCCTTATT, CAAACATGCCAACCTTAGAC, GTTGGGTACCGGTCTAAGGT, TTGGGTTGGGTACCGGTCTA').upper().replace(" ", "")
        # Validação
        if not re.fullmatch(r"[ATCG,]+", gRNA_input_string):
            return jsonify({"error": "gRNAs must contain only A, T, C or G."}), 400
        if len(gRNA_input_string) > 220:
            return jsonify({"error": "Too much sequences. Max = 10."}), 400



        gRNAs = [g.strip().upper() for g in gRNA_input_string.split(',')]
        p_s1_l = find_pam_for_grnas(seq_1_l, gRNAs)
        hp_s1_l = generate_and_translate_synonymous_variations(seq_1_l, p_s1_l, codon_table)
        hp_s1_l_filter = filter_by_protein(hp_s1_l, protein_1l)
        hp_s1_l_filter_final = count_and_sort_modifications(seq_1_l, hp_s1_l_filter)
        hp_s1_l_filter_final_cu = analyze_codon_changes(seq_1_l, hp_s1_l_filter_final, codon_usage)
        

        if snp_left_s1 == snp_right_s1 == snp_left_s2 == snp_right_s2:
            right_snp = False
        else:

            right_snp= True
            seq_1_r_rc = select_nucleotides_around(input_seq_1_rc, snp_left_s1_rc , 10)
            seq_2_r_rc = select_nucleotides_around(input_seq_2_rc, snp_left_s2_rc , 10)
            seq_1_r = rev_comp(seq_1_r_rc)
            seq_2_r = rev_comp(seq_2_r_rc)

            protein_1r = translate(seq_1_r, codon_table)
            protein_2r = translate(seq_2_r, codon_table)

            snp_r_s1a, _, snp_r_s2a, _, _, _, _, _ = get_snp_positions(seq_1_r_rc,seq_2_r_rc)
            snp_r_s1 = len(seq_1_r) - snp_r_s1a + 1
            snp_r_s2 = len(seq_2_r) - snp_r_s2a + 1

            rs_s1_r = find_rs_new(seq_1_r, selected_enzymes, max_mismatch=max_mismatch)
            rs_s2_r = find_rs_new(seq_2_r, selected_enzymes, max_mismatch=max_mismatch)

            rs_s1_r_rc = find_rs_new(seq_1_r_rc, selected_enzymes_np, max_mismatch=max_mismatch)
            rs_s2_r_rc = find_rs_new(seq_2_r_rc, selected_enzymes_np, max_mismatch=max_mismatch)

            rs_filtered_r_s1 = filter_rs(rs_s1_r, snp_r_s1)
            rs_filtered_r_s2 = filter_rs(rs_s2_r, snp_r_s2)
            unique_rs_r_s1 = find_unique_rs(rs_filtered_r_s1, rs_filtered_r_s2)
            unique_rs_r_s2 = find_unique_rs(rs_filtered_r_s2, rs_filtered_r_s1)
            primers_r_s1 = design_primers_dcaps_seq(seq_1_r, seq_2_r, unique_rs_r_s1, snp_r_s1)
            primers_r_s2 = design_primers_dcaps_seq(seq_2_r, seq_1_r, unique_rs_r_s2, snp_r_s2)
            validated_primers_r_s1 = valid_primers(primers_r_s1)
            validated_primers_r_s2 = valid_primers(primers_r_s2)
            lista_final_r_s1 = get_final_primers(validated_primers_r_s1, seq_1_r)
            lista_final_r_s2 = get_final_primers(validated_primers_r_s2, seq_2_r)
            
            _, _, _, _, snp_r_s1_rc, _, snp_r_s2_rc, _ = get_snp_positions(seq_1_r_rc,seq_2_r_rc)
            #REVCOMP
            rs_filtered_r_s1_rc = filter_rs(rs_s1_r_rc, snp_r_s1_rc)
            rs_filtered_r_s2_rc = filter_rs(rs_s2_r_rc, snp_r_s2_rc)
            unique_rs_r_s1_rc = find_unique_rs(rs_filtered_r_s1_rc, rs_filtered_r_s2_rc)
            unique_rs_r_s2_rc = find_unique_rs(rs_filtered_r_s2_rc, rs_filtered_r_s1_rc)
            primers_r_s1_rc = design_primers_dcaps_seq(seq_1_r_rc, seq_2_r_rc, unique_rs_r_s1_rc, snp_r_s1_rc)
            primers_r_s2_rc = design_primers_dcaps_seq(seq_2_r_rc, seq_1_r_rc, unique_rs_r_s2_rc, snp_r_s2_rc)
            validated_primers_r_s1_rc = valid_primers(primers_r_s1_rc)
            validated_primers_r_s2_rc = valid_primers(primers_r_s2_rc)
            lista_final_r_s1_rc = get_final_primers_rc(validated_primers_r_s1_rc, seq_1_r_rc)
            lista_final_r_s2_rc = get_final_primers_rc(validated_primers_r_s2_rc, seq_2_r_rc)
            
            lista_final_final_r_s1 = lista_final_r_s1 + lista_final_r_s1_rc
            lista_final_final_r_s2 = lista_final_r_s2 + lista_final_r_s2_rc







        
        

        input_seq_1_revcomp = rev_comp(input_seq_1)
        input_seq_2_revcomp = rev_comp(input_seq_2)

        seq_1_lfw_30 = select_nucleotides_around(input_seq_1, (find_last_shared_base(input_seq_1, input_seq_2)+1), 5)
        seq_1_lrc_30 = rev_comp(seq_1_lfw_30)
        seq_2_lfw_30 = select_nucleotides_around(input_seq_2, (find_last_shared_base(input_seq_1, input_seq_2)+1), 5)
        seq_2_lrc_30 = rev_comp(seq_2_lfw_30)

        seq_1_rrc_30 = select_nucleotides_around(input_seq_1_revcomp, (find_last_shared_base(input_seq_1_revcomp, input_seq_2_revcomp)+1), 5)
        seq_1_rfw_30 = rev_comp(seq_1_rrc_30)            
        seq_2_rrc_30 = select_nucleotides_around(input_seq_2_revcomp, (find_last_shared_base(input_seq_1_revcomp, input_seq_2_revcomp)+1), 5)
        seq_2_rfw_30 = rev_comp(seq_2_rrc_30)

        
        

        # <Talvez isso não sirva pra nada>
        # Análise de SNP Left
        snp_position_l = None
        snp_position_l = find_last_shared_base(input_seq_1, input_seq_2)
        snp_position_left = {
            'position': snp_position_l + 1,  # Convertendo para base 1
            'base_seq1': input_seq_1[snp_position_l] if snp_position_l < len(input_seq_1) else '-',
            'base_seq2': input_seq_2[snp_position_l] if snp_position_l < len(input_seq_2) else '-'
        }

        # Análise de SNP Right
        snp_position_r = None
        snp_position_r = find_last_shared_base(input_seq_1_revcomp, input_seq_2_revcomp)
        snp_position_right = {
            'position': snp_position_r + 1,  # Convertendo para base 1
            'base_seq1': input_seq_1_revcomp[snp_position_r] if snp_position_r < len(input_seq_1_revcomp) else '-',
            'base_seq2': input_seq_2_revcomp[snp_position_r] if snp_position_r < len(input_seq_2_revcomp) else '-'
        }

        # Análise de SNP Left 30
        snp_position_l_30 = None
        snp_position_l_30 = find_last_shared_base(seq_1_lfw_30, seq_2_lfw_30)
        snp_position_left_30 = {
            'position': snp_position_l_30 + 1,  # Convertendo para base 1
            'base_seq1': seq_1_lfw_30[snp_position_l_30] if snp_position_l_30 < len(seq_1_lfw_30) else '-',
            'base_seq2': seq_2_lfw_30[snp_position_l_30] if snp_position_l_30 < len(seq_2_lfw_30) else '-'
        }

        # Análise de SNP Right 30
        snp_position_r_30 = None
        snp_position_r_30 = find_last_shared_base(seq_1_rrc_30, seq_2_rrc_30)
        snp_position_right_30 = {
            'position': snp_position_r_30 + 1,  # Convertendo para base 1
            'base_seq1': seq_1_rrc_30[snp_position_r_30] if snp_position_r_30 < len(seq_1_rrc_30) else '-',
            'base_seq2': seq_2_rrc_30[snp_position_r_30] if snp_position_r_30 < len(seq_2_rrc_30) else '-'
        }
        # </Talvez isso não sirva pra nada>


        # Obter enzimas selecionadas em forma de lista
        selected_enzymes_list = request.form.getlist('enzymes')

       
        # Preparar informações das enzimas selecionadas (usando a nova estrutura)
        enzymes_info = []
        for enzyme_name in selected_enzymes_list:
            if enzyme_name in enzymes:
                seq, cut5, cut3, palindromic = enzymes[enzyme_name]
                enzymes_info.append({
                    'name': enzyme_name,
                    'sequence': seq,
                    'cut_5': cut5,
                    'cut_3': cut3,
                    'palindromic': palindromic
                })
        '''
        ALTERNATIVA COMPACTA
        enzymes_info = []
            for enzyme_name in selected_enzymes_list:
                if enzyme_name in enzymes:
                    seq, cut5, cut3 = enzymes[enzyme_name]
                    enzymes_info.append([enzyme_name, seq, cut5, cut3])

        ou
         #aqui fica em ordem aleatória
        enzymes_info = [
            [name, *enzymes[name]]
            for name in selected_enzymes_list
            if name in enzymes
        ]

        '''
        
        # Obter enzimas selecionadas em forma de dictionary
        selected_enzymes = {e['name']: (e['sequence'], e['cut_5'], e['cut_3'], e['palindromic']) for e in enzymes_info}
        
        selected_enzymes_p = {name: data for name, data in selected_enzymes.items() if data[-1] == 'p'}
        selected_enzymes_np = {name: data for name, data in selected_enzymes.items() if data[-1] == 'np'}
        

        #ENCONTRAR SITIO DE RESTRIÇÃO PRÒXIMO DO SNP ==============================================================
        rs_input_seq_1l_p = find_rs(seq_1_lfw_30, selected_enzymes_p)
        rs_input_seq_1l_np = find_rs(seq_1_lfw_30, selected_enzymes_np)
        rs_input_seq_1lrc_np = find_rs(seq_1_lrc_30, selected_enzymes_np)
        rs_input_seq_1l = rs_input_seq_1l_p + rs_input_seq_1l_np + rs_input_seq_1lrc_np
        rs_input_seq_1= rs_input_seq_1l

        rs_input_seq_2l_p = find_rs(seq_2_lfw_30, selected_enzymes_p)
        rs_input_seq_2l_np = find_rs(seq_2_lfw_30, selected_enzymes_np)
        rs_input_seq_2lrc_np = find_rs(seq_2_lrc_30, selected_enzymes_np)
        rs_input_seq_2l = rs_input_seq_2l_p + rs_input_seq_2l_np + rs_input_seq_2lrc_np
        rs_input_seq_2 = rs_input_seq_2l

        rs_input_seq_1r_p = find_rs(seq_1_rfw_30, selected_enzymes_p)
        rs_input_seq_1r_np = find_rs(seq_1_rfw_30, selected_enzymes_np)
        rs_input_seq_1rrc_np = find_rs(seq_1_rrc_30, selected_enzymes_np)
        rs_input_seq_1r = rs_input_seq_1r_p + rs_input_seq_1r_np + rs_input_seq_1rrc_np
        
        rs_input_seq_2r_p = find_rs(seq_2_rfw_30, selected_enzymes_p)
        rs_input_seq_2r_np = find_rs(seq_2_rfw_30, selected_enzymes_np)
        rs_input_seq_2rrc_np = find_rs(seq_2_rrc_30, selected_enzymes_np)
        rs_input_seq_2r = rs_input_seq_2r_p + rs_input_seq_2r_np + rs_input_seq_2rrc_np

        unique_rs_seq_l = filter_common_sites(rs_input_seq_1l,rs_input_seq_2l)
        unique_rs_seq_r = filter_common_sites(rs_input_seq_1r,rs_input_seq_1r)


        rs_input_seq_1_revcomp = find_rs(seq_1_rrc_30,selected_enzymes)
        rs_input_seq_2_revcomp = find_rs(seq_2_rrc_30,selected_enzymes)

        unique_rs_input_seq_1 = filter_common_sites(rs_input_seq_1, rs_input_seq_2)
        unique_rs_input_seq_2 = filter_common_sites(rs_input_seq_2, rs_input_seq_1)

        unique_rs_input_seq_1_revcomp = filter_common_sites(rs_input_seq_1_revcomp, rs_input_seq_2_revcomp)
        unique_rs_input_seq_2_revcomp = filter_common_sites(rs_input_seq_2_revcomp, rs_input_seq_1_revcomp)

        filtered_rs_revcomp_1 = filter_common_sites_revcomp(unique_rs_input_seq_1, unique_rs_input_seq_1_revcomp)
        real_unique_rs_input_seq_1 = unique_rs_input_seq_1 + filtered_rs_revcomp_1

        filtered_rs_revcomp_2 = filter_common_sites_revcomp(unique_rs_input_seq_2, unique_rs_input_seq_2_revcomp)
        real_unique_rs_input_seq_2 = unique_rs_input_seq_2 + filtered_rs_revcomp_2

        #GERAR DONOR COM SITIO DE RESTRIÇÃO PRÓXIMO DO SNP ==============================================================
        input_seq_2_variations = generate_synonymous_variations(seq_2_lfw_30)
        input_seq_2_variations = list(input_seq_2_variations)

        rs_seq_2_variations = find_rs_in_variations(input_seq_2_variations, seq_2_lfw_30, selected_enzymes)

        unique_rs_seq_2_variations = filter_common_sites(rs_seq_2_variations, rs_input_seq_1)
        unique_rs_seq_2_variations = filter_common_sites(rs_seq_2_variations, rs_input_seq_2)

        unique_rs_seq_2_variations_max2snps = filter_by_snp_range(unique_rs_seq_2_variations, min_snps=1, max_snps=2)

        unique_rs_seq_2_variations_max2snps_min = filter_min_snp_variants(unique_rs_seq_2_variations_max2snps)

        unique_rs_seq_2_variations_max2snps_min_codonusage = analyze_codon_usage_differences(seq_2_lfw_30, unique_rs_seq_2_variations_max2snps_min, codon_usage)



        #BUSCAR dCAPS ORIGINAIS COM 1 BASE ==============================================================
        degenerate_enzymes = generate_degenerate_enzymes(selected_enzymes)

        drs_input_seq_1 = find_drs(seq_1_lfw_30, degenerate_enzymes)
        drs_input_seq_2 = find_drs(seq_2_lfw_30, degenerate_enzymes)

        unique_drs_input_seq_1 = filter_common_sites(drs_input_seq_1, drs_input_seq_2)
        unique_drs_input_seq_2 = filter_common_sites(drs_input_seq_2, drs_input_seq_1)

        drs_input_seq_1_revcomp = find_drs(seq_1_rrc_30, degenerate_enzymes)
        drs_input_seq_2_revcomp = find_drs(seq_2_rrc_30, degenerate_enzymes)

        unique_drs_input_seq_1_revcomp = filter_common_sites(drs_input_seq_1_revcomp, drs_input_seq_2_revcomp)
        unique_drs_input_seq_2_revcomp = filter_common_sites(drs_input_seq_2_revcomp, drs_input_seq_1_revcomp)

        filtered_drs_revcomp_1 = filter_common_sites_revcomp(unique_drs_input_seq_1, unique_drs_input_seq_1_revcomp)
        real_unique_drs_input_seq_1 = unique_drs_input_seq_1 + filtered_drs_revcomp_1

        filtered_drs_revcomp_2 = filter_common_sites_revcomp(unique_drs_input_seq_2, unique_drs_input_seq_2_revcomp)
        real_unique_drs_input_seq_2 = unique_drs_input_seq_2 + filtered_drs_revcomp_2

        primers_f_list_1 = []
        for drs in real_unique_drs_input_seq_1:
            primer = generate_primer(seq_1_lfw_30, snp_position_left_30['position'], drs,"forward")
            if primer:
                primers_f_list_1.append((drs[0], primer))  # (nome da enzima, primer)

        primers_r_list_1 = []
        for drs in real_unique_drs_input_seq_1:
            primer = generate_primer(seq_1_lfw_30, snp_position_left_30['position'], drs,"reverse")
            if primer:
                primers_r_list_1.append((drs[0], primer))  # (nome da enzima, primer)

        primers_f_list_2 = []
        for drs in real_unique_drs_input_seq_2:
            primer = generate_primer(seq_2_lfw_30, snp_position_left_30['position'], drs,"forward")
            if primer:
                primers_f_list_2.append((drs[0], primer))  # (nome da enzima, primer)

        primers_r_list_2 = []
        for drs in real_unique_drs_input_seq_2:
            primer = generate_primer(seq_2_lfw_30, snp_position_left_30['position'], drs,"reverse")
            if primer:
                primers_r_list_2.append((drs[0], primer))  # (nome da enzima, primer)


        #BUSCAR dCAPS ORIGINAIS COM 2 BASES ==============================================================
        double_degenerate_enzymes = generate_double_degenerate_enzymes(selected_enzymes)

        ddrs_input_seq_1 = find_drs(seq_1_lfw_30, double_degenerate_enzymes)
        ddrs_input_seq_2 = find_drs(seq_2_lfw_30, double_degenerate_enzymes)

        ddrs_input_seq_1_revcomp = find_drs(seq_1_rrc_30, double_degenerate_enzymes)
        ddrs_input_seq_2_revcomp = find_drs(seq_2_rrc_30, double_degenerate_enzymes)

        unique_ddrs_input_seq_1 = filter_common_sites(ddrs_input_seq_1, ddrs_input_seq_2)
        unique_ddrs_input_seq_2 = filter_common_sites(ddrs_input_seq_2, ddrs_input_seq_1)

        unique_ddrs_input_seq_1_revcomp = filter_common_sites(ddrs_input_seq_1_revcomp, ddrs_input_seq_2_revcomp)
        unique_ddrs_input_seq_2_revcomp = filter_common_sites(ddrs_input_seq_2_revcomp, ddrs_input_seq_1_revcomp)

        almost_unique_ddrs_input_seq_1 = filter_intermediate_snps(unique_ddrs_input_seq_1, snp_position_left_30['position'])
        almost_unique_ddrs_input_seq_2 = filter_intermediate_snps(unique_ddrs_input_seq_2, snp_position_left_30['position'])

        almost_unique_ddrs_input_seq_1_revcomp = filter_intermediate_snps(unique_ddrs_input_seq_1_revcomp, snp_position_right_30['position'])
        almost_unique_ddrs_input_seq_2_revcomp = filter_intermediate_snps(unique_ddrs_input_seq_2_revcomp, snp_position_right_30['position'])

        filtered_ddrs_revcomp_1 = filter_common_sites_revcomp(almost_unique_ddrs_input_seq_1, almost_unique_ddrs_input_seq_1_revcomp)
        real_unique_ddrs_input_seq_1 = almost_unique_ddrs_input_seq_1 + filtered_ddrs_revcomp_1

        filtered_ddrs_revcomp_2 = filter_common_sites_revcomp(almost_unique_ddrs_input_seq_2, almost_unique_ddrs_input_seq_2_revcomp)
        real_unique_ddrs_input_seq_2 = almost_unique_ddrs_input_seq_2 + filtered_ddrs_revcomp_2

        primers_f2_list_1 = []
        for drs in real_unique_ddrs_input_seq_1:
            primer = generate_primer(seq_1_lfw_30, snp_position_left_30['position'], drs,"forward")
            if primer:
                primers_f_list_2.append((drs[0], primer))  # (nome da enzima, primer)



        return render_template('results.html',
                            input_seq_1 = input_seq_1,
                            input_seq_2 = input_seq_2,
                            input_seq_1_h =input_seq_1_h,
                            input_seq_2_h = input_seq_2_h,
                            input_seq_1_rc = input_seq_1_rc,
                            input_seq_2_rc = input_seq_2_rc,
                            input_seq_1_rc_h = input_seq_1_rc_h,
                            input_seq_2_rc_h = input_seq_2_rc_h,
                            protein_1 = protein_1,
                            protein_2 = protein_2,
                            protein_1_h = protein_1_h,
                            protein_2_h = protein_2_h,
                            snp_left_s1 = snp_left_s1,
                            max_mismatch = max_mismatch,
                            bl1 = bl1,
                            snp_left_s2 = snp_left_s2,
                            bl2 = bl2,
                            snp_right_s1 = snp_right_s1,
                            br1 = br1,
                            snp_right_s2 = snp_right_s2,
                            br2 = br2,
                            snp_left_s1_rc = snp_left_s1_rc,
                            bl1_rc = bl1_rc,
                            snp_left_s2_rc = snp_left_s2_rc,
                            bl2_rc = bl2_rc,
                            snp_right_s1_rc = snp_right_s1_rc,
                            br1_rc = br1_rc,
                            snp_right_s2_rc = snp_right_s2_rc,
                            br2_rc = br2_rc,
                            seq_1_l = seq_1_l,
                            seq_2_l = seq_2_l,
                            seq_1_l_rc = seq_1_l_rc,
                            seq_2_l_rc = seq_2_l_rc,
                            snp_l_s1 = snp_l_s1,
                            snp_l_s2 = snp_l_s2,
                            seq_1_r = seq_1_r,
                            seq_2_r = seq_2_r,
                            seq_1_r_rc = seq_1_r_rc,
                            seq_2_r_rc = seq_2_r_rc,
                            snp_r_s1 = snp_r_s1,
                            snp_r_s2 = snp_r_s2,
                            protein_1l = protein_1l,
                            protein_2l = protein_2l,
                            protein_1r = protein_1r,
                            protein_2r = protein_2r,
                            rs_s1_l = rs_s1_l,
                            rs_s2_l = rs_s2_l,
                            rs_s1_l_rc = rs_s1_l_rc,
                            rs_s2_l_rc = rs_s2_l_rc,
                            rs_filtered_l_s1 = rs_filtered_l_s1,
                            rs_filtered_l_s2 = rs_filtered_l_s2,
                            unique_rs_l_s1 = unique_rs_l_s1,
                            unique_rs_l_s2 = unique_rs_l_s2,
                            natural_rs_s1_l = natural_rs_s1_l,
                            natural_rs_s2_l = natural_rs_s2_l,
                            primers_l_s1 = primers_l_s1,
                            primers_l_s2 = primers_l_s2,
                            validated_primers_l_s1 = validated_primers_l_s1,
                            validated_primers_l_s2 = validated_primers_l_s2,
                            lista_final_l_s1 = lista_final_l_s1,
                            lista_final_l_s2 = lista_final_l_s2,
                            rs_filtered_l_s1_rc = rs_filtered_l_s1_rc,
                            rs_filtered_l_s2_rc = rs_filtered_l_s2_rc,
                            unique_rs_l_s1_rc = unique_rs_l_s1_rc,
                            unique_rs_l_s2_rc = unique_rs_l_s2_rc,
                            natural_rs_s1_l_rc = natural_rs_s1_l_rc,
                            natural_rs_s2_l_rc = natural_rs_s2_l_rc,
                            natural_rs_s1_l_final = natural_rs_s1_l_final,
                            natural_rs_s2_l_final = natural_rs_s2_l_final,
                            primers_l_s1_rc = primers_l_s1_rc,
                            primers_l_s2_rc = primers_l_s2_rc,
                            validated_primers_l_s1_rc = validated_primers_l_s1_rc,
                            validated_primers_l_s2_rc = validated_primers_l_s2_rc,
                            lista_final_l_s1_rc = lista_final_l_s1_rc,
                            lista_final_l_s2_rc = lista_final_l_s2_rc,
                            lista_final_final_l_s1 = lista_final_final_l_s1,
                            lista_final_final_l_s2 = lista_final_final_l_s2,
                            rs_s1_r = rs_s1_r,
                            rs_s2_r = rs_s2_r,
                            rs_s1_r_rc = rs_s1_r_rc,
                            rs_s2_r_rc = rs_s2_r_rc,
                            rs_filtered_r_s1 = rs_filtered_r_s1,
                            rs_filtered_r_s2 = rs_filtered_r_s2,
                            unique_rs_r_s1 = unique_rs_r_s1,
                            unique_rs_r_s2 = unique_rs_r_s2,
                            primers_r_s1 = primers_r_s1,
                            primers_r_s2 = primers_r_s2,
                            validated_primers_r_s1 = validated_primers_r_s1,
                            validated_primers_r_s2 = validated_primers_r_s2,
                            lista_final_r_s1 = lista_final_r_s1,
                            lista_final_r_s2 = lista_final_r_s2,
                            rs_filtered_r_s1_rc = rs_filtered_r_s1_rc,
                            rs_filtered_r_s2_rc = rs_filtered_r_s2_rc,
                            unique_rs_r_s1_rc = unique_rs_r_s1_rc,
                            unique_rs_r_s2_rc = unique_rs_r_s2_rc,
                            primers_r_s1_rc = primers_r_s1_rc,
                            primers_r_s2_rc = primers_r_s2_rc,
                            validated_primers_r_s1_rc = validated_primers_r_s1_rc,
                            validated_primers_r_s2_rc = validated_primers_r_s2_rc,
                            lista_final_r_s1_rc = lista_final_r_s1_rc,
                            lista_final_r_s2_rc = lista_final_r_s2_rc,
                            lista_final_final_r_s1 = lista_final_final_r_s1,
                            lista_final_final_r_s2 = lista_final_final_r_s2,
                            right_snp = right_snp,
                            rs_s2_l_1m = rs_s2_l_1m,
                            rs_s2_l_1m_rc = rs_s2_l_1m_rc,
                            grs_s2_l = grs_s2_l,
                            grs_s2_l_t =grs_s2_l_t,
                            grs_s2_l_rc = grs_s2_l_rc,
                            grs_s2_l_rc_t = grs_s2_l_rc_t,
                            grs_s2_l_final = grs_s2_l_final,
                            grs_s2_l_final_final = grs_s2_l_final_final,
                            grs_s2_l_final_final_cu = grs_s2_l_final_final_cu,
                            gRNA_input_string = gRNA_input_string,
                            gRNAs = gRNAs,
                            p_s1_l = p_s1_l,
                            hp_s1_l = hp_s1_l,
                            hp_s1_l_filter = hp_s1_l_filter,
                            hp_s1_l_filter_final = hp_s1_l_filter_final,
                            hp_s1_l_filter_final_cu = hp_s1_l_filter_final_cu,
                            organism_selected = organism_selected,

                            
                            selected_enzymes=selected_enzymes,
                            selected_enzymes_p = selected_enzymes_p,
                            selected_enzymes_np = selected_enzymes_np,
                            snp_position_l = snp_position_l,
                            snp_position_left = snp_position_left,
                            input_seq_1_revcomp = input_seq_1_revcomp,
                            input_seq_2_revcomp = input_seq_2_revcomp,
                            snp_position_r = snp_position_r,
                            snp_position_right = snp_position_right,
                            seq_1_lfw_30 = seq_1_lfw_30,
                            seq_2_lfw_30 = seq_2_lfw_30,
                            seq_1_lrc_30 = seq_1_lrc_30,
                            seq_2_lrc_30 = seq_2_lrc_30,
                            seq_1_rfw_30 = seq_1_rfw_30,
                            seq_2_rfw_30 = seq_2_rfw_30,
                            seq_1_rrc_30 = seq_1_rrc_30,
                            seq_2_rrc_30 = seq_2_rrc_30,
                            snp_position_left_30 = snp_position_left_30,
                            snp_position_right_30 = snp_position_right_30,
                            rs_input_seq_1l_p = rs_input_seq_1l_p,
                            rs_input_seq_1l_np = rs_input_seq_1l_np,
                            rs_input_seq_1lrc_np = rs_input_seq_1lrc_np,
                            rs_input_seq_1l = rs_input_seq_1l,
                            rs_input_seq_1r_p = rs_input_seq_1r_p,
                            rs_input_seq_1r_np = rs_input_seq_1r_np,
                            rs_input_seq_1rrc_np = rs_input_seq_1rrc_np,
                            rs_input_seq_1r = rs_input_seq_1r,
                            rs_input_seq_2_revcomp = rs_input_seq_2_revcomp,
                            rs_input_seq_1_revcomp = rs_input_seq_1_revcomp,
                            rs_input_seq_2l_p = rs_input_seq_2l_p,
                            rs_input_seq_2l_np = rs_input_seq_2l_np,
                            rs_input_seq_2lrc_np = rs_input_seq_2lrc_np,
                            rs_input_seq_2l = rs_input_seq_2l,
                            rs_input_seq_2r_p = rs_input_seq_2r_p,
                            rs_input_seq_2r_np = rs_input_seq_2r_np,
                            rs_input_seq_2rrc_np = rs_input_seq_2rrc_np,
                            rs_input_seq_2r = rs_input_seq_2r,
                            unique_rs_seq_l = unique_rs_seq_l,
                            unique_rs_seq_r = unique_rs_seq_r,
                            unique_rs_input_seq_1 = unique_rs_input_seq_1,
                            unique_rs_input_seq_2 = unique_rs_input_seq_2,
                            unique_rs_input_seq_1_revcomp = unique_rs_input_seq_1_revcomp,
                            unique_rs_input_seq_2_revcomp = unique_rs_input_seq_2_revcomp,
                            real_unique_rs_input_seq_1 = real_unique_rs_input_seq_1,
                            real_unique_rs_input_seq_2 = real_unique_rs_input_seq_2,
                            input_seq_2_variations = input_seq_2_variations,
                            rs_seq_2_variations = rs_seq_2_variations,
                            unique_rs_seq_2_variations = unique_rs_seq_2_variations,
                            unique_rs_seq_2_variations_max2snps = unique_rs_seq_2_variations_max2snps,
                            unique_rs_seq_2_variations_max2snps_min = unique_rs_seq_2_variations_max2snps_min,
                            unique_rs_seq_2_variations_max2snps_min_codonusage = unique_rs_seq_2_variations_max2snps_min_codonusage,
                            drs_input_seq_1 = drs_input_seq_1,
                            drs_input_seq_2 = drs_input_seq_2,
                            unique_drs_input_seq_1 = unique_drs_input_seq_1,
                            unique_drs_input_seq_2 = unique_drs_input_seq_2,
                            real_unique_drs_input_seq_1 = real_unique_drs_input_seq_1,
                            real_unique_drs_input_seq_2 = real_unique_drs_input_seq_2,
                            primers_f_list_1 = primers_f_list_1,
                            primers_r_list_1 = primers_r_list_1,
                            primers_f_list_2 = primers_f_list_2,
                            primers_r_list_2 = primers_r_list_2,
                            ddrs_input_seq_1 = ddrs_input_seq_1,
                            ddrs_input_seq_2 = ddrs_input_seq_2,
                            unique_ddrs_input_seq_1 = unique_ddrs_input_seq_1,
                            unique_ddrs_input_seq_2 = unique_ddrs_input_seq_2,
                            almost_unique_ddrs_input_seq_1 = almost_unique_ddrs_input_seq_1,
                            almost_unique_ddrs_input_seq_2 = almost_unique_ddrs_input_seq_2,
                            )
    
    except Exception as e:
        return f"Erro: {str(e)}", 500

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)

#app.run(debug=True, host='186.217.151.34')
'''
Examples for test
VPS70
TACAAACCCAAAGTTGAAAAATATTACCCATGGATAGGTGAACCAGTAGACACTAACGTAGCTCCTTTAGAAAATGGTAAAGTGGTCTACGAAGCAAGCATGATCGAGGATAGA
TACAAACCCAAAGTTGAAAAATATTACCCATGGATAGGTGAACCAGTAGACACTAACGTAGCTCTTTTAGAAAATGGTAAAGTGGTCTACGAAGCAAGCATGATCGAGGATAGA
ATGGATAGGTGAACCAGTAG

MKT1
ATGGCAATCAAGTCATTGGAATCGTTCCTTTTCGAAAGAGGTCTAGTAGGATCCTATGCCATTGAGGCTCTGAATAATTGTACCCTGGATATAGACGTCAACCATTATGTTTCCAGATTGTTGACCAATAAAAGAGA
ATGGCAATCAAGTCATTGGAATCGTTCCTTTTCGAAAGAGGTCTAGTAGGATCCTATGCCATTGAGGCTCTGAATAATTGTACCCTGGGTATAGACGTCAACCATTATGTTTCCAGATTGTTGACCAATAAAAGAGA
TCAACAATCTGGAAACATAA

PHO84
GCTGAATGTGATGCTAGATGTCAAAAGGCTTGTGACCAAATGTGGAGAATCCTTATTGGGTTGGGTACCGTTCTAGGGTTGGCATGTTTGTATTTCAGATTAACTATTCCAGAA
GCTGAATGTGATGCTAGATGTCAAAAGGCTTGTGACCAAATGTGGAGAATCCTTATTGGGTTGGGTACCGTTCCAGGGTTGGCATGTTTGTATTTCAGATTAACTATTCCAGAA
GAACGGTACCCAACCCAATA

HTA1
CAATCTAGATCTGCTAAGGCTGGTTTGACATTCCCAGTCGGTAGAGTGCACATATTGCTAAGAAGAGGTAACTACGCCCAAAGAATTGGTTCTGGTGCTCCAGTCTACTTGACTGCTGTCTTGGAATATTTGGCCGCTGAAATTTTAG
CAATCTAGATCTGCTAAGGCTGGTTTGACATTCCCAGTCGGTAGAGTGCACAGATTGCTAAGAAGAGGTAACTACGCCCAAAGAATTGGTTCTGGTGCTCCAGTCTACTTGACTGCTGTCTTGGAATATTTGGCCGCTGAAATTTTAG
AGTCTACTTGACTGCTGTCT

CAT5



CCAGTAGACACTAACGTAGCTCCTTTAGAAAATGGTAAAGTGG
CCAGTAGACACTAACGTAGCTCTTTTAGAAAATGGTAAAGTGG
'''