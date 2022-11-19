
"""
Exercici 5: Andrea Morales

- Fes un programa que mostri mutacions aleatòries d'una seqüència d'ADN a una pàgina html.
- La seqüència està al fitxer dna.fasta.
- Llegiu la seqüència del fitxer i genereu seqüències que tinguin una base (lletra) mutada aleatòriament.
- Les seqüències han de ser úniques, no hi pot haver repetides.
- Per generar la pàgina html, utilitzeu Jinja.
- A la pàgina html la mutació de cada seqüència ha d'estar en vermell,
  i la resta de lletres en color negre.
- El programa només rep un paràmetre: el número de seqüències a generar.
- El programa ha de rebre el número de seqüències des de la línia d'ordres.
- **Poseu el vostre nom i número d'exercici al principi del vostre codi.**

"""
#FINAL VERSION
#ONLY LAST TO DO THE COMPROBATION OF REPEATED SEQUENCE
#--------------------------------------------------------------------------------------------------------------------------------------
#IMPORTS
#--------------------------------------------------------------------------------------------------------------------------------------
import sys
import random
import engine
from pathlib import Path
#--------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------------
#THE SEQUENCE
#--------------------------------------------------------------------------------------------------------------------------------------
def get_fasta(filename: str) -> str:
    '''Input: The path to a .fasta file.
    Output: The contents of th .fasta file as a single string'''  
  
    all_lines: str = Path(filename).read_text().strip()
    seq:       str = ''.join(all_lines.split('\n')[1:])
    
    return seq



def mutate_seq(seq: str) -> dict:
    '''INPUT: A string of the hole sequences
       OUTPUT: A dict with before, snp ,after'''

 
    random_index: int = random.randint(0, len(seq)-1)
    new_letter:   str = random.choice("ATCG")

    before: str = seq[0:random_index]
    after:  str = seq[random_index+1:]

    mutated_seq: dict = {'before':before, 'new_letter': new_letter, 'after': after}

    return mutated_seq

def get_mutated_seq_list(num_seqs:int, seq:str)-> list[dict]:
    '''INPUT:
            num_seqs: Number of sequences
            seq: The string of the sequence untoched
       OUTPUT: A list of the number of the sequences given''' 

    
    mutated_seq_list: list[dict] = [mutate_seq(seq) for _ in range(num_seqs)]

    return  mutated_seq_list



#--------------------------------------------------------------------------------------------------------------------------------------
#MAIN
#--------------------------------------------------------------------------------------------------------------------------------------

def make_html_seq_list (num_seqs : int,
                        template_filename: str,
                        html_filename: str):
    '''INPUT: 
          num_seq: The number of sequences to create
          template_filename: A path to the the template
          html_filename: The name of the html file that will be written in disk
       OUTPUT'''                    

    #Variables
    original:               str = get_fasta('dna.fasta')
    mutated_seq_list: list[dict] = get_mutated_seq_list(num_seqs, seq)
 
    #Fill template
    template_str:  str = Path(template_filename).read_text()
    vars_dict:    dict = {'original':original,'mutated_seq_list':  mutated_seq_list}
    html_seq_list: str = engine.fill_template_str(template_str,vars_dict)

    #Write html in disk
    Path(html_filename).write_text(html_seq_list)

def parse_command_line (command_line: list[str])-> tuple[str, str, str]:


  #Program name & program parameter
  program_name:              str = sys.argv[0]
  program_parameters:  list[str] = sys.argv[1:]

  #Restriction
  assert len(program_parameters) == 3

  #List decostruction
  num_seqs, template_filename, html_filename = program_parameters


  return num_seqs, template_filename, html_filename





#--------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    seq: str = get_fasta('dna.fasta')
    mutated_seq: dict = mutate_seq(seq)
    
    #Terminal
    #num_seqs, template_filename, html_filename = parse_command_line(sys.argv)
    # make_html_seq_list(num_seqs, template_filename, html_filename)


    #VSCODE
    make_html_seq_list(3, 'template2.html', 'index2.html')



