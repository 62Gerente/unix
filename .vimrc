colorscheme jellybeans
set t_Co=256
:syntax on        "Turn on syntax highlighting
:set laststatus=2 "Always show status line

:set autowrite    "Automatically write a file when leaving a modified buffer
:set confirm      "Start a dialog when a command fails (here when quit command fails)
:set tabstop=4    "Number of spaces a TAB in the text stands for

:set shiftwidth=4 "Number of spaces used for each step of (auto)indent
:set hlsearch     "Have vim highlight the target of a search
:set incsearch    "Do incremental searching

:set ruler        "Show the cursor position all the time
:set number       "Show line numbers
:set ignorecase   "Ignore case when searching

:set mouse=a
:set clipboard=unnamed

:set title        "Show info in the window title
:set titlestring=PANKAJ:\ %F   
			      "Automatically set screen title
    
"Indent only if the file is of type cpp,c,java,sh,pl,php,asp
    :au FileType cpp,c,java,sh,pl,php,asp  set autoindent
    :au FileType cpp,c,java,sh,pl,php,asp  set smartindent
    :au FileType cpp,c,java,sh,pl,php,asp  set cindent

    "Wrapping long lines
    :set wrapmargin=4   "Margin from the right in which to break a line. Set
"    :set textwidth=70   "Line length above which to break a line
    
	"Defining abbreviations
    :ab #d #define
    :ab #i #include
	
	"Defining mine abbreviations
	:ab #p printf("%");

    "Defining abbreviations to draw comments
    :ab #b /********************************
    :ab #e ********************************/
    :ab #l /*-------------------- --------------------*/
	    

	" Converting tabs to spaces
    :au FileType cpp,c,java,sh,pl,php,asp,fl  set expandtab   "Converting tabs to spaces

call pathogen#infect()

""NERD TREE

" Give a shortcut key to NERD Tree
map <F2> :NERDTreeToggle<CR>

"Show hidden files in NerdTree  
let NERDTreeShowHidden=1
 
"autopen NERDTree and focus cursor in new document  
"autocmd VimEnter * NERDTree  
"autocmd VimEnter * wincmd p

"" FILETYPE

au BufNewFile,BufRead *.fl set ft=cpp
