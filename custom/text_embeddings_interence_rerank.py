from typing import List
from llama_index.core.schema import NodeWithScore, QueryBundle
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.callbacks import CBEventType, EventPayload
from llama_index.core.bridge.pydantic import Field


class TEIRanker(BaseNodePostprocessor):
    base_url: str = Field(
        description="The base url of the text embeddings inference service"
    )
    batch_size: int = Field(
        description="The batch size of the text embeddings inference service",
        default=32,
    )
    top_k: int = Field(
        description="The number of nodes to keep after reranking",
        default=3,
    )
    threshold: float = Field(
        description="The threshold of the reranking",
        default=0.0,
    )

    def __init__(
        self,
        base_url: str,
        batch_size: int = 32,
        top_k: int = 3,
        threshold: float = 0.0,
    ):
        super().__init__(
            base_url=base_url,
            batch_size=batch_size,
            top_k=top_k,
            threshold=threshold,
        )

    @classmethod
    def class_name(cls) -> str:
        return "TEIRanker"

    def _postprocess_nodes(
        self, nodes: List[NodeWithScore], query_bundle: QueryBundle | None = None
    ) -> List[NodeWithScore]:
        import httpx

        with self.callback_manager.event(
            CBEventType.RERANKING,
            payload={
                EventPayload.NODES: nodes,
                EventPayload.QUERY_STR: query_bundle.query_str,
            },
        ) as event:
            context = [node.text for node in nodes]
            query = query_bundle.query_str
            with httpx.Client() as client:
                response = client.post(
                    f"{self.base_url}/rerank",
                    json={
                        "texts": context,
                        "query": query,
                        "raw_scores": False,
                        "truncate": True,
                    },
                )
                response.raise_for_status()
            results = response.json()
            # print(results)

            new_nodes = []
            for result in results:
                if result["score"] > self.threshold:
                    new_nodes.append(
                        NodeWithScore(
                            node=nodes[int(result["index"])].node, score=result["score"]
                        )
                    )
            event.on_end(payload={EventPayload.NODES: new_nodes[: self.top_k]})
        return new_nodes[: self.top_k]
