from sqlalchemy import and_
from lds.app import db
from lds.app.models import Event, load_user


def log_event(user, module, message):
    event = Event(user_id=user.id, module=module, message=message)
    db.session.add(event)
    db.session.commit()


def get_events(module=None, user=None, time_earliest=None, time_latest=None):
    filters = []
    if module is not None:
        filters.append(Event.module == module)
    if user is not None:
        filters.append(Event.user_id == user.id)
    if time_earliest is not None:
        filters.append(Event.timestamp >= time_earliest)
    if time_latest is not None:
        filters.append(Event.timestamp <= time_latest)

    query = db.session.query(Event).filter(and_(*filters))

    events = []

    for row in query:
        event = {
            'id': row.id,
            'timestamp': row.timestamp,
            'module': row.module,
            'message': row.message,
            'user': load_user(row.user_id)
        }
        events.append(event)
    return events
