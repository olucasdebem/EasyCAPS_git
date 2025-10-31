#app.py

import os
import re
import bleach
from waitress import serve
from functools import wraps
from enzymes import enzymes
from aux_dict import codon_table, degenerate_bases, degenerate_bases_regex
from itertools import product, combinations
from codon_usage import codon_usage_tables, organism_names
from flask import Flask, request, render_template, jsonify, redirect, url_for, session

# --- Login
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'uma-chave-padrao-para-testes-locais')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin_test_2')

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
            return redirect(url_for('index'))
        else:
            error = 'Senha inválida. Tente novamente.'
    return render_template('login.html', error=error)

# --- Rota de Logout ---
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


VALID_PAMS = {"NGG"}

# --- BASIC FUNCTIONS ---
# pos_l_s1, base_l_s1, pos_l_s2, base_l_s2, pos_r_s1, base_r_s1, pos_r_s2, base_r_s2
def get_snp_positions(seq1, seq2):
    len1 = len(seq1)
    len2 = len(seq2)
    lcp_len, lcs_len = find_variable_region(seq1, seq2)
    if lcp_len + lcs_len >= min(len1, len2):
        return None
    pos_l_s1 = pos_l_s2 = lcp_len + 1
    base_l_s1 = seq1[lcp_len]
    base_l_s2 = seq2[lcp_len]
    pos_r_s1 = len1 - lcs_len
    base_r_s1 = seq1[pos_r_s1 - 1]
    pos_r_s2 = len2 - lcs_len
    base_r_s2 = seq2[pos_r_s2 - 1]
    return pos_l_s1, base_l_s1, pos_l_s2, base_l_s2, pos_r_s1, base_r_s1, pos_r_s2, base_r_s2
# ^^^ SHOW ^^^

#get shared nucleotides
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
# ^^^ SHOW ^^^

# highligh variable region
def highlight_variable_region(seq1, seq2):
    lcp_len, lcs_len = find_variable_region(seq1, seq2)
    prefix = seq1[:lcp_len]
    variable_region = seq1[lcp_len : len(seq1) - lcs_len]
    suffix = seq1[len(seq1) - lcs_len:]
    highlighted_variable_html = ""
    if len(variable_region) == 0:
        pass
    elif len(variable_region) == 1:
        first_char = variable_region[0]
        highlighted_variable_html = f'<span style="background-color:#ffffad;">{first_char}</span>'
    else:
        first_char = variable_region[0]
        middle = variable_region[1:-1]
        last_char = variable_region[-1]
        special_highlight = f'<span style="background-color:#ffffad;">{first_char}</span>'
        normal_highlight = f'<span style="background-color:#adff99;">{middle}</span>'
        special_highlight_end = f'<span style="background-color:#ffffad;">{last_char}</span>'     
        highlighted_variable_html = special_highlight + normal_highlight + special_highlight_end
    return prefix + highlighted_variable_html + suffix
# ^^^ SHOW ^^^

# get reverse-complement
def rev_comp(seq):
    complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C',
                  'Y':'R', 'R':'Y', 'K':'M', 'M':'K',
                  'D':'H', 'H':'D', 'V':'B', 'B':'V',
                  'W':'W', 'S':'S', 'N':'N'}
    return ''.join([complement.get(base.upper(), 'N') for base in seq[::-1]])
# ^^^ SHOW ^^^

# DNA to protein
def translate(seq, codon_table):
    protein = ''
    for i in range(0, len(seq), 3):
        codon = seq[i:i+3]
        amino_acid = codon_table.get(codon, 'X')
        protein += amino_acid
    return protein
# ^^^ SHOW ^^^

def select_nucleotides_around(seq, snp_position, x=1):
    pos_index = snp_position - 1
    codon_frame = pos_index % 3
    start_of_snp_codon = pos_index - codon_frame
    start = max(0, start_of_snp_codon - (3 * x))
    end = min(len(seq), start_of_snp_codon + 3 + (3 * x))
    return seq[start:end]
# ^^^ SHOW ^^^

def highlight_changes(modified_seq, original_seq):
    original_upper = original_seq.upper()
    modified_upper = modified_seq.upper()
    highlighted_output = ""
    if len(original_upper) != len(modified_upper):
        return modified_upper
    for i in range(len(original_upper)):
        if original_upper[i] != modified_upper[i]:
            highlighted_output += f'<span style="background-color:#ffadad">{modified_upper[i]}</span>'
        else:
            highlighted_output += original_upper[i]
    return highlighted_output

# --- MAIN FUNCTIONS FOR CAPS AND dCAPS ---
def bases_match(base1, base2, degenerate_bases):
    if base1 == base2:
        return True
    if base1 in degenerate_bases and base2 in degenerate_bases[base1]:
        return True
    if base2 in degenerate_bases and base1 in degenerate_bases[base2]:
        return True
    return False
# ^^^ SHOW ^^^

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
            for j in range(site_len):
                base_dna = dna_segment[j]
                base_enzyme = site_pattern[j]
                if not bases_match(base_dna, base_enzyme, degenerate_bases):
                    num_mismatches += 1
                    if num_mismatches > max_mismatch:
                        break
                    mismatch_pos.append(i + j + 1)
            else: 
                result_tuple = (enzyme_name, site_pattern, i + 1, i + site_len, dna_segment, num_mismatches, mismatch_pos)
                rs_info.append(result_tuple)          
    return rs_info
