RNAcontext is a motif model to predict the sequence and structure preferences of RNA-binding
proteins. There are two files that have to be provided to input RNAcontext:
- A set of sequnces together with their estimated binding affinities 
- RNA secondary structure annotations of the sequences estimated using SFOLD (details are below).

RCK is an extension of RNAcontext to a k-mer model.

-----------------------------------------------------------------------------
                           Publications             
-----------------------------------------------------------------------------
RCK: accurate and efficient inference of protein-RNA binding models from RNAcompete data
Yaron Orenstein, Yuhao Wang, Bonnie Berger
In preperation.

RNAcontext: a new method for learning the sequence and structure binding preferences of RNA-binding proteins
Hilal Kazan, Debashish Ray, Esther T Chan, Timothy R Hughes, Quaid Morris
Plos Computational Biology  (2010)

Rapid and systematic analysis of the RNA recognition specificities of RNA-binding protein
Debashish Ray and Hilal Kazan et al. 
Nature Biotechnology 27, 667-670 (2009)

-----------------------------------------------------------------------------
                           Install             
-----------------------------------------------------------------------------

The program should run under all Linux distributions, g++ is required. Type: 

 make

and run using the options described below.

Note: Ubuntu users might find the patch include.diff useful, if they have problems in compiling. 

-----------------------------------------------------------------------------
                           How to generate the annotation profiles?             
-----------------------------------------------------------------------------

SFOLD is required, you can download it from here: http://sfold.wadsworth.org/SFOLD-EXE-ACADEMIC.html

Please follow the guidelines provided in SFOLD package to install the software.

By default, SFOLD can generate the probability profile for a single sequence. By using the helper code that 
we provide (in helper_code_for_SFOLD), you can generate profiles for a set of sequences in a FASTA file.

How to compile:
First, copy the files (sfold_helper.cpp and sprofile.cpp) in directory helper_code_for_SFOLD to SFOLD directory. 

g++ sfold_helper.cpp -o sfold_helper
g++ sprofile.cpp -o sprofile

Requirements: 
- Create folders named data and out under SFOLD directory.
- Your FASTA file should be in SFOLD directory.
- sfold_helper and sprofile executables should be in SFOLD directory. 

How to run:

./sfold_helper <input_file_name> <output_file_name>

Example:
./sfold_helper sequences.fasta  sequences_profiles.txt 


-----------------------------------------------------------------------------
                           Usage        
-----------------------------------------------------------------------------
Description of options

    -a 	  <alphabet> (default ACGU)
	  determines the alphabet e.g. alphabet should be ACGT if you're using DNA sequences, and ACGU for RNA sequences etc.

    -e    <annotation alphabet> (default PLMU)
          determines the annotation alphabet. For instance, if the structure profile file has two rows for each sequence, 
	  for paired and unpaired contexts respectively, then you should use a two letter alphabet. You can choose letters
	  for your convenience e.g.PU

    -w    <motifwidth range> (default 4-10)
          controls the size range of the motif e.g. if you run the program with -w 4-7, the algorithm searches for motifs
          starting from width 4 until width 7.

    -c    <training input filename>
          The name of the input file which contains the sequences of interest with corresponding intensities. RNAcontext
          will use these sequences to find the motif model which explains the data best. 

          The format of the input file should be:

	  intensity \tab sequence 

	  0.34	AGCGAGUCGAGAGCUCUUAGAGGCUAUAUAUGCGAG	
	  -1.45 GGAGAGCGGAGAUCUUCUAGAGCUUAGAGGCGAGAGAG

	 If there is binary information (i.e. bound or unbound) about the data, please input intensity of 1 for bound sequences
	 and -1 for unbound sequences.
	
    -d 	  <test input filename>
	  The name of the input file which contains the test sequences. The motif model learned from the training sequences
          will be used to score test sequences.
	 
          The format of the input file should be:
	  intensity \tab sequence 

    -h 	  <annotation profile for training sequences>
	  The name of the file which contains annotation profiles for the training sequences

    -n 	  <annotation profile for test sequences>
	  The name of the file which contains annotation profiles for the test sequences

    -m    <output dir>
          Output files are saved under this directory.
          In binding prediction mode, the model file is under this directory.

    -l    <model filename key>
          The prefix of the model file name (see below, under -o option).
          This option sets the binding prediction mode.

    -o 	  <output filename key>
	  A number of output files with filenames containing <output filename key> are generated under directory ./outputs.
 

      	  - model_<output filename key>_<motifwidth>.txt   e.g. model_VTS1_4.txt

             This file contains the training error, the number of fitted parameters, predicted base parameters, annotation 
             parameter, bias parameters, scaling factor and intercept in least squares optimization. 

	     Four lines following "Base Parameters" has the predicted sequence preference for each base ( rows) and for each position (columns)		
       
	  - params_<output filename key>.txt

            In short, this file contains the PWMs and relative structural context affinities for each motif width.   

            If you would like to plot logos to show sequence preference, you can use the matrix following the "Base parameters" line. We recommend that you use enologos software (http://www.benoslab.pitt.edu/cgi-bin/enologos/enologos.cgi) with weight type "energies" to plot logos.
	    To see the relative affinities to each structural context (these are plot in Figure 4 of the PLos CompBio paper) you can use the values provided for 
	    each structural context. 

	 - train_<output filename key>_<motifwidth>.txt

            This is a tab delimited file where at each line, the first entry is the experimentally determined affinity
	    of a sequence in the training set and the second entry is the RNAcontext predicted affinity (score) for that sequence. 

         - test_<output filename key>_<motifwidth>.txt
	    
	    This is a tab delimited file where at each line, the first entry is the experimentally determined affinity
	    of a sequence in the test set and the second entry is the RNAcontext predicted affinitiy (score) for that sequence. 

    -q    <sequence mode>
          Ignores all structural probabilities. Sets them to uniform instead.

    -s    <number of initializations or restarts> (default 5)
	  It's useful to set s at least 3.


Example Run 

 Training:
 ./bin/rnacontext -b 200 -w 4-5 -a ACGU -e PLMU -s 3 -c VTS1_training_sequences.txt -h VTS1_training_annotations.txt -d VTS1_test_sequences.txt -n VTS1_test_annotations.txt -o VTS1_demo -m ./outputs/

 Predicting:
 ./bin/rnacontext -w 4-4 -a ACGU -e PLMU -d VTS1_test_sequences.txt -n VTS1_test_annotations.txt -l VTS1_demo -m ./outputs/
