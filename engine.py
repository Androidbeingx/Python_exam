"""
Engine module: Uses Markdown and Jinja to put content on templates.
"""

from typing  import Union
from pathlib import Path

import markdown
from   markdown.core    import Markdown

from jinja2             import Environment, BaseLoader, FileSystemLoader, select_autoescape
from jinja2.environment import Template


# -----------------------------------------------------------------------------
# Markdown functions
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
def convert_md_to_html(markdown_string: str) -> str:
    """Input:  Markdown string
       Output: HTML string"""

    md: Markdown = markdown.Markdown(extensions = ['meta'])
    html: str      = md.convert(markdown_string)

    return html


# - 'type: ignore' needed since MyPy complains, but it is correct.
# - raw_metadata is a dict[str, list[str]], but that's cumbersome, so we join the lists.
# -----------------------------------------------------------------------------
def get_md_metadata(markdown_string: str) -> dict[str, str]:
    """Input:  Markdown string
       Output: Dict with all the metada. Keys and values are strings.
       Metadata info: https://python-markdown.github.io/extensions/meta_data/ """

    # Store metadata in md calling .convert()
    md: Markdown = markdown.Markdown(extensions = ['meta'])
    _:  str      = md.convert(markdown_string)

    # Read metadata
    raw_metadata: dict[str, list[str]] = md.Meta   # type: ignore

    # Convert all values from list[str] to str
    joined_metadata: dict[str, str] = {key: ",".join(values) for key, values in raw_metadata.items()}

    return joined_metadata



# -----------------------------------------------------------------------------
# Jinja functions
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
def fill_template_file(template_dir: Union[str, Path], template_filename: str, vars_dict: dict) -> str:
    """ Reads the template and fills it with the contents.
        - template_dir: A directory path relative to main_module_name.
        - template_filename: Template file to fill.
        - vars_dict: Contents to put in the template.
        Keeping the template_dir and filename separate allows template inheritance.
        Autoescapes by default.
        Returns the result as a string.
    """
    
    env:        Environment = Environment( loader=FileSystemLoader(template_dir),
                                           autoescape=select_autoescape() )
    template:   Template    = env.get_template(template_filename)
    filled_str: str         = template.render(vars_dict)

    return filled_str


# -----------------------------------------------------------------------------
def fill_template_str(template_str: str, vars_dict: dict) -> str:
    """ Reads the template and fills it with the contents in vars_dict.
        - template_str: The Jinja template as a string.
        - vars_dict:    Contents to put in the template.
        This function is pure, but does not support template inheritance.
        If there is template inheritance in template_str it throws an error.
        Autoescapes by default.
        Returns the result as a string.
    """
    
    env:        Environment = Environment(loader=BaseLoader(), autoescape=select_autoescape())
    template:   Template    = env.from_string(template_str)
    filled_str: str         = template.render(vars_dict)

    return filled_str


# -----------------------------------------------------------------------------
