# Kenneth Jones's Resume

Scripts to generate my resume in various formats.

## Dependencies

- [Pandoc](https://pandoc.org/) - for converting to other formats
    ```zsh
    brew install pandoc
    ```

- [MacTeX](https://www.tug.org/mactex/) - for generating PDF
    ```zsh
    brew install --cask mactex
    ```

- Python 3.14 (just because it is π version of Python)
    ```zsh
    brew install python@3.14
    ```
    - Python packages:
        - [Jinja2](https://jinja.palletsprojects.com/en/stable/intro/) - for templating
        - [PyYAML](https://pyyaml.org/) - for parsing YAML
        - [Markdown](https://python-markdown.github.io/) - for parsing Markdown

- [Taskfile](https://taskfile.dev/) - for running command line shortcuts
    ```zsh
    brew install task
    ```

## Usage


Generate the resume documents in HTML, PDF, and Markdown formats, and open a preview server to view the HTML version.

```zsh
task all
```

Generate Markdown and HTML documents.

```zsh
task generate
```

Create a PDF using the generated HTML applying latex template using Pandoc.

```zsh
task pdf
```

Open a local web server to preview the HTML version of the resume.

```zsh
task preview
```
