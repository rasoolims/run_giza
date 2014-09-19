بسم الله الرحمن الرحیم

run_giza
========

This script is created by [Mohammad Sadegh Rasooli](cs.columbia.edu/~rasooli) during PhD research in Columbia University. This script enables you to run Giza++ (along with MKCLS) without any need to run moses decoder. The output is the word alingment from the target language to the source language and vice versa. 

The following preprocessing steps are done while running the script:
* Putting the source/target files in a directory
* Cleaning the corpus by [tokenizing](http://www.statmt.org/europarl/v5/tools.tgz) them, cleaning the corpus based on maximum and minimum size of the senence, lowercasing the chacters.
* Running different scripts such as plain2snt.out and MKCLS to provide data for GIZA++ (for more information read this [blog post](http://andreeaaussi.wordpress.com/2013/03/04/how-to-do-word-alignment-with-giza-from-parallel-corpora/)
* Running giza on both side (source -> target and target -> source)



