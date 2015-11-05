import click


logfile_option = click.option('--log-file', type=click.Path(exists=True), help='Set the log file location.')
