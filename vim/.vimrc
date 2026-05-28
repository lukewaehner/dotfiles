" ============================================================
" PLUGINS
" ============================================================
" Bootstrap: curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
"   https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

call plug#begin('~/.vim/plugged')

Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
Plug 'tpope/vim-fugitive'
Plug 'airblade/vim-gitgutter'
Plug 'christoomey/vim-tmux-navigator'
Plug 'dense-analysis/ale'
Plug 'sheerun/vim-polyglot'
Plug 'folke/tokyonight.nvim', { 'branch': 'main' }
Plug 'justinmk/vim-sneak'
Plug 'liuchengxu/vim-which-key'
Plug 'mhinz/vim-startify'

call plug#end()

" ============================================================
" OPTIONS
" ============================================================
set nocompatible
syntax on
filetype plugin indent on

set number relativenumber
set expandtab shiftwidth=2 tabstop=2 softtabstop=2
set smartindent
set ignorecase smartcase
set splitright splitbelow
set clipboard=unnamedplus
set scrolloff=8
set updatetime=100
set hidden
set termguicolors
set signcolumn=yes
set incsearch hlsearch
set wildmenu
set wildmode=longest:full,full
set laststatus=2
set encoding=utf-8
set backspace=indent,eol,start
set mouse=a

" ============================================================
" THEME
" ============================================================
let g:tokyonight_style = 'night'
let g:tokyonight_transparent_background = 1
silent! colorscheme tokyonight

" ============================================================
" STATUSLINE
" ============================================================
function! ALEStatus() abort
  let l:counts = ale#statusline#Count(bufnr(''))
  let l:errors = l:counts.error + l:counts.style_error
  let l:warnings = l:counts.warning + l:counts.style_warning
  if l:errors == 0 && l:warnings == 0
    return ''
  endif
  return printf(' ✗%d ▲%d', l:errors, l:warnings)
endfunction

set statusline=
set statusline+=\ %f                     " filename
set statusline+=\ %m                     " modified flag
set statusline+=%=                       " right side
set statusline+=%{ALEStatus()}           " ALE errors/warnings
set statusline+=\ %y                     " filetype
set statusline+=\ %l:%c                  " line:col
set statusline+=\ %p%%\                  " percentage

" ============================================================
" PLUGIN CONFIG
" ============================================================

" --- fzf ---
let g:fzf_layout = { 'down': '40%' }

" --- gitgutter ---
let g:gitgutter_sign_added    = '+'
let g:gitgutter_sign_modified = '~'
let g:gitgutter_sign_removed  = '-'

" --- ale ---
let g:ale_linters = { 'python': ['ruff'] }
let g:ale_fixers  = { 'python': ['ruff_format'], '*': ['remove_trailing_lines'] }
let g:ale_fix_on_save           = 1
let g:ale_lint_on_text_changed  = 'never'
let g:ale_lint_on_enter         = 0
let g:ale_lsp_suggestions       = 0
let g:ale_sign_error            = '✗'
let g:ale_sign_warning          = '▲'
let g:ale_echo_msg_format       = '[%linter%] %s'

" --- vim-sneak ---
let g:sneak#label = 1
let g:sneak#s_next = 1

" --- startify ---
let g:startify_custom_header = ['', '   WAEHNER', '']
let g:startify_lists = [{ 'type': 'files', 'header': ['   recent'] }]
let g:startify_files_number = 8
let g:startify_change_to_vcs_root = 1
let g:startify_enable_special = 0

" --- vim-which-key ---
let g:which_key_map = {}
nnoremap <silent> <leader> :<C-u>WhichKey '<Space>'<CR>
autocmd! User vim-which-key call which_key#register('<Space>', 'g:which_key_map')

" --- tmux navigator ---
let g:tmux_navigator_no_mappings = 1

" ============================================================
" FILE RUNNER
" ============================================================
function! s:FindRoot(start, marker) abort
  let l:dir = a:start
  while 1
    if filereadable(l:dir . '/' . a:marker)
      return l:dir
    endif
    let l:parent = fnamemodify(l:dir, ':h')
    if l:parent ==# l:dir
      return ''
    endif
    let l:dir = l:parent
  endwhile
endfunction

