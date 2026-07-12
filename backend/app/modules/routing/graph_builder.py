from app.modules.roads.models import Road


class GraphBuilder:

    async def build_graph(self):
        roads = await Road.find(Road.is_active == True).to_list()
        graph = {}

        for road in roads:
            source = str(road.source_depot_id)
            destination = str(road.destination_depot_id)

            if source not in graph:
                graph[source] = []
            if destination not in graph:
                graph[destination] = []

            graph[source].append(
                (
                    destination,
                    road.distance,
                    road.average_time
                )
            )
            graph[destination].append(
                (
                    source,
                    road.distance,
                    road.average_time
                )
            )

        return graph
