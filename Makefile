target:=jneines.github.io
all: book

new: clean book

book:
	jupyter-book build $(target)

open:
	open $(target)/_build/html/index.html

clean:
	rm -rf $(target)/_build
