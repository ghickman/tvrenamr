def start_dry_run(logger):
    logger('Dry Run beginning.')
    logger('-' * 70)
    logger('')


def stop_dry_run(logger):
    logger('')
    logger('-' * 70)
    logger('Dry Run complete. No files were harmed in the process.')
    logger('')
