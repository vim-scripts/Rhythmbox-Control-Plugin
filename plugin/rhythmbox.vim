" Vim Plugin for contorl Rhythmbox
" JinHyung Park <jinhyung@gmail.com>

function CurSong()
	echo substitute(system("$VIMRUNTIME/plugin/rbvim.py psong"), "\n", "","") 
endfunction

function NextSong()
	echo substitute(system("$VIMRUNTIME/plugin/rbvim.py next"), "\n", "","") 
endfunction

function PrevSong()
	echo substitute(system("$VIMRUNTIME/plugin/rbvim.py prev"), "\n", "","") 
endfunction

function PlayStop()
	echo substitute(system("$VIMRUNTIME/plugin/rbvim.py play"), "\n", "","") 
endfunction

map <silent> <F7> :call CurSong()<CR> 
map <silent> <F9> :call NextSong()<CR> 
map <silent> <F8> :call PrevSong()<CR> 
map <silent> <S-F7> :call PlayStop()<CR> 
