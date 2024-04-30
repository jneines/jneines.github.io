# Example:
# https://jneines.github.io/blog/2024/20240501-later/20240501-later.html

# Strategy is to scan the checked out local copy of the blog book for blog items,
# render a card per item and add a link to the rendered online version

from pathlib import Path
from collections import defaultdict

from loguru import logger

# base url to the blog book living in gh-pages
online_base_url = "https://jneines.github.io/blog"
# local base directory for the checked-out homepage repo
homepage_base_dir = Path("jneines.github.io")
# local base directory for the checked-out blog repo
blog_base_dir = Path("../../blog/blog")

# A model to hold all blog items in a structured manner.
# There will be a list of tuples for every year
# Each tuple contains the date string and the path to the blog.
# This way, the model can easily be sorted

blog_model = defaultdict(list)

# The toc model is used to create the _toc.yml file later.
# It will be populated based on the contents of the blog_model
blog_page_model = [
    "# Blog",  # Title of the overview page
    "",
    "::::{grid} 1",  # Structure page using a grid
    ":gutter: 3",
    "",
]

# find all abstracts belonging to the blog items and add them to the blog_model
abstract_paths = blog_base_dir.glob("20??/20??????-*/abstract.md")
for abstract_path in abstract_paths:
    logger.debug(f"Found {abstract_path=}")

    abstract = abstract_path.open("r").read()
    logger.debug(f"{abstract=}")

    *_, year_dir, blog_dir, abstract_filename = abstract_path.parts
    date_str, blog_title = blog_dir.split("-")
    logger.debug(f"{date_str=}, {blog_title=}")

    # The target_blog_path is the document to link to.
    # Instead of the 'abstract.md' we use the file with the real content.
    # It's expected that the name of the file is equal to the directory name.
    target_blog_path = abstract_path.parent / f"{blog_dir}.html"

    # The relative path is the part to append to the 'online_base_url'
    # to complete the online_url
    rel_path = target_blog_path.relative_to(blog_base_dir)
    online_url = f"{online_base_url}/{rel_path.as_posix()}"
    logger.debug(f"{online_url=}")

    # Add all known to the blog_model
    year_str = year_dir
    blog_model[year_str].append((date_str, blog_title, online_url, abstract))

logger.debug(blog_model)


# Now iterate the blog_model in reversed order

for year_str in sorted(blog_model.keys())[::-1]:
    for date_str, blog_title, online_url, abstract in sorted(blog_model[year_str])[
        ::-1
    ]:
        # Create a clickable 'grid-item-card' for every blog entry
        blog_page_model.append(f":::{{grid-item-card}} {date_str} - **{blog_title}**")
        blog_page_model.append(f":link: {online_url}")
        blog_page_model.append(abstract)
        blog_page_model.append("")
        blog_page_model.append(":::")
        blog_page_model.append("")

# Finalize the grid
blog_page_model.append("::::")

logger.debug(f"page contents: {"\n".join(blog_page_model)}")

# Update the blog overview page
with (homepage_base_dir / "blog.md").open("w") as fd:
    fd.write("\n".join(blog_page_model))
