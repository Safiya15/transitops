from fastapi import HTTPException, status

from .graph_builder import GraphBuilder
from .dijsktras import Dijkstra


class RouteService:

    async def calculate_route(self, source_id: str, destination_id: str):
        graph = await GraphBuilder().build_graph()

        route = Dijkstra.shortest_path(
            graph,
            str(source_id),
            str(destination_id)
        )

        if route is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No route found between depots"
            )

        total_time = 0
        current_path = route["path"]

        for i in range(len(current_path) - 1):
            current = current_path[i]
            nxt = current_path[i + 1]

            for neighbour, _, avg_time in graph.get(current, []):
                if neighbour == nxt:
                    total_time += avg_time
                    break

        return {
            "path": current_path,
            "distance": route["distance"],
            "estimated_time": total_time
        }
