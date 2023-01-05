env_configure:
	pip3 install --upgrade pip \
	&& pip3 install wheel \
	&& pip3 install poetry==1.3.1 \
	&& poetry install

env_install_precommit_hooks:
	pre-commit install && pre-commit install --hook-type commit-msg

env_use:
	poetry shell

env_install_jupyter_extensions:
	jupyter contrib nbextension install --sys-prefix \
	&& jupyter nbextension install --user https://rawgithub.com/minrk/ipython_extensions/master/nbextensions/toc.js \
	&& jupyter nbextension enable --py widgetsnbextension \
	&& jupyter nbextension enable codefolding/main \
	&& jupyter nbextension enable --py keplergl \
	&& jupyter nbextension enable spellchecker/main \
	&& jupyter nbextension enable toggle_all_line_numbers/main \
	&& jupyter nbextension enable hinterland/hinterland \
	&& jt -t grade3

run_streamlit:
	streamlit run --global.developmentMode false src/dashboards/main.py
