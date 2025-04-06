import json
from typing import List, Tuple

import pandas as pd
from retrieve import Retriever


class Evaluation:
    def __init__(self, ret: Retriever, questions_df: pd.DataFrame):
        self.ret = ret
        self.questions_df = questions_df

    def __call__(self, metrics):
        return self.eval(metrics)

    def _parse_references(self, references: str):
        return json.loads(references)

    def _intersection(self, range1: Tuple[int, int], range2: Tuple[int, int]):
        start_1, end_1 = range1
        start_2, end_2 = range2

        inter_start = max(start_1, start_2)
        inter_end = min(end_1, end_2)

        if inter_start <= inter_end:
            return inter_start, inter_end
        else:
            return None

    def _union_ranges(self, ranges):
        """
        Merge overlapping or contiguous ranges
        and return a list of non-overlapping intervals.
        """
        if not ranges:
            return []

        # Sort ranges by start index
        sorted_ranges = sorted(ranges, key=lambda x: x[0])
        merged = [sorted_ranges[0]]

        for current in sorted_ranges[1:]:
            prev_start, prev_end = merged[-1]
            curr_start, curr_end = current

            if curr_start <= prev_end:  # Overlapping or contiguous
                merged[-1] = (prev_start, max(prev_end, curr_end))
            else:
                merged.append(current)

        return merged

    def _sum_of_ranges(self, ranges):
        """
        Sum lengths of a list of (start, end) intervals.
        """
        return sum(end - start for start, end in ranges)

    def eval(self, metrics: List[str] = []):
        recall_scores = []
        precision_scores = []

        for idx, entry in self.questions_df.iterrows():
            question = entry["question"]
            ref_chunks = self._parse_references(entry["references"])
            ret_chunks = self.ret.query(question)

            ref_ranges = []
            ret_ranges = []
            intersections = []

            # Build reference ranges
            for ref_chunk in ref_chunks:
                ref_start = int(ref_chunk["start_index"])
                ref_end = int(ref_chunk["end_index"])
                ref_ranges.append((ref_start, ref_end))

            # Build retrieved ranges and compute intersections
            for ret_chunk in ret_chunks:
                ret_start = int(ret_chunk["metadata"]["start_index"])
                ret_end = int(ret_chunk["metadata"]["end_index"])
                ret_range = (ret_start, ret_end)
                ret_ranges.append(ret_range)

                # Check against all reference ranges
                for ref_range in ref_ranges:
                    inter = self._intersection(ref_range, ret_range)
                    if inter:
                        intersections.append(inter)

            # Merge overlaps to avoid double-counting
            ref_union = self._union_ranges(ref_ranges)
            ret_union = self._union_ranges(ret_ranges)
            inter_union = self._union_ranges(intersections)

            total_ref_len = self._sum_of_ranges(ref_union)
            total_ret_len = self._sum_of_ranges(ret_union)
            total_inter_len = self._sum_of_ranges(inter_union)

            recall = total_inter_len / total_ref_len if total_ref_len > 0 else 0
            precision = total_inter_len / total_ret_len if total_ret_len > 0 else 0

            recall_scores.append(recall)
            precision_scores.append(precision)

        avg_recall = sum(recall_scores) / len(recall_scores) if recall_scores else 0
        avg_precision = (
            sum(precision_scores) / len(precision_scores) if precision_scores else 0
        )

        eval_res = {}
        if "recall" in metrics:
            eval_res["recall"] = avg_recall
            eval_res["recall_scores"] = recall_scores

        if "precision" in metrics:
            eval_res["precision"] = avg_precision
            eval_res["precision_scores"] = precision_scores

        return eval_res