# ^^^ SHOW ^^^

# filter (SNP out of enzyme site) or (SNP = mismatch position) or (SNP between mismatches) 
def filter_rs(rs_seq, snp_position):
    results = []
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
        results.append(item)
    return results
# ^^^ SHOW ^^^

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
# ^^^ SHOW ^^^

def concretize_pattern(pattern_segment, dna_segment, degenerate_bases):
    concrete_str = ""
    if len(pattern_segment) != len(dna_segment):
        return pattern_segment
    for i in range(len(pattern_segment)):
        pattern_base = pattern_segment[i]
        dna_base = dna_segment[i]
        if pattern_base in degenerate_bases:
            if dna_base in degenerate_bases[pattern_base]:
                concrete_str += dna_base
            else:
                concrete_str += pattern_base
        else:
            concrete_str += pattern_base
    return concrete_str
# ^^^ SHOW ^^^

# (enzyme_name, enzyme_pattern, site_start, site_end, design_primer, test1, test2, primer_type)]
#test1 and test2 are relatives; for s1 test1~seq1, test2~seq2, but for s2 test1~seq2 and test2~seq1
def design_primers_dcaps_seq(seq1, seq2, unique_rs, snp_pos, degenerate_bases):
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
            pattern_part2 = enzyme_pattern[:snp_pos - site_start]
            dna_part2 = seq1[site_start - 1 : snp_pos - 1]
            part2 = concretize_pattern(pattern_part2, dna_part2, degenerate_bases)
            design_primer = part1 + part2
            test1 = design_primer + seq1[snp_pos_0:]
            test2 = design_primer + seq2[snp_pos_0:]
        else:
            primer_type = "Reverse"
            pattern_part1 = enzyme_pattern[snp_pos - site_start + 1 :]
            dna_part1 = seq1[snp_pos : site_end]
            part1 = concretize_pattern(pattern_part1, dna_part1, degenerate_bases)
            part2 = seq1[site_end:]
            design_primer = part1 + part2
            test1 = seq1[:snp_pos] + design_primer
            test2 = seq2[:snp_pos] + design_primer
        if design_primer: 
            results.append(
                (enzyme_name, enzyme_pattern, site_start, site_end, design_primer, test1, test2, primer_type))
    return results
# ^^^ SHOW ^^^

#if enzyme_pattern in test1 != in test2, it is a dCAPS
def valid_primers(primers, degenerate_bases_regex):
    results = []
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
            if base in degenerate_bases_regex:
                regex_pattern += degenerate_bases_regex[base]
                is_degenerate = True
            else:
                regex_pattern += base
        if is_degenerate:
            find_test1 = bool(re.search(regex_pattern, test1))
            find_test2 = bool(re.search(regex_pattern, test2))
        else:
            find_test1 = enzyme_pattern in test1
            find_test2 = enzyme_pattern in test2
        if find_test1 != find_test2:
            results.append(item)        
    return results
# ^^^ SHOW ^^^

# Natural logic
def get_final_primers(validated_primers, seq):
    results = []
    for item in validated_primers:
        enzyme_name, enzyme_pattern, site_start, site_end, design_primer, _, _, primer_type = item
        if primer_type == "Forward":
            design_primer_cut = design_primer[-25:]
            seq_raw = seq[:len(design_primer)]
            seq_cut = seq_raw[-25:]
            primer_h = highlight_changes(design_primer_cut, seq_cut)
            final_list = (enzyme_name, enzyme_pattern, site_start, site_end, design_primer, primer_type, seq_cut, primer_h)
            results.append(final_list)
        elif primer_type == "Reverse":
            seq_rc = rev_comp(seq)
            design_primer = rev_comp(design_primer)
            design_primer_cut = design_primer[-25:]
            seq_raw_rc = (seq_rc[:len(design_primer)])
            seq_cut_rc = seq_raw_rc[-25:]
            primer_h_rc = highlight_changes(design_primer_cut, seq_cut_rc)
            final_list = (enzyme_name, enzyme_pattern, site_start, site_end, design_primer, primer_type, seq_cut_rc, primer_h_rc)
            results.append(final_list)        
    return results
# ^^^ SHOW ^^^

# Rev-comp logic
def get_final_primers_rc(validated_primers, seq):
    results = []
    for item in validated_primers:
        enzyme_name, enzyme_pattern, site_start, site_end, design_primer, _, _, primer_type = item
        if primer_type == "Reverse":
            seq_rc = rev_comp(seq)
            design_primer = rev_comp(design_primer)
            design_primer_cut = design_primer[-25:]
            seq_raw_rc = (seq_rc[:len(design_primer)])
            seq_cut_rc = seq_raw_rc[-25:]
            primer_h_rc = highlight_changes (design_primer_cut, seq_cut_rc)
            final_list = (enzyme_name, enzyme_pattern, site_start, site_end, design_primer, "Forward", seq_cut_rc, primer_h_rc)
            results.append(final_list) 
        elif primer_type == "Forward":
            design_primer_cut = design_primer[-25:]
            seq_raw = seq[:len(design_primer)]
            seq_cut = seq_raw[-25:]
            primer_h = highlight_changes(design_primer_cut, seq_cut)
            final_list = (enzyme_name, enzyme_pattern, site_start, site_end, design_primer, "Reverse", seq_cut, primer_h)
            results.append(final_list)        
    return results
