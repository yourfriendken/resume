# LaTeX Resume Templates

This directory contains LaTeX templates for generating professional PDFs of your resume and CV.

## Templates Available

### 1. Modern Resume (`modern-resume.tex`)
- Clean, professional layout suitable for industry positions
- Single-page format optimized for corporate applications
- Modern typography with subtle color accents
- Includes sections for experience, skills, education, and projects

### 2. Academic CV (`academic-cv.tex`)
- Comprehensive format designed for academic positions
- Multi-page layout accommodating extensive publication lists
- Traditional academic styling with proper citation formatting
- Includes sections for research, publications, grants, teaching, and service

## Required Packages

Both templates require the following LaTeX packages:
- `fontawesome` - For icons in contact information
- `geometry` - Page layout and margins
- `hyperref` - Clickable links
- `enumitem` - Customized list formatting
- `etaremune` - Reverse-numbered lists (for academic CV)

## Compilation Instructions

1. **Install LaTeX Distribution**
   - **Windows**: MiKTeX or TeX Live
   - **macOS**: MacTeX
   - **Linux**: TeX Live (usually available via package manager)

2. **Compile the Document**
   ```bash
   pdflatex resume.tex
   ```
   or
   ```bash
   pdflatex cv.tex
   ```

3. **For Bibliography (if needed)**
   ```bash
   pdflatex document.tex
   bibtex document.aux
   pdflatex document.tex
   pdflatex document.tex
   ```

## Customization

### Color Scheme
Modify the color definitions at the top of each file:
```latex
\definecolor{darkblue}{RGB}{0,100,200}
\definecolor{gray}{RGB}{100,100,100}
```

### Fonts
To use different fonts, add font packages:
```latex
\usepackage{lmodern}      % Latin Modern
\usepackage{helvet}       % Helvetica
\usepackage{times}        % Times New Roman
```

### Layout
Adjust margins and spacing:
```latex
\geometry{top=1in, bottom=1in, left=0.8in, right=0.8in}
```

## Template Variables

Replace the placeholder variables `{VARIABLE_NAME}` with your actual data:

**Common Variables:**
- `{NAME}` - Your full name
- `{TITLE}` - Professional title
- `{EMAIL}` - Email address
- `{PHONE}` - Phone number
- `{WEBSITE}` - Personal website
- `{LINKEDIN}` - LinkedIn profile
- `{GITHUB}` - GitHub profile
- `{LOCATION}` - City, State/Country

**Experience Variables:**
- `{POSITION}` - Job title
- `{COMPANY}` - Company name
- `{START_DATE}` - Start date
- `{END_DATE}` - End date
- `{DESCRIPTION}` - Role description
- `{ACHIEVEMENT_1}` - Key achievement

## Automation Ideas

For automated generation from YAML data:
1. Create a Python script using `jinja2` templating
2. Use the YAML data files from `/data/` directory
3. Generate LaTeX files with populated variables
4. Compile to PDF using `subprocess` to call `pdflatex`

Example Python automation script structure:
```python
import yaml
from jinja2 import Template
import subprocess

# Load data
with open('data/personal-info.yml') as f:
    personal_data = yaml.safe_load(f)

# Load template
with open('templates/latex/modern-resume.tex') as f:
    template = Template(f.read())

# Render template
output = template.render(**personal_data)

# Write and compile
with open('output/resume.tex', 'w') as f:
    f.write(output)

subprocess.run(['pdflatex', 'output/resume.tex'])
```

## Tips for Best Results

1. **Proofread Carefully**: LaTeX compilation will fail with syntax errors
2. **Test Compilation**: Always test compile after making changes
3. **Version Control**: Keep your `.tex` files in version control
4. **PDF Output**: Add generated PDFs to `.gitignore` if desired
5. **Backup**: Keep backups of working templates before major changes

## Troubleshooting

**Common Issues:**
- **Missing packages**: Install required packages via your LaTeX distribution
- **Font errors**: Ensure font packages are installed
- **Compilation errors**: Check for unescaped special characters
- **Bibliography issues**: Make sure `.bib` files are properly formatted

**Special Characters:**
Escape these LaTeX special characters in your data:
- `&` → `\&`
- `%` → `\%`
- `$` → `\$`
- `#` → `\#`
- `{` → `\{`
- `}` → `\}`
- `_` → `\_`