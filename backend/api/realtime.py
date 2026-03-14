from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone


def notify_slot_update(space_id, reason='updated'):
    channel_layer = get_channel_layer()
    if not channel_layer:
        return

    async_to_sync(channel_layer.group_send)(
        f'space_slots_{space_id}',
        {
            'type': 'slot_update',
            'space_id': int(space_id),
            'reason': reason,
            'timestamp': timezone.now().isoformat(),
        },
    )