# ^^^ SHOW ^^^

def run_analysis_pipeline(seq_1, seq_2, enzymes, max_mismatch, degenerate_bases, is_rc_analysis=False):
            snp_data = get_snp_positions(seq_1, seq_2)
            if snp_data is None:
               return {
                'natural_sites_s1': [], 'natural_sites_s2': [],
                'final_primers_s1': [], 'final_primers_s2': [],
                'debug_info': {}
            }
            snp_s1, _, snp_s2, _, _, _, _, _ = snp_data
            rs_s1 = find_rs_new(seq_1, enzymes, max_mismatch)
            rs_s2 = find_rs_new(seq_2, enzymes, max_mismatch)
            rs_filtered_s1 = filter_rs(rs_s1, snp_s1)
            rs_filtered_s2 = filter_rs(rs_s2, snp_s2)
            unique_rs_s1 = find_unique_rs(rs_filtered_s1, rs_filtered_s2)
            unique_rs_s2 = find_unique_rs(rs_filtered_s2, rs_filtered_s1)
            natural_rs_s1 = [item for item in unique_rs_s1 if item[5] == 0]
            natural_rs_s2 = [item for item in unique_rs_s2 if item[5] == 0]
            primers_s1 = design_primers_dcaps_seq(seq_1, seq_2, unique_rs_s1, snp_s1, degenerate_bases)
            primers_s2 = design_primers_dcaps_seq(seq_2, seq_1, unique_rs_s2, snp_s2, degenerate_bases)
            validated_primers_s1 = valid_primers(primers_s1, degenerate_bases_regex)
            validated_primers_s2 = valid_primers(primers_s2, degenerate_bases_regex)
            if is_rc_analysis:
                final_primers_s1 = get_final_primers_rc(validated_primers_s1, seq_1)
                final_primers_s2 = get_final_primers_rc(validated_primers_s2, seq_2)
            else:
                final_primers_s1 = get_final_primers(validated_primers_s1, seq_1)
                final_primers_s2 = get_final_primers(validated_primers_s2, seq_2)
            results = {
                # Resultados principais
                'natural_sites_s1': natural_rs_s1,
                'natural_sites_s2': natural_rs_s2,
                'final_primers_s1': final_primers_s1,
                'final_primers_s2': final_primers_s2,
                
                # Dados intermediários para depuração ou exibição detalhada
                'debug_info': {
                    'snp_s1': snp_s1,
                    'snp_s2': snp_s2,
                    'rs_s1': rs_s1,
                    'rs_s2': rs_s2,
                    'rs_filtered_s1': rs_filtered_s1,
                    'rs_filtered_s2': rs_filtered_s2,
                    'unique_rs_s1': unique_rs_s1,
                    'unique_rs_s2': unique_rs_s2,
                    'primers_s1': primers_s1,
                    'primers_s2': primers_s2,
                    'validated_primers_s1': validated_primers_s1,
                    'validated_primers_s2': validated_primers_s2
                        }
                    }
            return results
# ^^^ SHOW ^^^

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
            output_tuple = (enzyme_name, enzyme_pattern, start_pos_1based, end_pos_1based, new_sequence)
            results.append(output_tuple)        
    return results

def get_donor(seq, enzymes, codon_table, is_rc_analysis=False):
            rs_s2 = find_rs_new(seq, enzymes, max_mismatch=1)
            rs_s2_1m = [item for item in rs_s2 if item[5] == 1]
            grs_s2 = generate_modified_sequences(seq, rs_s2_1m)
            grs_s2_t = []
            if not is_rc_analysis:
                for item in grs_s2:
                    enzyme_name, pattern, start, end, new_seq = item
                    translated_seq = translate(new_seq, codon_table)
                    grs_s2_t.append((enzyme_name, pattern, start, end, new_seq, translated_seq))
            else:
                for item in grs_s2:
                    enzyme_name, pattern, start, end, new_seq = item
                    new_seq_rc = rev_comp(new_seq)
                    start_rc = len(seq) - end + 1
                    end_rc = len(seq) - start + 1
                    translated_seq_rc = translate(new_seq_rc, codon_table)
                    grs_s2_t.append((enzyme_name, pattern, start_rc, end_rc, new_seq_rc, translated_seq_rc))
            results = {
                'grs_s2_t': grs_s2_t,
                'debug_info': {
                    'rs_s2': rs_s2,
                    'rs_s2_1m': rs_s2_1m,
                    'grs_s2': grs_s2
                }
            }
            return results

