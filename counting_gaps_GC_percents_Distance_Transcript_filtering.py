# -*- coding: utf-8 -*-


import argparse
from os import listdir
from os import mkdir



def get_args():

    parser = argparse.ArgumentParser(description='Batch trimming alignment from a folder')
    parser.add_argument('data_dir', help = 'path to data directory')
    
    return parser.parse_args()

def gap_count(input_file, output_file, output_file2):

    inputfile=open(input_file, 'r')
    outputFH = open(output_file, 'a')
    outputFH2 = open(output_file2, 'w')

    count_seq = 0
    count_trans = 0
    count_dist_sup = 0
    count_distGAP_sup = 0
    name_seq = []
    seq = []

   
    min_similarity = 2

    for line in inputfile:
        if count_seq == 0:
            name_exon=line.strip()
            count_seq +=1
        elif count_seq == 1:
            seq_exon=line.strip()
            #print(name_exon)
            #print(seq_exon)

            count_gap = 0
            count_GC = 0

            for position in line:
                if position =='-':
                    count_gap+=1
                elif position == 'g':
                    count_GC+=1
                elif position == 'c':
                    count_GC+=1

            #print(count_gap)
            #print(len(line))

            gap_percent = count_gap/len(line)*100

            exon_length = len(line)

            count_nuc = len(line)-count_gap

            #print(length_seq)
            #print(count_GC)

            GC_percent = count_GC/count_nuc*100

            # if gap_percent <10 and GC_percent >30 and GC_percent <70:
            #     outputFH2.write(name_exon + '\n' + seq_exon + '\n')
      
            #print(round((gap_percent),2))
            #print(round((GC_percent),2))

            count_seq += 1

        elif count_seq%2==0:
            #print(line)
            # print(line.strip())
            # name_seq=line.strip()
            #print(name_seq)
            name_seq.append(line.strip())
            count_seq += 1
            count_trans +=1



        elif count_seq%2 !=0:
            # seq=line.strip()
            # print(line.strip())
            seq.append(line.strip())
            count_seq +=1   

          
            counter_dist = 0
            counter_distGAP=0
            comp_dist=0
            comp_distGAP=0


            for i in range(len(line.strip())):
                #print(i)
                #print(line[i])
                if line[i] == '-' and seq_exon[i] != '-':
                    counter_distGAP +=1
                    comp_distGAP +=1
                elif line[i] != '-' and seq_exon[i] =='-':
                    counter_distGAP += 1
                    comp_distGAP += 1
                elif line[i] !='-' and seq_exon[i] == line[i]:
                    comp_dist+=1
                elif line[i] != '-' and seq_exon[i] != line[i]:
                    counter_dist +=1
                    comp_dist +=1
                   
            dist_nuc = counter_dist*100/comp_dist
            dist_gap = (counter_distGAP+counter_dist)*100/(comp_dist+comp_distGAP)
            #print(dist_gap)
            if dist_nuc < min_similarity:
                count_dist_sup +=1
            #if dist_gap < min_similarity:
            #    count_distGAP_sup +=1

            dist_percent_nuc = count_dist_sup/count_trans*100
            #dist_percent_gap=count_distGAP_sup/count_trans*100

            # if gap_percent <10 and GC_percent >30 and GC_percent <70 and count_trans>3 :
            #     print(name_seq)
            #     outputFH2.write(name_seq + '\n'+ seq + '\n')

            
    #print(count_dist_sup)
    #print(count_distGAP_sup)  

#            transcripts = count_trans
#            print(transcripts)    
    if gap_percent <5 and GC_percent >30 and GC_percent <70 and count_trans>3 and dist_percent_nuc == 0 : 
        outputFH2.write(name_exon+'\n'+seq_exon+'\n')
        
    for i in range(len(name_seq)):
        if gap_percent <5 and GC_percent >30 and GC_percent <70 and count_trans>3 and dist_percent_nuc == 0 :
        #print(name_seq)
            outputFH2.write(name_seq[i] + '\n' +  seq[i] + '\n')


    outputFH.write(name_exon + '\t' + str(round((gap_percent),2))+ '\t' + str(round((GC_percent),2)) + '\t' + str(exon_length) + '\t' + str(count_trans) + '\t' + str(round((dist_percent_nuc),2)) + '\n')
    

           
    #return(name_exon, gap_percent) 
    #print(name_exon)

    inputfile.close()
    outputFH.close()
    outputFH2.close()

def main():

    args = get_args()
    input_dir = args.data_dir
    output_dir = input_dir+'_sorted_5Percent'
    #output_dir2 = input_dir+'_count_file'
    #print(output_dir)
    mkdir(output_dir)
    #mkdir(output_dir2)
    list_file= listdir(input_dir) #options listdir à regarder

    output_file = output_dir + '/summary.csv'

    output2FH = open(output_file, 'w')

    output2FH.write('Name exon' + '\t' + 'Gap percent' + '\t' + 'GC percent' + '\t' + 'Exon length' + '\t'+ 'Transcript number' + '\t'+ 'Percent dist nuc >2%' + '\n')
    output2FH.close()

    for file in list_file:
        #print(file[:-6])
        #print(trimmed_file)
        input_file = input_dir +'/'+ file

        output_file2= output_dir + '/' + file + '_sorted_5Percent.fasta' 

        gap_count(input_file, output_file, output_file2)

    #output_file.write(gap_count)
        
   
if __name__ == '__main__':  #__name__ est une variable d'environnement
    main()
