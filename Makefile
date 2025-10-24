pages:
	python3 automation/pages_from_csv.py

shorts:
	python3 automation/shorts_from_csv.py

serve:
	cd site_src && hugo server -D

build:
	cd site_src && hugo --minify

deploy:
	git add . && git commit -m "update" && git push
