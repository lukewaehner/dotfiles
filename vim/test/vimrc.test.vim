" Regression tests for ~/.vimrc behaviour.
"
" Run:  vim -es -u vim/.vimrc -S vim/test/vimrc.test.vim </dev/null; echo $?
" Exits 0 on success, 1 on failure, and prints failures to stderr.

let s:failures = []

function! s:Assert(cond, msg) abort
  if !a:cond
    call add(s:failures, a:msg)
  endif
endfunction

function! s:AssertEqual(got, want, msg) abort
  call s:Assert(a:got ==# a:want,
        \ printf('%s: expected %s, got %s', a:msg, string(a:want), string(a:got)))
endfunction

function! s:Tempfile(lines) abort
  let l:path = tempname() . '.txt'
  call writefile(a:lines, l:path)
  return l:path
endfunction

" --- BufWritePre trailing-whitespace strip -------------------------------

function! s:TestStripRemovesTrailingWhitespace() abort
  let l:path = s:Tempfile(['alpha   ', 'beta', 'gamma  '])
  execute 'edit!' fnameescape(l:path)
  silent write
  call s:AssertEqual(readfile(l:path), ['alpha', 'beta', 'gamma'],
        \ 'strip removes trailing whitespace on save')
endfunction

function! s:TestStripPreservesSearchPattern() abort
  let l:path = s:Tempfile(['alpha   ', 'beta', 'gamma  '])
  execute 'edit!' fnameescape(l:path)
  let @/ = 'beta'
  silent write
  call s:AssertEqual(@/, 'beta',
        \ 'strip leaves the last search pattern alone (hlsearch must not jump to \s\+$)')
endfunction

function! s:TestStripPreservesCursorPosition() abort
  let l:path = s:Tempfile(['alpha   ', 'beta', 'gamma  ', 'delta', 'epsilon'])
  execute 'edit!' fnameescape(l:path)
  call cursor(2, 3)
  silent write
  call s:AssertEqual(getpos('.')[1:2], [2, 3],
        \ 'strip restores the cursor position after save')
endfunction

function! s:TestStripSkipsDiffFiletype() abort
  let l:path = s:Tempfile(['+ added   ', '- removed  '])
  execute 'edit!' fnameescape(l:path)
  setlocal filetype=diff
  silent write
  call s:AssertEqual(readfile(l:path), ['+ added   ', '- removed  '],
        \ 'strip leaves diff buffers untouched')
endfunction

" --- run -----------------------------------------------------------------

call s:TestStripRemovesTrailingWhitespace()
call s:TestStripPreservesSearchPattern()
call s:TestStripPreservesCursorPosition()
call s:TestStripSkipsDiffFiletype()

" `vim -es` swallows :echo, so report through stderr directly.
if empty(s:failures)
  call writefile(['ok - ' . '4 vimrc tests passed'], '/dev/stderr')
  qall!
else
  call writefile(map(copy(s:failures), '"FAIL " . v:val'), '/dev/stderr')
  cquit!
endif
