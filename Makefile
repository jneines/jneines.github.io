target:=jneines.github.io

all: update_blog_page book

new: clean update_blog_page book

update_blog_page:
	python3 tools/update_blog_page.py

book:
	jupyter-book build $(target)

open:
	open $(target)/_build/html/index.html

clean:
	rm -rf $(target)/_build
