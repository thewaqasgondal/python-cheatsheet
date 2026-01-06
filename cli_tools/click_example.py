"""
Command-Line Interfaces with Click

This module demonstrates comprehensive usage of the Click library
for building modern command-line interfaces in Python.
"""

import click
import os
import json
import time
from typing import List, Optional, Any
from pathlib import Path


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """A modern CLI tool built with Click."""
    pass


@cli.command()
@click.argument('name', default='World')
@click.option('--count', '-c', default=1, type=int,
              help='Number of greetings.')
@click.option('--verbose', '-v', is_flag=True,
              help='Enable verbose output.')
def greet(name: str, count: int, verbose: bool):
    """Simple greeting command."""
    click.echo(f"Greet command called with: name={name}, count={count}, verbose={verbose}")

    for i in range(count):
        greeting = f"Hello, {name}!"
        if verbose:
            greeting += f" (#{i+1})"
        click.echo(greeting)


@cli.command()
@click.argument('operation', type=click.Choice(['add', 'sub', 'mul', 'div']))
@click.argument('numbers', nargs=-1, type=float)
@click.option('--precision', '-p', default=2, type=int,
              help='Decimal precision for result.')
def calc(operation: str, numbers: List[float], precision: int):
    """Perform mathematical operations on numbers."""
    if len(numbers) < 2:
        click.echo("Error: Need at least 2 numbers", err=True)
        return

    try:
        if operation == 'add':
            result = sum(numbers)
        elif operation == 'sub':
            result = numbers[0] - sum(numbers[1:])
        elif operation == 'mul':
            result = 1.0
            for num in numbers:
                result *= num
        elif operation == 'div':
            result = numbers[0]
            for num in numbers[1:]:
                if num == 0:
                    raise ZeroDivisionError("Division by zero")
                result /= num

        click.echo(f"Result: {result:.{precision}f}")

    except ZeroDivisionError as e:
        click.echo(f"Error: {e}", err=True)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(),
              help='Output file path.')
@click.option('--format', '-f',
              type=click.Choice(['txt', 'json', 'csv']),
              default='txt',
              help='Output format.')
@click.option('--force', '-F', is_flag=True,
              help='Overwrite output file if it exists.')
def process(input_file: str, output: Optional[str], format: str, force: bool):
    """Process a file with various output formats."""
    input_path = Path(input_file)

    # Determine output path
    if output:
        output_path = Path(output)
    else:
        output_path = input_path.with_suffix(f'.{format}')

    # Check if output exists
    if output_path.exists() and not force:
        if not click.confirm(f"Output file {output_path} exists. Overwrite?"):
            click.echo("Operation cancelled.")
            return

    try:
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.splitlines()
        word_count = len(content.split())
        char_count = len(content)

        # Process based on format
        if format == 'txt':
            output_content = f"""File: {input_path.name}
Lines: {len(lines)}
Words: {word_count}
Characters: {char_count}

Content preview:
{content[:200]}{'...' if len(content) > 200 else ''}
"""

        elif format == 'json':
            data = {
                'filename': input_path.name,
                'path': str(input_path),
                'stats': {
                    'lines': len(lines),
                    'words': word_count,
                    'characters': char_count
                },
                'content': content
            }
            output_content = json.dumps(data, indent=2, ensure_ascii=False)

        elif format == 'csv':
            output_content = "metric,value\n"
            output_content += f"lines,{len(lines)}\n"
            output_content += f"words,{word_count}\n"
            output_content += f"characters,{char_count}\n"

        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_content)

        click.echo(f"Processed {input_path} -> {output_path}")
        click.echo(f"Format: {format}, Lines: {len(lines)}, Words: {word_count}")

    except Exception as e:
        click.echo(f"Error processing file: {e}", err=True)


@cli.command()
@click.option('--host', default='localhost', help='Server host.')
@click.option('--port', default=8080, type=int, help='Server port.')
@click.option('--debug', is_flag=True, help='Enable debug mode.')
@click.option('--workers', '-w', default=1, type=int,
              help='Number of worker processes.')
def serve(host: str, port: int, debug: bool, workers: int):
    """Start a simple web server."""
    click.echo(f"Starting server on {host}:{port}")
    click.echo(f"Debug mode: {debug}")
    click.echo(f"Workers: {workers}")

    # Simulate server startup
    with click.progressbar(range(100), label='Starting server...') as bar:
        for i in bar:
            time.sleep(0.01)  # Simulate work

    click.echo("Server started successfully!")
    click.echo("Press Ctrl+C to stop...")

    # In a real implementation, this would start the actual server
    # For demo purposes, we'll just wait
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo("\nServer stopped.")


@cli.command()
@click.argument('path', type=click.Path())
@click.option('--pattern', '-p', default='*',
              help='File pattern to match.')
@click.option('--recursive', '-r', is_flag=True,
              help='Search recursively.')
