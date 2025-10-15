#!/usr/bin/env python3
"""
Resume Generator Script

Usage:
    python generate_resume.py --template resume --format all
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
import yaml
from jinja2 import Environment, FileSystemLoader, Template
import markdown
from datetime import datetime

# Add the project root to the path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class ResumeGenerator:
    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = project_root
        self.data_dir = project_root / "data"
        self.templates_dir = project_root / "templates"
        self.output_dir = project_root / "docs"
        
        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader([
                str(self.templates_dir / "markdown"),
                str(self.templates_dir / "html"),
                str(self.templates_dir)
            ]),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.jinja_env.filters['format_date'] = self._format_date
        self.jinja_env.filters['join_list'] = self._join_list
        self.jinja_env.filters['markdown'] = self._markdown_filter
    
    def load_data(self) -> Dict[str, Any]:
        """Load all YAML data files and merge them into a single dictionary."""
        data = {}
        
        # Define the order of data files to load
        data_files = [
            'personal-info.yml',
            'experience.yml',
            'education.yml',
            'skills.yml',
        ]
        
        for filename in data_files:
            file_path = self.data_dir / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_data = yaml.safe_load(f) or {}
                    data.update(file_data)
                    print(f"✓ Loaded {filename}")
            else:
                print(f"⚠ Warning: {filename} not found")
        
        # Add generation metadata
        data['generated_at'] = datetime.now().isoformat()
        data['generator'] = "Resume Generator v1.0"
        
        return data
    
    def _format_date(self, date_str: str) -> str:
        """Format date strings for display."""
        if not date_str or date_str.lower() == 'present':
            return 'Present'
        
        try:
            # Assume YYYY-MM format
            if len(date_str) == 7:  # YYYY-MM
                year, month = date_str.split('-')
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                return f"{months[int(month)-1]} {year}"
            return date_str
        except (ValueError, IndexError):
            return date_str
    
    def _join_list(self, items: List[Any], separator: str = ', ') -> str:
        """Join list items with a separator."""
        if not items:
            return ''
        return separator.join(str(item) for item in items)
    
    def _markdown_filter(self, text: str) -> str:
        """Convert markdown to HTML."""
        return markdown.markdown(text)
    
    def generate_markdown(self, template_name: str, data: Dict[str, Any]) -> str:
        """Generate markdown from template and data."""
        template_file = f"{template_name}.md.jinja"
        
        try:
            template = self.jinja_env.get_template(template_file)
            return template.render(**data)
        except Exception as e:
            print(f"❌ Error generating markdown: {e}")
            raise
    
    def generate_html(self, markdown_content: str, template_name: str = None) -> str:
        """Convert markdown to HTML with optional HTML template."""
        # Convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=['markdown.extensions.tables', 'markdown.extensions.toc']
        )
        
        # If HTML template exists, use it
        if template_name:
            html_template_file = f"{template_name}.html.jinja"
            try:
                html_template = self.jinja_env.get_template(html_template_file)
                return html_template.render(content=html_content)
            except:
                print(f"⚠ HTML template {html_template_file} not found, using basic HTML")

    
    def generate_resume(self, template_name: str, formats: List[str]) -> Dict[str, Path]:
        """Generate resume in specified formats."""
        print(f"🚀 Generating resume using template: {template_name}")
        
        # Load data
        data = self.load_data()
        
        # Generate markdown
        markdown_content = self.generate_markdown(template_name, data)
        
        output_files = {}
        
        # Save markdown
        if 'markdown' in formats or 'all' in formats:
            md_path = self.output_dir / f"resume.md"
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            output_files['markdown'] = md_path
            print(f"✓ Generated markdown: {md_path}")
        
        # Generate and save HTML
        if 'html' in formats or 'all' in formats:
            html_content = self.generate_html(markdown_content, template_name)
            html_path = self.output_dir / f"index.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            output_files['html'] = html_path
            print(f"✓ Generated HTML: {html_path}")
        
        return output_files

def main():
    parser = argparse.ArgumentParser(description='Generate resume from YAML data')
    parser.add_argument('--template', '-t', default='resume', help='Template name (without extension)')
    parser.add_argument('--format', '-f', choices=['markdown', 'html', 'all'], default='all', help='Output format(s)')
    parser.add_argument('--list-templates', action='store_true', help='List available templates')
    args = parser.parse_args()
    generator = ResumeGenerator()
    
    if args.list_templates:
        # List available templates
        templates_dir = generator.templates_dir / "markdown"
        if templates_dir.exists():
            print("📄 Available templates:")
            for template_file in templates_dir.glob("*.md.jinja"):
                print(f"  - {template_file.stem}")
        return
    
    try:
        formats = [args.format] if args.format != 'all' else ['markdown', 'html']
        output_files = generator.generate_resume(args.template, formats)
        
        print(f"\n🎉 Resume generation complete!")
        print(f"📁 Output directory: {generator.output_dir}")
        for format_type, file_path in output_files.items():
            print(f"   {format_type.upper()}: {file_path.name}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()