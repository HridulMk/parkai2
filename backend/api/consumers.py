from channels.generic.websocket import AsyncJsonWebsocketConsumer


class SpaceSlotsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.space_id = self.scope['url_route']['kwargs']['space_id']
        self.group_name = f'space_slots_{self.space_id}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_json({'type': 'connected', 'space_id': int(self.space_id)})

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def slot_update(self, event):
        await self.send_json({
            'type': 'slot_update',
            'space_id': event.get('space_id'),
            'reason': event.get('reason', 'updated'),
            'timestamp': event.get('timestamp'),
        })
