بسم الله الرحمن الرحیم

run_giza
========


# USAGE
```
python run_giz.py [giza_bin_dir] [tokenizer_script_path] [cleaner_script_path] [build_dir] [src_file] [trg_file] [src_lang_type] [trgt_lang_type] [min_len] [max_len]
```
* [giza_bin_dir]: directory where giza++ and mkcls binary files are put. These file should be in that directory:
	* GIZA++
	* mkcls  
	* plain2snt.out  
	* snt2cooc.out
* [tokenizer_script_path]: the perl script tokenizer.perl that can be download from [http://www.statmt.org/europarl/v5/tools.tgz](http://www.statmt.org/europarl/v5/tools.tgz)
* [cleaner_script_path]: can be download from [https://github.com/moses-smt/mosesdecoder/blob/master/scripts/training/clean-corpus-n.perl](https://github.com/moses-smt/mosesdecoder/blob/master/scripts/training/clean-corpus-n.perl)
*  [build_dir]: the directory where the preprocessed and output files should be there. 
    * If the directory does not exist, the script will create it.
	* __WARNING__: If you want to keep your previous results, do not use an already used directory 
* [src_file]: source language corpus file
* [trg_file]: target language corpus file
	* __WARNING__: [src_file] and [trg_file] should have the same number of lines
* [src_lang_type]: can be en, de, ar, etc.
* [trgt_lang_type]: can be en, de, ar, etc.
* [min_len]: minimum number of words per sentence (used for cleaning the corpus)
* [max_len]: maximum number of words per sentence (used for cleaning the corpus)



# Description
This script is created by [Mohammad Sadegh Rasooli](cs.columbia.edu/~rasooli) during PhD research in Columbia University. This script enables you to run Giza++ (along with MKCLS) without any need to run moses decoder. The output is the word alingment from the target language to the source language and vice versa. 

The following preprocessing steps are done while running the script:
* Putting the source/target files in a directory
* Cleaning the corpus by [tokenizing](http://www.statmt.org/europarl/v5/tools.tgz) them, cleaning the corpus based on maximum and minimum size of the senence, lowercasing the chacters.
* Running different scripts such as plain2snt.out and MKCLS to provide data for GIZA++ (for more information read this [blog post](http://andreeaaussi.wordpress.com/2013/03/04/how-to-do-word-alignment-with-giza-from-parallel-corpora/)
* Running giza on both sides (source -> target and target -> source)

# Retrieving Sentences with Casing
__corpus.tok.clean.[lang_id]__ are the files in __[build_dir]__ after cleaning the size of the corpus and __corpus.tok.clean.lower.[lang_id]__ are the files after lowercasing the files. In alignment, lowercased files are used, thus if you want to use the original casing, you can easily align them with __corpus.tok.clean.[lang_id]__ files.

# Retrieving Final Alignments
In __[build_dir]__ you can find the following file patterns:

* src_trg.align.*: Contains different __.final__ files from Giza++ from the source language to the target language.
* trg_src.align.*: Contains different __.final__ files from Giza++ from the target language to the source language.


# Requirements
* Python 2.6 or higher
* Perl
* Giza++ can be installed and the binary files should be put in __[gia_bin_dir]__. For more information, see [part I, support tools installation part of moses guides](http://www.statmt.org/moses_steps.html)