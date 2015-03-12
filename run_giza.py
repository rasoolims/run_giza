import os,sys,glob,re

if len(sys.argv)<4:
	print 'python run_giza.py [giza_bin_dir] [tokenizer_script_path] [cleaner_script_path] [build_dir] [src_file] [trg_file] [src_lang_type] [trgt_lang_type] [min_len] [max_len]'
	print 'WARNING: if [build_dir] is not empty, it will overwrite previous alignment files'
	print 'input null if your text is pre-tokenized'
	sys.exit(0)



def clean_corpus(cleaner_script_path, file_path,src_lang_type,trgt_lang_type,min_num,max_num):
	clean_path=file_path+'.clean'
	os.system('perl '+cleaner_script_path+' '+file_path+' '+src_lang_type+' '+trgt_lang_type+' '+clean_path+' '+str(min_num)+' '+str(max_num))
	os.system('sed -i \'s/  */\ /g\' '+clean_path+'.'+src_lang_type)
	os.system('sed -i \'s/  */\ /g\' '+clean_path+'.'+trgt_lang_type)
	os.system('sed -i \'s/  /\ /g\' '+clean_path+'.'+src_lang_type)
	os.system('sed -i \'s/  /\ /g\' '+clean_path+'.'+trgt_lang_type)
	os.system('sed -i \'s/  /\ /g\' '+clean_path+'.'+src_lang_type)
	os.system('sed -i \'s/  /\ /g\' '+clean_path+'.'+trgt_lang_type)
	
giza_bin_dir=os.path.abspath(sys.argv[1])+'/'
tokenizer_script_path=os.path.abspath(sys.argv[2])
cleaner_script_path=os.path.abspath(sys.argv[3])

dir_path=os.path.abspath(sys.argv[4])+'/'
if not os.path.isdir(dir_path):
	os.mkdir(dir_path)

os.system('rm -f '+dir_path+'*.final')


print '(MSR_MESSAGE) copying files...'
sys.stdout.flush()
os.system('cp '+sys.argv[5]+' '+dir_path+'src.txt')
os.system('cp '+sys.argv[6]+' '+dir_path+'dst.txt')
src_lang_type=sys.argv[7]
trgt_lang_type=sys.argv[8]
min_len=int(sys.argv[9])
max_len=int(sys.argv[10])
os.chdir(dir_path)

print '(MSR_MESSAGE) tokenizing files...'
sys.stdout.flush()
if src_lang_type=='en':
	os.system(' sed -i "s/\' s /\'s /g" '+dir_path+'src.txt')
if trgt_lang_type=='en':
	os.system(' sed -i "s/\' s /\'s /g" '+dir_path+'dst.txt')

if sys.argv[2]!='null':
	os.system('perl '+tokenizer_script_path+' -l '+src_lang_type+' < '+dir_path+'src.txt > '+dir_path+'corpus.tok.'+src_lang_type)
	os.system('perl '+tokenizer_script_path+' -l '+trgt_lang_type+' < '+dir_path+'dst.txt > '+dir_path+'corpus.tok.'+trgt_lang_type)
else:
	os.system('cp '+dir_path+'src.txt ' +dir_path+'corpus.tok.'+src_lang_type)
	os.system('cp '+dir_path+'dst.txt ' +dir_path+'corpus.tok.'+trgt_lang_type)

print '(MSR_MESSAGE) cleaning files...'
sys.stdout.flush()
clean_corpus(cleaner_script_path, dir_path+'corpus.tok',src_lang_type,trgt_lang_type,min_len,max_len)


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


'''
	source -> target
'''

print '(MSR_MESSAGE) running snt2cooc (source->target)...'
sys.stdout.flush()
cooc_file=dir_path+final_src_file+'_'+final_dst_file+'.cooc'
os.system(giza_bin_dir+'snt2cooc.out '+src_vcb_file+' '+dst_vcb_file+' '+snt_file +' > '+cooc_file)

print '(MSR_MESSAGE) running mkcls...'
print giza_bin_dir+'mkcls -n10 -p'+dir_path+final_src_file+' -V'+src_vcb_file+'.classes'
sys.stdout.flush()
os.system(giza_bin_dir+'mkcls -n10 -p'+dir_path+final_src_file+' -V'+src_vcb_file+'.classes')
os.system(giza_bin_dir+'mkcls -n10 -p'+dir_path+final_dst_file+' -V'+dst_vcb_file+'.classes')

print '(MSR_MESSAGE) run giza on source->target...'
sys.stdout.flush()
os.system(giza_bin_dir+'GIZA++ -S  '+src_vcb_file+ ' -T '+dst_vcb_file+' -C '\
	+ snt_file+' -CoocurrenceFile '+cooc_file+' -o '+dir_path+trgt_lang_type+'_'+src_lang_type+'.align '+' > '+dir_path+'s_t_nohup.out')


'''
	target -> source
'''
print '(MSR_MESSAGE) target->source...'
sys.stdout.flush()
snt_file=dir_path+final_dst_file+'_'+final_src_file+'.snt'
cooc_file=dir_path+final_dst_file+'_'+final_src_file+'.cooc'


print '(MSR_MESSAGE) running snt2cooc (target->source)...'
sys.stdout.flush()
os.system(giza_bin_dir+'snt2cooc.out '+src_vcb_file+' '+dst_vcb_file+' '+snt_file +' > '+cooc_file)

print '(MSR_MESSAGE) run giza...'
sys.stdout.flush()
os.system(giza_bin_dir+'GIZA++ -S  '+dst_vcb_file+ ' -T '+src_vcb_file+' -C '\
	+ snt_file+' -CoocurrenceFile '+cooc_file +' -o '+dir_path+src_lang_type+'_'+trgt_lang_type+'.align '+' > '+dir_path+'t_s_nohup.out')

print '(MSR_MESSAGE) done!'

