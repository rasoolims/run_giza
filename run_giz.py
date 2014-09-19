import os,sys

if len(sys.argv)<4:
	print '(MSR_MESSAGE) python run_giz.py [giza_bin_dir] [tokenizer_script_path] [build_dir] [src_file] [trg_file] [src_lang_type] [trgt_lang_type]'
	sys.exit(0)



def clean_corpus(file_path,src_lang_type,trgt_lang_type,min_num,max_num):
	reader1=open(file_path+'.'+src_lang_type,'r')
	reader2=open(file_path+'.'+trgt_lang_type,'r')
	writer1=open(file_path+'.clean.'+src_lang_type,'w')
	writer2=open(file_path+'.clean.'+trgt_lang_type,'w')

	line1=reader1.readline()
	while line1:
		line2=reader2.readline()
		line1=line1.strip()
		line2=line2.strip()
		len1=len(line1.split(' '))
		len2=len(line2.split(' '))
		min_len=min(len1,len2)
		max_len=max(len1,len2)
		if max_len<=max_num and min_len>=min_num and line1 and line2:
			writer1.write(line1+'\n')
			writer2.write(line2+'\n')

		line1=reader1.readline()
	writer1.flush()
	writer1.close()
	writer2.flush()
	writer2.close()



giza_bin_dir=os.path.abspath(sys.argv[1])+'/'
tokenizer_script_path=os.path.abspath(sys.argv[2])

dir_path=os.path.abspath(sys.argv[3])+'/'
if not os.path.isdir(dir_path):
	os.mkdir(dir_path)
os.chdir(dir_path)


print '(MSR_MESSAGE) copying files...'
sys.stdout.flush()
os.system('cp '+sys.argv[4]+' '+dir_path+'src.txt')
os.system('cp '+sys.argv[5]+' '+dir_path+'dst.txt')
src_lang_type=sys.argv[6]
trgt_lang_type=sys.argv[7]


print '(MSR_MESSAGE) tokenizing files...'
sys.stdout.flush()
os.system('perl '+tokenizer_script_path+' -l '+src_lang_type+' < '+dir_path+'src.txt > '+dir_path+'corpus.tok.'+src_lang_type)
os.system('perl '+tokenizer_script_path+' -l '+trgt_lang_type+' < '+dir_path+'dst.txt > '+dir_path+'corpus.tok.'+trgt_lang_type)

print '(MSR_MESSAGE) cleaning files...'
sys.stdout.flush()
clean_corpus(dir_path+'corpus.tok',src_lang_type,trgt_lang_type,2,100)


print '(MSR_MESSAGE) lowercasing files...'
sys.stdout.flush()
final_src_file='corpus.tok.clean.lower.'+src_lang_type
final_dst_file='corpus.tok.clean.lower.'+trgt_lang_type
os.system('tr \'[:upper:]\' \'[:lower:]\' < '+dir_path+'corpus.tok.clean.'+src_lang_type+' > '+dir_path+final_src_file)
os.system('tr \'[:upper:]\' \'[:lower:]\' < '+dir_path+'corpus.tok.clean.'+trgt_lang_type+' >'+dir_path+final_dst_file)



print '(MSR_MESSAGE) starting for source->target...'
print '(MSR_MESSAGE) running plain2snt...'
sys.stdout.flush()
os.system(giza_bin_dir+'plain2snt.out '+dir_path+final_src_file+' '+final_dst_file)
snt_file=dir_path+final_src_file+'_'+final_dst_file+'.snt'
src_vcb_file=dir_path+final_src_file+'.vcb'
dst_vcb_file=dir_path+final_dst_file+'.vcb'


print '(MSR_MESSAGE) running snt2cooc (source->target)...'
sys.stdout.flush()
cooc_file=dir_path+final_src_file+'_'+final_dst_file+'.cooc'
os.system(giza_bin_dir+'snt2cooc.out '+src_vcb_file+' '+dst_vcb_file+' '+snt_file +' > '+cooc_file)

print '(MSR_MESSAGE) running mkcls...'
print giza_bin_dir+'mkcls -n10 -p'+dir_path+final_src_file+' -V'+src_vcb_file+'.classes'
sys.stdout.flush()
os.system(giza_bin_dir+'mkcls -n10 -p'+dir_path+final_src_file+' -V'+src_vcb_file+'.classes')
os.system(giza_bin_dir+'mkcls -n10 -p'+dir_path+final_dst_file+' -V'+dst_vcb_file+'.classes')

print '(MSR_MESSAGE) run gizza on source->target...'
sys.stdout.flush()
os.system(giza_bin_dir+'GIZA++ -S  '+src_vcb_file+ ' -T '+dst_vcb_file+' -C '\
	+ snt_file+' -CoocurrenceFile '+cooc_file+' -o '+dir_path+'src_trg.align '++' > '+dir_path+'s_t_nohup.out')


print '(MSR_MESSAGE) run gizza on target->source...'
sys.stdout.flush()
snt_file=dir_path+final_dst_file+'_'+final_src_file+'.snt'
cooc_file=dir_path+final_dst_file+'_'+final_src_file+'.cooc'


print '(MSR_MESSAGE) running snt2cooc (target->source)...'
sys.stdout.flush()
os.system(giza_bin_dir+'snt2cooc.out '+src_vcb_file+' '+dst_vcb_file+' '+snt_file +' > '+cooc_file)

print giza_bin_dir+'GIZA++ -S  '+dst_vcb_file+ ' -T '+src_vcb_file+' -C '\
	+ snt_file+' -CoocurrenceFile '+cooc_file +' -o '+dir_path+'trg_src.align '+' > '+dir_path+'t_s_nohup.out'
sys.stdout.flush()


os.system(giza_bin_dir+'GIZA++ -S  '+dst_vcb_file+ ' -T '+src_vcb_file+' -C '\
	+ snt_file+' -CoocurrenceFile '+cooc_file +' > '+dir_path+'t_s_nohup.out')

print '(MSR_MESSAGE) done!'

