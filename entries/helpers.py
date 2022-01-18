from logging import getLogger

from entries.models import Entry

logger = getLogger(__name__)


def process_action(action: str) -> tuple:
    """
    Processes an action string from an exported modlog and converts it into a format that can be loaded into the DB.

    :param action: An action string, such as "Warn" or "14 day ban"
    :return: A tuple containing an Entry.ACTION_CHOICE and a ban length/None.
    """
    if action.title() == 'Permaban':
        return Entry.ACTION_PERM_BAN, None
    elif action.title() == 'Warn':
        return Entry.ACTION_WARN, None
    else:
        if len(action.split(' ')) > 1:
            try:
                return Entry.ACTION_TEMP_BAN, int(action.split(' ')[0])
            except ValueError:
                # This is something unexpected, so making it a warning.
                logger.error(f'Encountered unknown action `{action}`. Setting as warning.')
                return Entry.ACTION_WARN, None

        raise ValueError(f'Could not process {action}')
