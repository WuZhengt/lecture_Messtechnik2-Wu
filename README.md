# Lecture "Messtechnik 2"

This repository contains the LaTeX Beamer based slides as well as PYTHON/Jupyter based notebooks for the lecture "Messung nichtelektrischer Größen und Sensorik".

## Compile
- Tested with MikTeX on Windows and texlive on Ubuntu 19.10
- Compilation process can be determined from VisualStudio Code workspace settings localted in `.vscode/settings.json` 
### First Compile after Cloning Repository
- build the latex `*.fmt` file, see instructions in `mybeamer.tex`
- initialize local submodules configuration file via `git submodule init`
- fetch all submodule data and check out the appropriate commit via `git submodule update`


### LaTeX Predefined Format
- to speedup compilation, this project uses a predefined LaTeX format
- i.e. most packages, in particular the beamer package, is preloaded in the format file
- refer also to https://ctan.org/pkg/mylatexformat
- the workflow needs compilation with pdflatex


## LaTex Coding Guidelines/Best Practice

### Images
- all images shall be placed in the sub-folder `fig` of the respective section folder
- images taken from books/articles/papers shall be named according to `<bibtexkey>_<figure_label>_<number>`, where `<bibtexkey>` is the Bibtex key of the document in the file `references.bib` (any reference used needs to be listed in there), `<figure_label>` is, e.g., one of `{fig, abb}` (depending whether it's an english or german text) and `<number>` is the corresponding number of the item in that document; e.g. if *Abb. 2.1* of the book *``Elektrische Messtechnik``, Thomas Mühl, Springer Fachmedien Wiesbaden* shall be included in the slides, the figure should be saved as `muhl2017_abb_2_1.png` (or `*.pdf`)
- if images are exported from exiting PowerPoint or lecture slides, a meaningful prefix shall be used, e.g., `slides_messtechnik1_ws21_<slide_number>`

## Setting up Python Environment
- use Anaconda distribution
- change to root directory of project
- create predefined environment `lecture_remote_sensing` by `conda env create environment.yml`
- activate environmen `conda activate lecture_remote_sensing`
  
### Additions for Development and Source Control
- Jupyter Lab typically also saves the outputs (plots, etc.) of the notebooks
- This can however bloat the files under source control
- Therefore, before checking in any `*.ipynb` files, they shall be saved with all outputs cleared `Edit -> Clear All Outputs`
- To **automatically** let Jupyter clear all outputs on save, add the following configuration
    - create a defalut jupyter lab configuration (can be executed from any venv)
    ``` bash
        jupyter notebook --generate-config
    ```
    - this will create a jupyter config file `~/.jupyter/jupyter_notebook_config.py` 
    - add the following lines to this `jupyter_notebook_config.py`
    ``` python
        def scrub_output_pre_save(model, **kwargs):
        """scrub output before saving notebooks"""
        # only run on notebooks
        if model['type'] != 'notebook':
            return
        # only run on nbformat v4
        if model['content']['nbformat'] != 4:
            return
    
        for cell in model['content']['cells']:
            if cell['cell_type'] != 'code':
                continue
            cell['outputs'] = []
            cell['execution_count'] = None
    
        c.FileContentsManager.pre_save_hook = scrub_output_pre_save
    ```
    - restart jupyter lab to apply settings