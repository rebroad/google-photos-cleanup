from __future__ import annotations

from datetime import datetime, timezone
from pathlib import PurePosixPath

from .fingerprint import hamming
def _media_kind(item: dict[str, object]) -> str | None:
    mime_type = str(item.get("mime_type", "")).lower()
    if mime_type.startswith("video/"):
        return "video"
    if mime_type.startswith("image/"):
        return "image"
    extension = str(item.get("extension", item.get("filename", ""))).lower()
    return "video" if extension.rsplit(".", 1)[-1] in {"3gp", "avi", "m4v", "mkv", "mov", "mp4", "webm"} else ("image" if "." in extension else None)

def _compatible(local: dict[str, object], remote: dict[str, object]) -> bool:
    local_kind = _media_kind(local)
    remote_kind = _media_kind(remote)
    return local_kind is None or remote_kind is None or local_kind == remote_kind



def normalize(items: list[dict[str, object]]) -> list[dict[str, object]]:
    """Normalize adapter output without retaining access tokens or URLs to bytes.

    Accepted fields: id, filename, size, mime_type, creation_time, sha256,
    product_url. Unknown fields are discarded deliberately.
    """
    result = []
    for item in items:
        filename = str(item.get("filename", ""))
        result.append({key: item[key] for key in ("id", "filename", "size", "mime_type", "creation_time", "sha256", "product_url", "content_url", "phash", "width", "height") if key in item and item[key] is not None} | {"basename": PurePosixPath(filename).name})
    return result


def _timestamp(value: object) -> float | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).replace(tzinfo=timezone.utc if "+" not in str(value) else None).timestamp()
    except ValueError:
        return None


def duplicate_groups(items: list[dict[str, object]], threshold: int = 24) -> list[dict[str, object]]:
    """Return same-kind duplicate groups using exact or perceptual evidence."""
    eligible = [item for item in items if _media_kind(item) and (item.get("sha256") or item.get("phash"))]
    parent = list(range(len(eligible)))

    def root(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def join(left: int, right: int) -> None:
        left_root, right_root = root(left), root(right)
        if left_root != right_root:
            parent[right_root] = left_root

    by_kind: dict[str, list[int]] = {}
    for index, item in enumerate(eligible):
        kind = _media_kind(item)
        if kind:
            by_kind.setdefault(kind, []).append(index)

    for indices in by_kind.values():
        by_sha: dict[str, list[int]] = {}
        for index in indices:
            sha = str(eligible[index].get("sha256", "")).lower()
            if sha:
                by_sha.setdefault(sha, []).append(index)
        for group in by_sha.values():
            for index in group[1:]:
                join(group[0], index)

        phash_items = [index for index in indices if eligible[index].get("phash")]
        if not phash_items:
            continue
        block_count = max(1, threshold + 1)
        hash_values: dict[int, int] = {}
        hash_lengths: dict[int, int] = {}
        for index in phash_items:
            value = str(eligible[index]["phash"])
            try:
                hash_values[index] = int(value, 2)
                hash_lengths[index] = len(value)
            except ValueError:
                continue
        buckets: dict[tuple[int, str], list[int]] = {}
        for index in phash_items:
            if index not in hash_values:
                continue
            value = str(eligible[index]["phash"])
            value_int = hash_values[index]
            block_width = max(1, (len(value) + block_count - 1) // block_count)
            seen: set[int] = set()
            for block in range(block_count):
                start = block * block_width
                if start >= len(value):
                    break
                key = (block, value[start:start + block_width])
                for candidate in buckets.get(key, []):
                    if candidate not in seen and (value_int ^ hash_values[candidate]).bit_count() + abs(len(value) - hash_lengths[candidate]) <= threshold:
                        join(index, candidate)
                    seen.add(candidate)
                buckets.setdefault(key, []).append(index)

    grouped: dict[int, list[dict[str, object]]] = {}
    for index, item in enumerate(eligible):
        grouped.setdefault(root(index), []).append(item)
    return [
        {"group_id": f"duplicates:{group_index}", "items": group}
        for group_index, group in enumerate(grouped.values(), 1)
        if len(group) > 1
    ]


def match(local: list[dict[str, object]], remote: list[dict[str, object]], tolerance_seconds: int = 172800) -> list[dict[str, object]]:
    by_hash: dict[str, list[dict[str, object]]] = {}
    by_name: dict[str, list[dict[str, object]]] = {}
    for item in remote:
        if item.get("sha256"):
            by_hash.setdefault(str(item["sha256"]).lower(), []).append(item)
        by_name.setdefault(str(item.get("basename", item.get("filename", ""))).casefold(), []).append(item)
    output = []
    for file in local:
        evidence: list[str] = []
        candidates = []
        digest = str(file.get("sha256", "")).lower()
        if digest and digest in by_hash:
            candidates = [candidate for candidate in by_hash[digest] if _compatible(file, candidate)]
            evidence.append("sha256")
            confidence = "high"
        else:
            local_name = str(file.get("filename", "")).casefold()
            candidates = [candidate for candidate in by_name.get(local_name, []) if _compatible(file, candidate)] if local_name else []
            confidence = "review"
            for candidate in candidates:
                if file.get("size") is not None and candidate.get("size") == file.get("size"):
                    evidence.append("size")
                local_time = float(file.get("mtime", 0))
                remote_time = _timestamp(candidate.get("creation_time"))
                if remote_time is not None and abs(local_time - remote_time) <= tolerance_seconds:
                    evidence.append("creation_time")
            if {"size", "creation_time"}.issubset(evidence):
                confidence = "medium"
        if file.get("phash"):
            local_phash = str(file["phash"])
            perceptual = [
                candidate for candidate in remote
                if _compatible(file, candidate)
                and candidate.get("phash")
                and hamming(local_phash, str(candidate["phash"])) <= 24
            ]
            if perceptual:
                existing_ids = {id(candidate) for candidate in candidates}
                candidates.extend(candidate for candidate in perceptual if id(candidate) not in existing_ids)
                evidence.append("perceptual_hash")
                if confidence != "high":
                    confidence = "review"
        output.append({"path": file.get("path"), "filename": file.get("filename"), "confidence": confidence if candidates else "none", "evidence": sorted(set(evidence)), "remote_ids": [item.get("id") for item in candidates], "remote_urls": [item.get("product_url") for item in candidates]})
    return output