function! RunFile() abort
  write
  let l:file = expand('%:t')
  let l:out  = expand('%:t:r')
  let l:dir  = expand('%:p:h')
  let l:ft   = &filetype

  " Commands that run from project root
  if l:ft ==# 'rust'
    let l:root = s:FindRoot(l:dir, 'Cargo.toml')
    let l:run_dir = empty(l:root) ? l:dir : l:root
    let l:cmd = 'cd ' . shellescape(l:run_dir) . ' && cargo run'
  elseif l:ft ==# 'go'
    let l:root = s:FindRoot(l:dir, 'go.mod')
    let l:run_dir = empty(l:root) ? l:dir : l:root
    let l:cmd = 'cd ' . shellescape(l:run_dir) . ' && go run .'
  " Commands that run on the file directly
  elseif l:ft ==# 'python'
    let l:cmd = 'cd ' . shellescape(l:dir) . ' && python3 ' . shellescape(l:file)
  elseif l:ft ==# 'javascript'
    let l:cmd = 'cd ' . shellescape(l:dir) . ' && node ' . shellescape(l:file)
  elseif l:ft ==# 'typescript'
    let l:cmd = 'cd ' . shellescape(l:dir) . ' && tsx ' . shellescape(l:file)
  elseif l:ft ==# 'lua'
    let l:cmd = 'cd ' . shellescape(l:dir) . ' && lua ' . shellescape(l:file)
  elseif l:ft ==# 'sh'
    let l:cmd = 'cd ' . shellescape(l:dir) . ' && bash ' . shellescape(l:file)
  elseif l:ft ==# 'c'
    let l:cmd = 'cd ' . shellescape(l:dir) . ' && gcc -std=c11 ' . shellescape(l:file) . ' -o ' . shellescape(l:out) . ' && ./' . shellescape(l:out)
  elseif l:ft ==# 'cpp'
    let l:cmd = 'cd ' . shellescape(l:dir) . ' && g++ ' . shellescape(l:file) . ' -o ' . shellescape(l:out) . ' && ./' . shellescape(l:out)
  else
    echo 'No runner configured for filetype: ' . l:ft
    return
  endif

  " Open terminal split at bottom and run
  botright 15new
  call termopen(l:cmd)
  startinsert
endfunction

" ============================================================
" KEYMAPS
" ============================================================
let mapleader = ' '

" --- fzf ---
nnoremap <leader>ff :Files<CR>
nnoremap <leader>sg :Rg<CR>
nnoremap <leader>fb :Buffers<CR>

" --- terminal ---
nnoremap <leader>tf :botright 15new \| call termopen(&shell) \| startinsert<CR>

" --- file runner ---
nnoremap <leader>tr :call RunFile()<CR>

" --- tmux navigation ---
nnoremap <silent> <C-h> :TmuxNavigateLeft<CR>
nnoremap <silent> <C-j> :TmuxNavigateDown<CR>
nnoremap <silent> <C-k> :TmuxNavigateUp<CR>
nnoremap <silent> <C-l> :TmuxNavigateRight<CR>
nnoremap <silent> <C-\> :TmuxNavigatePrevious<CR>

" --- git hunks (gitgutter) ---
nmap ]h <Plug>(GitGutterNextHunk)
nmap [h <Plug>(GitGutterPrevHunk)
nnoremap <leader>hs :GitGutterStageHunk<CR>
nnoremap <leader>hr :GitGutterUndoHunk<CR>
nnoremap <leader>hp :GitGutterPreviewHunk<CR>
nnoremap <leader>hb :G blame<CR>

" --- marks as harpoon replacement ---
nnoremap <leader>a  ma
nnoremap <M-1>      'a
nnoremap <M-2>      'b
nnoremap <M-3>      'c
nnoremap <M-4>      'd

" --- search ---
nnoremap <leader>sr :vimgrep /\<<C-r><C-w>\>/ **<CR>:copen<CR>
nnoremap <Esc>      :nohlsearch<CR>

" --- quickfix ---
nnoremap <leader>co :copen<CR>
nnoremap <leader>cn :cnext<CR>
nnoremap <leader>cp :cprev<CR>

" --- quit all (mirrors :WQ from neovim config) ---
command! WQ :wa | qa

" ============================================================
" AUTOCMDS
" ============================================================
augroup vim_config
  autocmd!
  " Strip trailing whitespace on save (non-binary files)
  autocmd BufWritePre * if &ft !=# 'diff' | :%s/\s\+$//e | endif
  " Return to last cursor position when reopening a file
  autocmd BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
  " Filetype-specific indent overrides
  autocmd FileType python setlocal shiftwidth=4 tabstop=4 softtabstop=4
  autocmd FileType go     setlocal noexpandtab shiftwidth=4 tabstop=4
augroup END
