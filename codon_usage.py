#codon_usage.py

# https://www.kazusa.or.jp/codon/
codon_usage_tables = {
    'Human': {
        'UUU': 17.6, 'UCU': 15.2, 'UAU': 12.2, 'UGU': 10.6, 'UUC': 20.3, 'UCC': 17.7, 'UAC': 15.3, 'UGC': 12.6,
        'UUA': 7.7,  'UCA': 12.2, 'UAA': 1.0,  'UGA': 1.6, 'UUG': 12.9, 'UCG': 4.4,  'UAG': 0.8,  'UGG': 13.2,
        'CUU': 13.2, 'CCU': 17.5, 'CAU': 10.9, 'CGU': 4.5, 'CUC': 19.6, 'CCC': 19.8, 'CAC': 15.1, 'CGC': 10.4,
        'CUA': 7.2,  'CCA': 16.9, 'CAA': 12.3, 'CGA': 6.2, 'CUG': 39.6, 'CCG': 6.9,  'CAG': 34.2, 'CGG': 11.4,
        'AUU': 16.0, 'ACU': 13.1, 'AAU': 17.0, 'AGU': 12.1, 'AUC': 20.8, 'ACC': 18.9, 'AAC': 19.1, 'AGC': 19.5,
        'AUA': 7.5,  'ACA': 15.1, 'AAA': 24.4, 'AGA': 12.2, 'AUG': 22.0, 'ACG': 6.1,  'AAG': 31.9, 'AGG': 12.0,
        'GUU': 11.0, 'GCU': 18.4, 'GAU': 21.8, 'GGU': 10.8, 'GUC': 14.5, 'GCC': 27.7, 'GAC': 25.1, 'GGC': 22.2,
        'GUA': 7.1,  'GCA': 15.8, 'GAA': 29.0, 'GGA': 16.5, 'GUG': 28.1, 'GCG': 7.4,  'GAG': 39.6, 'GGG': 16.5
    },
    'E. coli': {
        'UUU': 23.2, 'UCU': 8.7,  'UAU': 16.5, 'UGU': 5.5, 'UUC': 16.9, 'UCC': 8.9,  'UAC': 12.1, 'UGC': 6.9,
        'UUA': 13.9, 'UCA': 7.8,  'UAA': 2.0,  'UGA': 1.1, 'UUG': 14.0, 'UCG': 8.7,  'UAG': 0.3,  'UGG': 15.2,
        'CUU': 11.7, 'CCU': 7.3,  'CAU': 13.6, 'CGU': 20.3, 'CUC': 11.0, 'CCC': 5.8,  'CAC': 9.8,  'CGC': 21.0,
        'CUA': 4.0,  'CCA': 8.5,  'CAA': 15.0, 'CGA': 3.9, 'CUG': 50.9, 'CCG': 21.8, 'CAG': 29.5, 'CGG': 6.3,
        'AUU': 29.8, 'ACU': 9.1,  'AAU': 18.6, 'AGU': 9.5, 'AUC': 24.2, 'ACC': 22.8, 'AAC': 21.4, 'AGC': 16.0,
        'AUA': 5.4,  'ACA': 8.2,  'AAA': 33.2, 'AGA': 2.9, 'AUG': 27.0, 'ACG': 14.8, 'AAG': 10.7, 'AGG': 1.9,
        'GUU': 18.5, 'GCU': 15.6, 'GAU': 32.1, 'GGU': 24.4, 'GUC': 15.1, 'GCC': 25.1, 'GAC': 18.6, 'GGC': 27.9,
        'GUA': 11.1, 'GCA': 20.6, 'GAA': 38.2, 'GGA': 9.0, 'GUG': 25.5, 'GCG': 31.7, 'GAG': 17.7, 'GGG': 11.3
    },
    'S. cerevisiae': {
        'UUU': 26.1, 'UCU': 23.5, 'UAU': 18.8, 'UGU': 8.1, 'UUC': 18.4, 'UCC': 14.2, 'UAC': 14.8, 'UGC': 4.8,
        'UUA': 26.2, 'UCA': 18.7, 'UAA': 1.1,  'UGA': 0.7, 'UUG': 27.2, 'UCG': 8.6,  'UAG': 0.5,  'UGG': 10.4,
        'CUU': 12.3, 'CCU': 13.5, 'CAU': 13.6, 'CGU': 6.4, 'CUC': 5.4,  'CCC': 6.8,  'CAC': 7.8,  'CGC': 2.6,
        'CUA': 13.4, 'CCA': 18.3, 'CAA': 27.3, 'CGA': 3.0, 'CUG': 10.5, 'CCG': 5.3,  'CAG': 12.1, 'CGG': 1.7,
        'AUU': 30.1, 'ACU': 20.3, 'AAU': 35.7, 'AGU': 14.2, 'AUC': 17.2, 'ACC': 12.7, 'AAC': 24.8, 'AGC': 9.8,
        'AUA': 17.8, 'ACA': 17.8, 'AAA': 41.9, 'AGA': 21.3, 'AUG': 20.9, 'ACG': 8.0,  'AAG' :30.8, 'AGG': 9.2,
        'GUU': 22.1, 'GCU': 21.2, 'GAU': 37.6, 'GGU': 23.9, 'GUC': 11.8, 'GCC': 12.6, 'GAC': 20.2, 'GGC': 9.8,
        'GUA': 11.8, 'GCA': 16.2, 'GAA': 45.6, 'GGA': 10.9, 'GUG': 10.8, 'GCG': 6.2,  'GAG': 19.2, 'GGG': 6.0
    },
    'A. thaliana': {
        'UUU': 21.8, 'UCU': 25.2, 'UAU': 14.6, 'UGU': 10.5, 'UUC': 20.7, 'UCC': 11.2, 'UAC': 13.7, 'UGC': 7.2,
        'UUA': 12.7, 'UCA': 18.3, 'UAA': 0.9,  'UGA': 1.2, 'UUG': 20.9, 'UCG': 9.3,  'UAG': 0.5,  'UGG': 12.5,
        'CUU': 24.1, 'CCU': 18.7, 'CAU': 13.8, 'CGU': 9.0, 'CUC': 16.1, 'CCC': 5.3,  'CAC': 8.7,  'CGC': 3.8,
        'CUA': 9.9,  'CCA': 16.1, 'CAA': 19.4, 'CGA': 6.3, 'CUG': 9.8,  'CCG': 8.6,  'CAG': 15.2, 'CGG': 4.9,
        'AUU': 21.5, 'ACU': 17.5, 'AAU': 22.3, 'AGU': 14.0, 'AUC': 18.5, 'ACC': 10.3, 'AAC': 20.9, 'AGC': 11.3,
        'AUA': 12.6, 'ACA': 15.7, 'AAA': 30.8, 'AGA': 19.0, 'AUG': 24.5, 'ACG': 7.7,  'AAG': 32.7, 'AGG': 11.0,
        'GUU': 27.2, 'GCU': 28.3, 'GAU': 36.6, 'GGU': 22.2, 'GUC': 12.8, 'GCC': 10.3, 'GAC': 17.2, 'GGC': 9.2,
        'GUA': 9.9,  'GCA': 17.5, 'GAA': 34.3, 'GGA': 24.2, 'GUG': 17.4, 'GCG': 9.0,  'GAG': 32.2, 'GGG': 10.2
    },
    'C. elegans': {
        'UUU': 23.3, 'UCU': 16.7, 'UAU': 17.5, 'UGU': 11.2, 'UUC': 23.9, 'UCC': 10.6, 'UAC': 13.7, 'UGC': 9.1,
        'UUA': 9.8,  'UCA': 20.6, 'UAA': 1.6,  'UGA': 1.4, 'UUG': 20.0, 'UCG': 12.2, 'UAG': 0.6,  'UGG': 11.1,
        'CUU': 21.2, 'CCU': 8.8,  'CAU': 14.1, 'CGU': 11.2, 'CUC': 14.8, 'CCC': 4.4,  'CAC': 9.2,  'CGC': 5.1,
        'CUA': 7.9,  'CCA': 26.1, 'CAA': 27.4, 'CGA': 12.1, 'CUG': 12.1, 'CCG': 9.7,  'CAG': 14.4, 'CGG': 4.7,
        'AUU': 32.2, 'ACU': 18.9, 'AAU': 30.2, 'AGU': 12.1, 'AUC': 18.9, 'ACC': 10.4, 'AAC': 18.3, 'AGC': 8.4,
        'AUA': 9.5,  'ACA': 20.0, 'AAA': 37.5, 'AGA': 15.4, 'AUG': 26.1, 'ACG': 8.9,  'AAG': 25.8, 'AGG': 4.0,
        'GUU': 24.1, 'GCU': 22.4, 'GAU': 35.8, 'GGU': 10.9, 'GUC': 13.6, 'GCC': 12.6, 'GAC': 17.1, 'GGC': 6.7,
        'GUA': 9.8,  'GCA': 19.8, 'GAA': 40.8, 'GGA': 31.7, 'GUG': 14.3, 'GCG': 8.2,  'GAG': 24.5, 'GGG': 4.4
    },
    'M. musculus': {
        'UUU': 17.2, 'UCU': 16.2, 'UAU': 12.2, 'UGU': 11.4, 'UUC': 21.8, 'UCC': 18.1, 'UAC': 16.1, 'UGC': 12.3,
        'UUA': 6.7,  'UCA': 11.8, 'UAA': 1.0,  'UGA': 1.6, 'UUG': 13.4, 'UCG': 4.2,  'UAG': 0.8,  'UGG': 12.5,
        'CUU': 13.4, 'CCU': 18.4, 'CAU': 10.6, 'CGU': 4.7, 'CUC': 20.2, 'CCC': 18.2, 'CAC': 15.3, 'CGC': 9.4,
        'CUA': 8.1,  'CCA': 17.3, 'CAA': 12.0, 'CGA': 6.6, 'CUG': 39.5, 'CCG': 6.2,  'CAG': 34.1, 'CGG': 10.2,
        'AUU': 15.4, 'ACU': 13.7, 'AAU': 15.6, 'AGU': 12.7, 'AUC': 22.5, 'ACC': 19.0, 'AAC': 20.3, 'AGC': 19.7,
        'AUA': 7.4,  'ACA': 16.0, 'AAA': 21.9, 'AGA': 12.1, 'AUG': 22.8, 'ACG': 5.6,  'AAG': 33.6, 'AGG': 12.2,
        'GUU': 10.7, 'GCU': 20.0, 'GAU': 21.0, 'GGU': 11.4, 'GUC': 15.4, 'GCC': 26.0, 'GAC': 26.0, 'GGC': 21.2,
        'GUA': 7.4,  'GCA': 15.8, 'GAA': 27.0, 'GGA': 16.8, 'GUG': 28.4, 'GCG': 6.4,  'GAG': 39.4, 'GGG': 15.2
    },
    'D. rerio': {
        'UUU': 18.2, 'UCU': 16.9, 'UAU': 12.6, 'UGU': 11.3, 'UUC': 20.8, 'UCC': 15.2, 'UAC': 17.0, 'UGC': 11.2,
        'UUA': 7.0,  'UCA': 13.2, 'UAA': 1.1,  'UGA': 1.4, 'UUG': 12.3, 'UCG': 5.6,  'UAG': 0.6,  'UGG': 11.6,
        'CUU': 12.7, 'CCU': 16.6, 'CAU': 10.9, 'CGU': 6.9, 'CUC': 17.0, 'CCC': 12.7, 'CAC': 14.8, 'CGC': 9.6,
        'CUA': 6.2,  'CCA': 15.7, 'CAA': 11.8, 'CGA': 6.7, 'CUG': 37.6, 'CCG': 8.2,  'CAG': 33.5, 'CGG': 6.6,
        'AUU': 16.5, 'ACU': 14.5, 'AAU': 16.3, 'AGU': 13.2, 'AUC': 23.7, 'ACC': 16.2, 'AAC': 24.1, 'AGC': 18.4,
        'AUA': 7.7,  'ACA': 17.0, 'AAA': 29.3, 'AGA': 14.3, 'AUG': 25.5, 'ACG': 7.4,  'AAG': 30.7, 'AGG': 10.2,
        'GUU': 14.1, 'GCU': 20.9, 'GAU': 24.8, 'GGU': 13.7, 'GUC': 14.8, 'GCC': 19.5, 'GAC': 27.8, 'GGC': 17.2,
        'GUA': 6.7,  'GCA': 16.6, 'GAA': 24.4, 'GGA': 21.5, 'GUG': 28.3, 'GCG': 8.6,  'GAG': 42.8, 'GGG': 10.0
    },
    'D. melanogaster': {
        'UUU': 13.2, 'UCU': 7.0,  'UAU': 10.8, 'UGU': 5.4, 'UUC': 21.8, 'UCC': 19.6, 'UAC': 18.4, 'UGC': 13.2,
        'UUA': 4.5,  'UCA': 7.8,  'UAA': 0.8,  'UGA': 0.5, 'UUG': 16.1, 'UCG': 16.6, 'UAG': 0.7,  'UGG': 9.9,
        'CUU': 9.0,  'CCU': 6.9,  'CAU': 10.8, 'CGU': 8.8, 'CUC': 13.8, 'CCC': 18.1, 'CAC': 16.2, 'CGC': 18.0,
        'CUA': 8.2,  'CCA': 13.5, 'CAA': 15.6, 'CGA': 8.4, 'CUG': 38.2, 'CCG': 15.8, 'CAG': 36.1, 'CGG': 8.2,
        'AUU': 16.6, 'ACU': 9.5,  'AAU': 21.0, 'AGU': 11.5, 'AUC': 22.9, 'ACC': 21.3, 'AAC': 26.2, 'AGC': 20.4,
        'AUA': 9.5,  'ACA': 11.0, 'AAA': 17.0, 'AGA': 5.1, 'AUG': 23.6, 'ACG': 14.4, 'AAG': 39.5, 'AGG': 6.3,
        'GUU': 11.0, 'GCU': 14.4, 'GAU': 27.6, 'GGU': 13.3, 'GUC': 13.9, 'GCC': 33.6, 'GAC': 24.6, 'GGC': 26.7,
        'GUA': 6.4,  'GCA': 12.8, 'GAA': 21.1, 'GGA': 18.0, 'GUG': 27.8, 'GCG': 14.0, 'GAG': 42.5, 'GGG': 4.7
    },
    'O. sativa': {
        'UUU': 13.1, 'UCU': 12.7, 'UAU': 10.0, 'UGU': 6.2, 'UUC': 22.4, 'UCC': 16.3, 'UAC': 15.1, 'UGC': 12.4,
        'UUA': 6.1,  'UCA': 12.4, 'UAA': 0.7,  'UGA': 1.2, 'UUG': 14.7, 'UCG': 12.3, 'UAG': 0.8,  'UGG': 13.8,
        'CUU': 15.2, 'CCU': 13.6, 'CAU': 11.3, 'CGU': 7.2, 'CUC': 25.8, 'CCC': 12.1, 'CAC': 13.8, 'CGC': 16.1,
        'CUA': 7.7,  'CCA': 14.2, 'CAA': 13.5, 'CGA': 6.4, 'CUG': 21.0, 'CCG': 18.0, 'CAG': 20.8, 'CGG': 13.4,
        'AUU': 14.2, 'ACU': 10.6, 'AAU': 15.1, 'AGU': 8.8, 'AUC': 19.4, 'ACC': 14.9, 'AAC': 18.5, 'AGC': 16.0,
        'AUA': 8.8,  'ACA': 11.6, 'AAA': 16.0, 'AGA': 10.5, 'AUG': 23.8, 'ACG': 11.4, 'AAG': 32.3, 'AGG': 16.0,
        'GUU': 15.5, 'GCU': 19.6, 'GAU': 25.3, 'GGU': 14.8, 'GUC': 20.1, 'GCC': 30.8, 'GAC': 28.1, 'GGC': 29.5,
        'GUA': 6.8,  'GCA': 17.3, 'GAA': 21.6, 'GGA': 15.9, 'GUG': 24.3, 'GCG': 26.6, 'GAG': 38.6, 'GGG': 17.1
    },
    'Z. mays': {
        'UUU': 12.6, 'UCU': 12.0, 'UAU': 9.5,  'UGU': 5.6, 'UUC': 25.1, 'UCC': 16.4, 'UAC': 19.4, 'UGC': 12.2,
        'UUA': 5.7,  'UCA': 11.0, 'UAA': 0.5,  'UGA': 1.1, 'UUG': 13.0, 'UCG': 10.7, 'UAG': 0.7,  'UGG': 13.0,
        'CUU': 15.7, 'CCU': 12.6, 'CAU': 10.1, 'CGU': 6.0, 'CUC': 25.4, 'CCC': 13.5, 'CAC': 14.9, 'CGC': 14.3,
        'CUA': 7.3,  'CCA': 13.8, 'CAA': 13.2, 'CGA': 4.4, 'CUG': 25.8, 'CCG': 15.8, 'CAG': 23.7, 'CGG': 9.5,
        'AUU': 13.8, 'ACU': 10.7, 'AAU': 13.5, 'AGU': 7.8, 'AUC': 22.7, 'ACC': 16.6, 'AAC': 22.1, 'AGC': 16.4,
        'AUA': 8.4,  'ACA': 10.5, 'AAA': 15.1, 'AGA': 8.8, 'AUG': 24.2, 'ACG': 11.0, 'AAG': 39.4, 'AGG': 14.8,
        'GUU': 15.7, 'GCU': 21.0, 'GAU': 22.9, 'GGU': 14.1, 'GUC': 21.0, 'GCC': 31.1, 'GAC': 32.1, 'GGC': 30.3,
        'GUA': 6.4,  'GCA': 16.7, 'GAA': 19.9, 'GGA': 13.4, 'GUG': 25.5, 'GCG': 23.3, 'GAG': 40.8, 'GGG': 15.4
    },
    'S. pombe': {
        'UUU': 32.5, 'UCU': 30.3, 'UAU': 22.1, 'UGU': 9.0, 'UUC': 13.0, 'UCC': 12.2, 'UAC': 11.8, 'UGC': 5.6,
        'UUA': 26.3, 'UCA': 18.1, 'UAA': 1.3,  'UGA': 0.4, 'UUG': 24.1, 'UCG': 8.1,  'UAG': 0.4,  'UGG': 11.1,
        'CUU': 25.3, 'CCU': 21.6, 'CAU': 16.3, 'CGU': 15.6, 'CUC': 7.3,  'CCC': 8.1,  'CAC': 6.3,  'CGC': 6.0,
        'CUA': 8.7,  'CCA': 12.7, 'CAA': 27.4, 'CGA': 8.0, 'CUG': 6.5,  'CCG': 4.6,  'CAG': 10.9, 'CGG': 3.0,
        'AUU': 35.1, 'ACU': 23.0, 'AAU': 34.1, 'AGU': 14.9, 'AUC': 12.6, 'ACC': 10.7, 'AAC': 17.8, 'AGC': 9.2,
        'AUA': 13.5, 'ACA': 14.3, 'AAA': 39.8, 'AGA': 11.3, 'AUG': 20.8, 'ACG': 6.6,  'AAG': 24.5, 'AGG': 5.1,
        'GUU': 29.0, 'GCU': 29.8, 'GAU': 38.0, 'GGU': 21.5, 'GUC': 10.7, 'GCC': 11.5, 'GAC': 15.7, 'GGC': 8.3,
        'GUA': 12.4, 'GCA': 15.9, 'GAA': 44.4, 'GGA': 15.9, 'GUG': 8.3,  'GCG': 5.4,  'GAG': 21.0, 'GGG': 4.4
    },
    'B. subtilis': {
        'UUU': 30.0, 'UCU': 12.7, 'UAU': 23.3, 'UGU': 3.6, 'UUC': 14.3, 'UCC': 8.3,  'UAC': 12.6, 'UGC': 4.3,
        'UUA': 19.8, 'UCA': 14.6, 'UAA': 1.9,  'UGA': 0.8, 'UUG': 15.8, 'UCG': 6.5,  'UAG': 0.5,  'UGG': 10.7,
        'CUU': 21.8, 'CCU': 10.6, 'CAU': 15.7, 'CGU': 7.2, 'CUC': 10.7, 'CCC': 3.5,  'CAC': 7.5,  'CGC': 8.2,
        'CUA': 4.9,  'CCA': 7.1,  'CAA': 20.4, 'CGA': 4.3, 'CUG': 23.0, 'CCG': 16.3, 'CAG': 18.5, 'CGG': 6.9,
        'AUU': 36.2, 'ACU': 8.7,  'AAU': 22.9, 'AGU': 6.8, 'AUC': 27.2, 'ACC': 9.0,  'AAC': 17.8, 'AGC': 14.4,
        'AUA': 9.8,  'ACA': 21.6, 'AAA': 48.4, 'AGA': 10.5, 'AUG': 26.3, 'ACG': 14.9, 'AAG': 20.8, 'AGG': 4.1,
        'GUU': 18.6, 'GCU': 18.6, 'GAU': 33.2, 'GGU': 13.0, 'GUC': 17.3, 'GCC': 16.5, 'GAC': 19.0, 'GGC': 23.3,
        'GUA': 13.0, 'GCA': 21.1, 'GAA': 48.1, 'GGA': 21.8, 'GUG': 17.3, 'GCG': 19.8, 'GAG': 22.6, 'GGG': 11.2
    }
}

organism_names = {
    'A. thaliana': 'A. thaliana',
    'B. subtilis': 'B. subtilis',
    'C. elegans': 'C. elegans',
    'D. rerio': 'D. rerio (Zebrafish)',
    'D. melanogaster': 'D. melanogaster (Fruit Fly)',
    'E. coli': 'E. coli',
    'Human': 'Human',
    'M. musculus': 'M. musculus (Mouse)',
    'O. sativa': 'O. sativa (Rice)',
    'S. cerevisiae': 'S. cerevisiae (Baker´s Yeast)',
    'S. pombe': 'S. pombe (Fission Yeast)',
    'Z. mays': 'Z. mays (Maize)',
}