def get_codon_changes(original_seq, modified_seq_info_list, codon_usage_table):
    final_results_with_comparison = []
    for item in modified_seq_info_list:
        enzyme_name = item[0]
        enzyme_pattern = item[1]
        start_pos = item[2]
        end_pos = item[3]
        modified_seq = item[4]
        for i in range(0, len(original_seq), 3):
            original_codon_dna = original_seq[i:i+3].upper()
            modified_codon_dna = modified_seq[i:i+3].upper()
            if len(original_codon_dna) < 3 or len(modified_codon_dna) < 3:
                continue
            if original_codon_dna != modified_codon_dna:
                original_codon_rna = original_codon_dna.replace('T', 'U')
                modified_codon_rna = modified_codon_dna.replace('T', 'U')
                original_usage = codon_usage_table.get(original_codon_rna, 0.0) # Usar 0.0 para facilitar o cálculo
                modified_usage = codon_usage_table.get(modified_codon_rna, 0.0)
                difference_str = ""
                if isinstance(original_usage, (int, float)) and isinstance(modified_usage, (int, float)):
                    if original_usage > 0 and modified_usage > 0:
                        if original_usage > modified_usage:
                            fold_change = original_usage / modified_usage
                            difference_str = f"-{fold_change:.1f}x"
                        elif modified_usage > original_usage:
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

def match_degenerate(sequence, pattern):
    if len(sequence) != len(pattern):
        return False
    for i in range(len(pattern)):
        base_pattern = pattern[i]
        base_seq = sequence[i]
        if base_pattern == 'N':
            continue
        if base_pattern in degenerate_bases:
            if base_seq not in degenerate_bases[base_pattern]:
                return False
        elif base_pattern != base_seq:
            return False
    return True

def find_pam_for_grnas(target_seq, grna_list):
    results = []
    target_seq_upper = target_seq.upper()
    pam_forward_pattern = "NGG"
    pam_reverse_pattern = "CCN"
    for grna in grna_list:
        grna_upper = grna.upper()
        found = False
        for match in re.finditer(grna_upper, target_seq_upper):
            grna_pos_0b = match.start()
            pam_start_0b = grna_pos_0b + len(grna_upper)
            if pam_start_0b + len(pam_forward_pattern) <= len(target_seq_upper):
                actual_pam_seq = target_seq_upper[pam_start_0b : pam_start_0b + len(pam_forward_pattern)]
                if match_degenerate(actual_pam_seq, pam_forward_pattern):
                    results.append((grna, grna_pos_0b + 1, pam_forward_pattern, pam_start_0b + 1))
                    found = True
                    break
        if found:
            continue
        target_on_fwd = rev_comp(grna_upper)
        for match in re.finditer(target_on_fwd, target_seq_upper):
            target_pos_0b = match.start()
            pam_start_0b = target_pos_0b - len(pam_reverse_pattern)
            if pam_start_0b >= 0:
                actual_pam_seq = target_seq_upper[pam_start_0b : pam_start_0b + len(pam_reverse_pattern)]
                if match_degenerate(actual_pam_seq, pam_reverse_pattern):
                    results.append((grna, target_pos_0b + 1, pam_reverse_pattern, pam_start_0b + 1)                    )
                    found = True
                    break
    return results

def matches_pam_pattern(dna_seq, pam_pattern):
    if len(dna_seq) != len(pam_pattern):
        return False
    for dna_base, pattern_base in zip(dna_seq.upper(), pam_pattern.upper()):
        if pattern_base != 'N' and dna_base != pattern_base:
            return False
    return True

def generate_and_translate_synonymous_variations(target_seq, gRNA_list, codon_table):
    results_dict = {}
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
                generated_seq = (target_seq[:codon_start] + syn_codon + target_seq[codon_start + 3:])
                new_pam_sequence = generated_seq[pam_start_idx : pam_start_idx + pam_len]
                if not matches_pam_pattern(new_pam_sequence, pam_pattern):
                    valid_dna_variations.append(generated_seq)
        dna_and_protein_pairs = [{'dna': dna_seq, 'protein': translate(dna_seq, codon_table)} for dna_seq in valid_dna_variations]
        results_dict[gRNA_sequence] = dna_and_protein_pairs
    return results_dict

def filter_by_protein(results_dict, reference_protein):
    filtered_results = {}
    for gRNA, results_list in results_dict.items():
        matching_dna_sequences = [pair['dna'] for pair in results_list if pair['protein'] == reference_protein        ]
        if matching_dna_sequences:
            filtered_results[gRNA] = matching_dna_sequences
    return filtered_results

def count_and_sort_modifications(original_seq, modified_seq_dict):
    final_results = {}
    for gRNA, dna_list in modified_seq_dict.items():
        one_nt_changes = []
        two_nt_changes = []
        for modified_seq in dna_list:
            modification_count = 0
            for original_char, modified_char in zip(original_seq, modified_seq):
                if original_char != modified_char:
                    modification_count += 1
            if modification_count == 1:
                one_nt_changes.append({'dna': modified_seq, 'modifications': 1})
            elif modification_count == 2:
                two_nt_changes.append({'dna': modified_seq, 'modifications': 2})
        if one_nt_changes:
            final_results[gRNA] = one_nt_changes
        elif two_nt_changes:
            final_results[gRNA] = two_nt_changes    
    return final_results