@click.option('--type', '-t',
              type=click.Choice(['file', 'dir', 'all']),
              default='all',
              help='Type of items to list.')
def find(path: str, pattern: str, recursive: bool, type: str):
    """Find files and directories."""
    search_path = Path(path)

    if not search_path.exists():
        click.echo(f"Error: Path {path} does not exist", err=True)
        return

    # Simple glob-based search (in real implementation, use more sophisticated matching)
    if recursive:
        if type == 'file':
            items = list(search_path.rglob(pattern))
            items = [item for item in items if item.is_file()]
        elif type == 'dir':
            items = list(search_path.rglob(pattern))
            items = [item for item in items if item.is_dir()]
        else:
            items = list(search_path.rglob(pattern))
    else:
        if type == 'file':
            items = list(search_path.glob(pattern))
            items = [item for item in items if item.is_file()]
        elif type == 'dir':
            items = list(search_path.glob(pattern))
            items = [item for item in items if item.is_dir()]
        else:
            items = list(search_path.glob(pattern))

    if not items:
        click.echo("No items found.")
        return

    click.echo(f"Found {len(items)} items in {path}:")
    for item in sorted(items):
        item_type = "DIR" if item.is_dir() else "FILE"
        click.echo(f"  {item_type}  {item}")


@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True),
              help='Configuration file path.')
@click.option('--env-prefix', default='APP_',
              help='Environment variable prefix.')
@click.pass_context
def config(ctx: click.Context, config: Optional[str], env_prefix: str):
    """Display current configuration."""
    click.echo("Current Configuration:")
    click.echo("-" * 30)

    # Load from config file if provided
    config_data = {}
    if config:
        try:
            with open(config, 'r') as f:
                if config.endswith('.json'):
                    config_data = json.load(f)
                else:
                    # Simple key=value format
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            config_data[key.strip()] = value.strip()
        except Exception as e:
            click.echo(f"Error reading config file: {e}", err=True)
            return

    # Override with environment variables
    for key, value in os.environ.items():
        if key.startswith(env_prefix):
            config_key = key[len(env_prefix):].lower()
            config_data[config_key] = value

    # Display configuration
    if config_data:
        for key, value in sorted(config_data.items()):
            click.echo(f"{key}: {value}")
    else:
        click.echo("No configuration found.")

    # Show command context
    click.echo(f"\nCommand context: {ctx.invoked_subcommand}")


@cli.command()
@click.option('--style', type=click.Choice(['simple', 'rich', 'minimal']),
              default='simple', help='Progress bar style.')
@click.option('--total', '-n', default=100, type=int,
              help='Total items to process.')
@click.option('--delay', '-d', default=0.01, type=float,
              help='Delay between items (seconds).')
def progress(style: str, total: int, delay: float):
    """Demonstrate different progress bar styles."""
    click.echo(f"Processing {total} items with {style} style...")

    if style == 'simple':
        with click.progressbar(range(total)) as bar:
            for item in bar:
                time.sleep(delay)

    elif style == 'rich':
        with click.progressbar(range(total),
                              label='Processing',
                              fill_char='█',
                              empty_char='░') as bar:
            for item in bar:
                time.sleep(delay)

    elif style == 'minimal':
        for i in range(total):
            if i % 10 == 0:
                click.echo(f"Progress: {i}/{total}", nl=False, err=True)
                click.echo('\r', nl=False, err=True)
            time.sleep(delay)
        click.echo(f"Progress: {total}/{total}", err=True)

    click.echo("Processing complete!")


def main():
    """Entry point for the CLI application."""
    # In a real application, this would be:
    # cli()
    # But for demonstration, we'll show help
    click.echo("Click CLI Examples")
    click.echo("=" * 40)
    click.echo()

    # Show help
    click.echo("Available commands:")
    click.echo("  greet     Simple greeting command")
    click.echo("  calc      Mathematical calculator")
    click.echo("  process   File processing with multiple formats")
    click.echo("  serve     Start a web server")
    click.echo("  find      Find files and directories")
    click.echo("  config    Display configuration")
    click.echo("  progress  Demonstrate progress bars")
    click.echo()

    # Demonstrate some commands programmatically
    click.echo("Demonstrating commands:")
    click.echo()

    # Test greet command
    click.echo("1. Testing greet command:")
    try:
        # Use Click's testing utilities
        from click.testing import CliRunner
        runner = CliRunner()
        result = runner.invoke(cli, ['greet', 'Alice', '--count', '2', '--verbose'])
        click.echo(result.output)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
    click.echo()

    # Test calc command
    click.echo("2. Testing calc command:")
    try:
        runner = CliRunner()
        result = runner.invoke(cli, ['calc', 'add', '10', '20', '5'])
        click.echo(result.output)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
    click.echo()

    # Test progress command
    click.echo("3. Testing progress command (shortened):")
    try:
        runner = CliRunner()
        result = runner.invoke(cli, ['progress', '--total', '5', '--delay', '0.001'])
        click.echo(result.output)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    main()