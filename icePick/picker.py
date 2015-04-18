import asyncio
import aiohttp

__all__ = ('Picker')


class Picker:
    def __init__(self, orders):
        self.orders = orders
        self.loop = asyncio.get_event_loop()

    def run(self, is_event_close=True):
        result = asyncio.wait(self.get_orders_with_async(), loop=self.loop)
        self.loop.run_until_complete(result)

        if is_event_close:
            self.loop.close()

    def get_orders_with_async(self):
        return [asyncio.async(self._dispatch(order)) for order in self.orders]

    @asyncio.coroutine
    def _dispatch(self, order):
        html = yield from self._download(url=order.url, method=order.method.value, headers=order.get_headers())
        result = order.parse(html.decode(order.charset, 'ignore'))
        order.save(result)

    @asyncio.coroutine
    def _download(self, method, *args, **kwargs):
        response = yield from aiohttp.request(method, *args, **kwargs)
        return (yield from response.read_and_close())