def analyze_codon_changes(original_seq, final_filtered_dict, codon_usage_table):
    analysis_results = {}
    for gRNA, results_list in final_filtered_dict.items():
        gRNA_analysis_list = []
        for result_item in results_list:
            modified_seq = result_item['dna']
            modification_count = result_item['modifications']
            changes_found = []
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
                            fold_change = (original_usage / modified_usage)
                            difference_str = f"-{fold_change:.1f}x"
                        elif modified_usage > original_usage:
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
            analyzed_pair = {
                'dna': modified_seq_h,
                'modifications': modification_count, # Mantém a contagem
                'changes': changes_found             # Adiciona a análise de códons
            }
            gRNA_analysis_list.append(analyzed_pair)
        analysis_results[gRNA] = gRNA_analysis_list
    return analysis_results



@app.route('/')
@login_required
def index():
    return render_template('index.html', enzymes=enzymes, organisms=organism_names,  selected_organism='S. cerevisiae')




@app.route('/results', methods=['POST'])
@login_required
def results():
    try:
        # --- Block 1: Input Sequences info ---
        input_seq_1 = bleach.clean(request.form.get("input_seq_1", "AGATGTCAAAAGGCTTGTGACCAAATGTGGAGAATCCTTATTGGGTTGGGTACCGGTCTAAGGTTGGCATGTTTGTATTTCAGATTAACTATTCCAGAA").upper().replace(" ", ""))
        input_seq_2 = bleach.clean(request.form.get("input_seq_2", "AGATGTCAAAAGGCTTGTGACCAAATGTGGAGAATCCTTATTGGGTTGGGTACCGTTCTAAGGTTGGCATGTTTGTATTTCAGATTAACTATTCCAGAA").upper().replace(" ", ""))

        if not re.fullmatch(r"[ATCGRYSWKMBDHVN]+", input_seq_1):
            return jsonify({"error": "Sequence 1 must contain only DNA nucleotides."}), 400
        if len(input_seq_1) > 200:
            return jsonify({"error": "Sequence 1 is too long. Max = 200bp."}), 400

        if not re.fullmatch(r"[ATCGRYSWKMBDHVN]+", input_seq_2):
            return jsonify({"error": "Sequence 2 must contain only DNA nucleotides."}), 400
        if len(input_seq_2) > 200:
            return jsonify({"error": "Sequence 2 is too long. Max = 200bp."}), 400

        snp_data = get_snp_positions(input_seq_1, input_seq_2)
        if snp_data is None:
            return jsonify({"error": "Input sequences are identical or do not have a clear variable region to analyze."}), 400

        input_seq_1_h = highlight_variable_region(input_seq_1, input_seq_2)
        input_seq_2_h = highlight_variable_region(input_seq_2, input_seq_1)

        input_seq_1_rc = rev_comp(input_seq_1)
        input_seq_2_rc = rev_comp(input_seq_2)
        input_seq_1_rc_h = highlight_variable_region(input_seq_1_rc, input_seq_2_rc)
        input_seq_2_rc_h = highlight_variable_region(input_seq_2_rc, input_seq_1_rc)

        protein_1 = translate(input_seq_1, codon_table)
        protein_2 = translate(input_seq_2, codon_table)
        protein_1_h = highlight_variable_region(protein_1, protein_2)
        protein_2_h = highlight_variable_region(protein_2, protein_1)



        # --- Block 2: Enzymes info ---
        selected_enzymes_list = request.form.getlist('enzymes')

        valid_enzymes = set(enzymes.keys())
        if not set(selected_enzymes_list).issubset(valid_enzymes):
            return "Erro: Invalid enzyme detected.", 400

        selected_enzymes = {name: tuple(enzymes[name]) for name in selected_enzymes_list}
        selected_enzymes_np = {name: data for name, data in selected_enzymes.items() if data[-1] == 'np'}
        


        # --- Block 3L: Main Algorithm for CAPS and dCAPS  ---
        max_mismatch_str = request.form.get("max_mismatch", 1)

        valid_mismatches = {"1", "2", "3"}
        if max_mismatch_str not in valid_mismatches:
            return "Erro: Invalid mismatch value.", 400

        max_mismatch = int(max_mismatch_str)

        snp_left_s1, bl1, snp_left_s2, bl2, snp_right_s1, br1, snp_right_s2, br2 = get_snp_positions(input_seq_1, input_seq_2)
        snp_left_s1_rc, bl1_rc, snp_left_s2_rc, bl2_rc,snp_right_s1_rc, br1_rc, snp_right_s2_rc, br2_rc = get_snp_positions(input_seq_1_rc,input_seq_2_rc)

        seq_1_l = select_nucleotides_around(input_seq_1, snp_left_s1 , 9)
        seq_2_l = select_nucleotides_around(input_seq_2, snp_left_s2 , 9)
        seq_1_l_rc = rev_comp(seq_1_l)
        seq_2_l_rc = rev_comp(seq_2_l)
        protein_1l = translate(seq_1_l, codon_table)
        protein_2l = translate(seq_2_l, codon_table)

        analysis_results_l = run_analysis_pipeline(seq_1_l, seq_2_l, selected_enzymes, max_mismatch, degenerate_bases, is_rc_analysis=False)

        natural_rs_s1_l = analysis_results_l['natural_sites_s1']
        natural_rs_s2_l = analysis_results_l['natural_sites_s2']

        lista_final_l_s1 = analysis_results_l['final_primers_s1']
        lista_final_l_s2 = analysis_results_l['final_primers_s2']

        # --- Debug info ---
        rs_s1_l = analysis_results_l['debug_info']['rs_s1']
        rs_s2_l = analysis_results_l['debug_info']['rs_s2']
        snp_l_s1 = analysis_results_l['debug_info']['snp_s1']
        snp_l_s2 = analysis_results_l['debug_info']['snp_s2']
        rs_filtered_l_s1 = analysis_results_l['debug_info']['rs_filtered_s1']
        rs_filtered_l_s2 = analysis_results_l['debug_info']['rs_filtered_s2']
        unique_rs_l_s1 = analysis_results_l['debug_info']['unique_rs_s1']
        unique_rs_l_s2 = analysis_results_l['debug_info']['unique_rs_s2']
        primers_l_s1 = analysis_results_l['debug_info']['primers_s1']
        primers_l_s2 = analysis_results_l['debug_info']['primers_s2']
        validated_primers_l_s1 = analysis_results_l['debug_info']['validated_primers_s1']
        validated_primers_l_s2 = analysis_results_l['debug_info']['validated_primers_s2']

        analysis_results_l_rc = run_analysis_pipeline(seq_1_l_rc, seq_2_l_rc, selected_enzymes_np, max_mismatch, degenerate_bases, is_rc_analysis=True)
        
        natural_rs_s1_l_rc = analysis_results_l_rc['natural_sites_s1']
        natural_rs_s2_l_rc = analysis_results_l_rc['natural_sites_s2']

        lista_final_l_s1_rc = analysis_results_l_rc['final_primers_s1']
        lista_final_l_s2_rc = analysis_results_l_rc['final_primers_s2']

        # --- Debug info rc ---
        rs_s1_l_rc = analysis_results_l_rc['debug_info']['rs_s1']
        rs_s2_l_rc = analysis_results_l_rc['debug_info']['rs_s2']
        snp_l_s1_rc = analysis_results_l_rc['debug_info']['snp_s1']
        snp_l_s2_rc = analysis_results_l_rc['debug_info']['snp_s2']
        rs_filtered_l_s1_rc = analysis_results_l_rc['debug_info']['rs_filtered_s1']
        rs_filtered_l_s2_rc = analysis_results_l_rc['debug_info']['rs_filtered_s2']
        unique_rs_l_s1_rc = analysis_results_l_rc['debug_info']['unique_rs_s1']
        unique_rs_l_s2_rc = analysis_results_l_rc['debug_info']['unique_rs_s2']
        primers_l_s1_rc = analysis_results_l_rc['debug_info']['primers_s1']
        primers_l_s2_rc = analysis_results_l_rc['debug_info']['primers_s2']
        validated_primers_l_s1_rc = analysis_results_l_rc['debug_info']['validated_primers_s1']
        validated_primers_l_s2_rc = analysis_results_l_rc['debug_info']['validated_primers_s2']

        natural_rs_s1_l_final = natural_rs_s1_l + natural_rs_s1_l_rc
        natural_rs_s2_l_final = natural_rs_s2_l + natural_rs_s2_l_rc

        lista_final_final_l_s1 = lista_final_l_s1 + lista_final_l_s1_rc
        lista_final_final_l_s2 = lista_final_l_s2 + lista_final_l_s2_rc
        


        # --- Block 4L: Design a donor with CAPS without change the final protein  ---
        organism_selected = request.form.get('organism', 'S. cerevisiae')
        valid_organisms = {"A. thaliana","B. subtilis", "C. elegans","D. rerio", "D. melanogaster", "E. coli", "Human", "M. musculus", "O. sativa","S. cerevisiae", "S. pombe", "Z. mays"}
        
        if organism_selected not in valid_organisms:
            return "Erro: Invalid organism", 400

        codon_usage = codon_usage_tables.get(organism_selected)

        seq_1_ld = select_nucleotides_around(input_seq_1, snp_left_s1 , 19)
        seq_2_ld = select_nucleotides_around(input_seq_2, snp_left_s2 , 19)
        seq_2_ld_rc = rev_comp(seq_2_ld)
        protein_2_ld = translate(seq_2_ld, codon_table)

        '''
        rs_s2_ld = find_rs_new(seq_2_ld, selected_enzymes, max_mismatch=1)
        rs_s2_ld_1m = [item for item in rs_s2_ld if item[5] == 1]
        grs_s2_ld = generate_modified_sequences(seq_2_ld, rs_s2_ld_1m)
        grs_s2_ld_t = [(item[0], item[1], item[2], item[3],item[4], translate(item[4],codon_table)) for item in grs_s2_ld]
        
        rs_s2_ld_rc = find_rs_new(seq_2_ld, selected_enzymes_np, max_mismatch=1)
        rs_s2_ld_1m_rc = [item for item in rs_s2_l_rc if item[5] == 1]
        grs_s2_ld_rc = generate_modified_sequences(seq_2_ld, rs_s2_ld_1m_rc)
        grs_s2_ld_rc_t = [(item[0], item[1], len(item[4])-item[3], len(item[4])-item[2],rev_comp(item[4]), translate(rev_comp(item[4]),codon_table)) for item in grs_s2_ld_rc]
        '''

        analysis_donor_l = get_donor(seq_2_ld, selected_enzymes, codon_table, is_rc_analysis=False)
        rs_s2_ld = analysis_donor_l['debug_info']['rs_s2']
        rs_s2_ld_1m = analysis_donor_l['debug_info']['rs_s2_1m']
        grs_s2_ld = analysis_donor_l['debug_info']['grs_s2']
        grs_s2_ld_t = analysis_donor_l['grs_s2_t']

        analysis_donor_l_rc = get_donor(seq_2_ld, selected_enzymes, codon_table, is_rc_analysis=True)
        rs_s2_ld_rc = analysis_donor_l_rc['debug_info']['rs_s2']
        rs_s2_ld_1m_rc = analysis_donor_l_rc['debug_info']['rs_s2_1m']
        grs_s2_ld_rc = analysis_donor_l_rc['debug_info']['grs_s2']
        grs_s2_ld_rc_t = analysis_donor_l_rc['grs_s2_t']

        grs_s2_ld_final = grs_s2_ld_t + grs_s2_ld_rc_t
        grs_s2_ld_final_final = [item for item in grs_s2_ld_final if item[5] == protein_2_ld]
        grs_s2_ld_final_final_cu = get_codon_changes(seq_2_ld, grs_s2_ld_final_final, codon_usage)
       
        

        # --- Block 5L: Hiding PAM  ---
        gRNA_input_string_raw = request.form.get('gRNAs', 'CAAATGTGGAGAATCCTTAT, AAATGTGGAGAATCCTTATT, CAAACATGCCAACCTTAGAC, GTTGGGTACCGGTCTAAGGT, TTGGGTTGGGTACCGGTCTA').upper().replace(" ", "")
        gRNA_input_string = bleach.clean(gRNA_input_string_raw)
        
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

        seq_1_r = ""
        seq_2_r = ""
        seq_1_r_rc = ""
        seq_2_r_rc = ""
        snp_r_s1 = ""
        snp_r_s2 = ""
        protein_1r = ""
        protein_2r = ""
        rs_s1 = ""
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


        # --- Block 3R: Main Algorithm for CAPS and dCAPS  ---
        if snp_left_s1 != snp_right_s1:
            seq_1_r = select_nucleotides_around(input_seq_1, snp_right_s1 , 9)
            seq_2_r = select_nucleotides_around(input_seq_2, snp_right_s1 , 9)
            seq_1_r_rc = rev_comp(seq_1_r)
            seq_2_r_rc = rev_comp(seq_2_r)
            protein_rl = translate(seq_1_r, codon_table)
            protein_2l = translate(seq_2_r, codon_table)

            analysis_results_r = run_analysis_pipeline(seq_1_r, seq_2_r, selected_enzymes, max_mismatch, degenerate_bases, is_rc_analysis=False)

            natural_rs_s1_r = analysis_results_r['natural_sites_s1']
            natural_rs_s2_r = analysis_results_r['natural_sites_s2']

            lista_final_r_s1 = analysis_results_r['final_primers_s1']
            lista_final_r_s2 = analysis_results_r['final_primers_s2']

            # --- Debug info ---
            rs_s1_r = analysis_results_r['debug_info']['rs_s1']
            rs_s2_r = analysis_results_r['debug_info']['rs_s2']
            snp_r_s1 = analysis_results_r['debug_info']['snp_s1']
            snp_r_s2 = analysis_results_r['debug_info']['snp_s2']
            rs_filtered_r_s1 = analysis_results_r['debug_info']['rs_filtered_s1']
            rs_filtered_r_s2 = analysis_results_r['debug_info']['rs_filtered_s2']
            unique_rs_r_s1 = analysis_results_r['debug_info']['unique_rs_s1']
            unique_rs_r_s2 = analysis_results_r['debug_info']['unique_rs_s2']
            primers_r_s1 = analysis_results_r['debug_info']['primers_s1']
            primers_r_s2 = analysis_results_r['debug_info']['primers_s2']
            validated_primers_r_s1 = analysis_results_r['debug_info']['validated_primers_s1']
            validated_primers_r_s2 = analysis_results_r['debug_info']['validated_primers_s2']

            analysis_results_r_rc = run_analysis_pipeline(seq_1_r_rc, seq_2_r_rc, selected_enzymes_np, max_mismatch, degenerate_bases, is_rc_analysis=True)
        
            natural_rs_s1_r_rc = analysis_results_r_rc['natural_sites_s1']
            natural_rs_s2_r_rc = analysis_results_r_rc['natural_sites_s2']

            lista_final_r_s1_rc = analysis_results_r_rc['final_primers_s1']
            lista_final_r_s2_rc = analysis_results_r_rc['final_primers_s2']

            # --- Debug info rc ---
            rs_s1_r_rc = analysis_results_r_rc['debug_info']['rs_s1']
            rs_s2_r_rc = analysis_results_r_rc['debug_info']['rs_s2']
            snp_r_s1_rc = analysis_results_r_rc['debug_info']['snp_s1']
            snp_r_s2_rc = analysis_results_r_rc['debug_info']['snp_s2']
            rs_filtered_r_s1_rc = analysis_results_r_rc['debug_info']['rs_filtered_s1']
            rs_filtered_r_s2_rc = analysis_results_r_rc['debug_info']['rs_filtered_s2']
            unique_rs_r_s1_rc = analysis_results_r_rc['debug_info']['unique_rs_s1']
            unique_rs_r_s2_rc = analysis_results_r_rc['debug_info']['unique_rs_s2']
            primers_r_s1_rc = analysis_results_r_rc['debug_info']['primers_s1']
            primers_r_s2_rc = analysis_results_r_rc['debug_info']['primers_s2']
            validated_primers_r_s1_rc = analysis_results_r_rc['debug_info']['validated_primers_s1']
            validated_primers_r_s2_rc = analysis_results_r_rc['debug_info']['validated_primers_s2']

            natural_rs_s1_r_final = natural_rs_s1_r + natural_rs_s1_r_rc
            natural_rs_s2_r_final = natural_rs_s2_r + natural_rs_s2_r_rc

            lista_final_final_r_s1 = lista_final_r_s1 + lista_final_r_s1_rc
            lista_final_final_r_s2 = lista_final_r_s2 + lista_final_r_s2_rc



            # --- Block 4R: Design a donor with CAPS without change the final protein  ---
            seq_1_rd = select_nucleotides_around(input_seq_1, snp_right_s1 , 19)
            seq_2_rd = select_nucleotides_around(input_seq_2, snp_right_s2 , 19)
            seq_2_rd_rc = rev_comp(seq_2_rd)
            protein_2_rd = translate(seq_2_rd, codon_table)

            analysis_donor_r = get_donor(seq_2_rd, selected_enzymes, codon_table, is_rc_analysis=False)
            rs_s2_rd = analysis_donor_r['debug_info']['rs_s2']
            rs_s2_rd_1m = analysis_donor_r['debug_info']['rs_s2_1m']
            grs_s2_rd = analysis_donor_r['debug_info']['grs_s2']
            grs_s2_rd_t = analysis_donor_r['grs_s2_t']

            analysis_donor_r_rc = get_donor(seq_2_rd, selected_enzymes, codon_table, is_rc_analysis=True)
            rs_s2_rd_rc = analysis_donor_r_rc['debug_info']['rs_s2']
            rs_s2_rd_1m_rc = analysis_donor_r_rc['debug_info']['rs_s2_1m']
            grs_s2_rd_rc = analysis_donor_r_rc['debug_info']['grs_s2']
            grs_s2_rd_rc_t = analysis_donor_r_rc['grs_s2_t']

            grs_s2_rd_final = grs_s2_rd_t + grs_s2_rd_rc_t
            grs_s2_rd_final_final = [item for item in grs_s2_rd_final if item[5] == protein_2_rd]
            grs_s2_rd_final_final_cu = get_codon_changes(seq_2_rd, grs_s2_rd_final_final, codon_usage)



            # --- Block 5R: Hiding PAM  ---
            p_s1_r = find_pam_for_grnas(seq_1_r, gRNAs)
            hp_s1_r = generate_and_translate_synonymous_variations(seq_1_r, p_s1_r, codon_table)
            hp_s1_r_filter = filter_by_protein(hp_s1_r, protein_1r)
            hp_s1_r_filter_final = count_and_sort_modifications(seq_1_r, hp_s1_r_filter)
            hp_s1_r_filter_final_cu = analyze_codon_changes(seq_1_r, hp_s1_r_filter_final, codon_usage)



            # --- END ---
            
            
        return render_template('results.html',
                            input_seq_1_h =input_seq_1_h,
                            input_seq_2_h = input_seq_2_h,
                            input_seq_1_rc_h = input_seq_1_rc_h,
                            input_seq_2_rc_h = input_seq_2_rc_h,
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
                            
                            gRNA_input_string = gRNA_input_string,
                            gRNAs = gRNAs,
                            p_s1_l = p_s1_l,
                            hp_s1_l = hp_s1_l,
                            hp_s1_l_filter = hp_s1_l_filter,
                            hp_s1_l_filter_final = hp_s1_l_filter_final,
                            hp_s1_l_filter_final_cu = hp_s1_l_filter_final_cu,
                            organism_selected = organism_selected,
                            selected_enzymes = selected_enzymes,
                            selected_enzymes_np = selected_enzymes_np,
                            seq_2_ld = seq_2_ld,
                            seq_2_ld_rc = seq_2_ld_rc,
                            protein_2_ld = protein_2_ld,
                            rs_s2_ld = rs_s2_ld,
                            rs_s2_ld_1m = rs_s2_ld_1m,
                            grs_s2_ld = grs_s2_ld,
                            grs_s2_ld_t = grs_s2_ld_t,
                            rs_s2_ld_rc = rs_s2_ld_rc,
                            rs_s2_ld_1m_rc = rs_s2_ld_1m_rc,
                            grs_s2_ld_rc = grs_s2_ld_rc,
                            grs_s2_ld_rc_t = grs_s2_ld_rc_t,
                            grs_s2_ld_final = grs_s2_ld_final,
                            grs_s2_ld_final_final = grs_s2_ld_final_final,
                            grs_s2_ld_final_final_cu = grs_s2_ld_final_final_cu
                            )
    
    except Exception as e:
        return f"Erro: {str(e)}", 500
'''
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
'''
if __name__ == '__main__':
    app.run(debug=True)