import heapq


class Dijkstra:

    @staticmethod
    def shortest_path(graph, source, destination):
        priority_queue = [(0, source, [])]
        visited = set()

        while priority_queue:
            distance, node, path = heapq.heappop(priority_queue)

            if node in visited:
                continue

            visited.add(node)
            path = path + [node]

            if node == destination:
                return {
                    "distance": distance,
                    "path": path
                }

            for neighbour, edge_distance, _ in graph.get(node, []):
                if neighbour not in visited:
                    heapq.heappush(
                        priority_queue,
                        (
                            distance + edge_distance,
                            neighbour,
                            path
                        )
                    )

        return None
