# -*- coding: utf-8 -*-




import argparse
from os import listdir
from os import mkdir



def get_args():
    parser = argparse.ArgumentParser(description='Batch trimming alignment from a folder')
    parser.add_argument('data_dir', help = 'path to data directory')
    
    return parser.parse_args()




def limit_seq(alignment_file):

    inputfile=open(alignment_file, "r")
    
    
    file_lines=inputfile.readlines()
    secondline=file_lines[1].strip()
    
    debut=len(secondline)-len(secondline.lstrip('-'))
    fin=len(secondline)-len(secondline[::-1].lstrip('-'))
    finseq=len(secondline)-fin
    
    return(debut,finseq)
    
    inputfile.close()


def count_seq(debut,fin,alignment_file,trimmed_file):
    
    inputfile = open(alignment_file, "r")
    outputfile = open(trimmed_file, "w")    
        
    count_line = 0
                                
    for line in inputfile:
        line = line.strip()
        count_line += 1
        #print(count_line)
        if count_line == 1:
           name_line = line
           print(name_line)
           #outputfile.write(name_line+'\n')
    
        if count_line == 2:
            pos_base = 0
            for position in line[debut:fin]:
                if position == '-':
                    pos_base +=1
            print(pos_base)
            print(len(line[debut:fin]))
            if pos_base != len(line[debut:fin]):
                outputfile.write(name_line+'\n')
                outputfile.write(line[debut:fin]+'\n')
                count_line = 0
            # if pos_base == len(line[debut:fin]):
            #     outputfile.write(name_line+'\n')
            #     outputfile.write(line[debut:fin]+'\n')
            #     count_line = 0
            else:
                count_line = 0

    inputfile.close()
    outputfile.close()

def main():

    args = get_args()
    input_dir = args.data_dir
    output_dir = input_dir+'_trimmed'
    #print(output_dir)
    mkdir(output_dir)
    list_file= listdir(input_dir) #options listdir à regarder

    for file in list_file:
        #print(file[:-6])
        trimmed_file = output_dir + '/' + file.split('.fasta')[0]+'_trimmed.fasta'
        #print(trimmed_file)
        alignment_file = input_dir +'/'+ file
        debut,fin = limit_seq(alignment_file)
        count_seq(debut,fin,alignment_file,trimmed_file)




if __name__ == '__main__':  #__name__ est une variable d'environnement
    main()






