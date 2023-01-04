import math
import os
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)

class PathSimilarity:
    def __init__(self):
        raise NotImplementedError("This class is not intended to be instantiated.")

    @classmethod
    def _normalize_path(cls, path: str) -> str:
        """
        Attempts to normalize a path to aid searching. The results
        are not necessarily valid paths (i.e. case insensitivity).
        """
        if not path:
            return None
        path = path.replace("\\", "/")

        if not path.startswith("/"):
            path = "/" + path
        
        if path.endswith("/"):
            path = path[:-1]

        path = path.strip().lower()
        return path


    @classmethod
    def get_path_similarity(cls, path1: str, path2: str) -> float:
        """Estimates how similar the two paths are.

        Args:
            path1: The first path to compare.
            path2: The second path to compare.

        Returns:
            A float between 0 and 1 indicating how similar the two paths are.       
        """
        logger.debug('get_path_similarity(%s, %s)', path1, path2)
        if path1 == path2:
            return 1.0

        path1 = cls._normalize_path(path1)
        path2 = cls._normalize_path(path2)

        if (
            not path1                          # Invalid
            or not path2                       # Invalid   
            or path1.startswith("pkg:")        # Not a path
            or path2.startswith("pkg:")        # Not a path
        ):
            return 0.0

        # The paths must share the same basename
        if os.path.basename(path1) != os.path.basename(path2):
            return 0.0

        # If one is a suffix of the other, then it's the best we can do.
        if path1.endswith(path2) or path2.endswith(path1):
            return 0.80

        longest_suffix = cls.get_longest_common_suffix(path1, path2)
        if longest_suffix:
            suffix_dirs = longest_suffix.count('/') + 1
            min_common_dirs = min(path1.count('/'), path2.count('/')) + 1
            if suffix_dirs == min_common_dirs:
                return 0.90
            else:
                return min(math.sqrt(suffix_dirs / min_common_dirs), 0.90)
        else:
            return 0.0
    
    @classmethod
    def get_longest_common_suffix(cls, path1: str, path2: str) -> str:
        """
        Calculate the longest common suffix of two strings.
        Since these strings are going to be relatively small (path lengths),
        we'll use a simple naiive algorithm.

        A common suffix is defined as the longest string that is a suffix of
        both strings, but is also the start of a filename or directory. This
        means that "foo.txt" is the common suffix of "/bar/foo.txt" and "/quux/foo.txt",
        but is not the common suffix of "/barfoo.txt" and "/quux/foo.txt".

        Args:
            path1: The first path to compare.
            path2: The second path to compare.
        
        Returns:
            The longest common suffix of the two paths, or None if there 
            is no common suffix.
        """
        # Simplify the algorithm to reduce copy/paste.
        cases = [(path1, path2), (path2, path1)]
        longest_common_suffix = None

        for case in cases:
            for index in range(len(case[0]), 0, -1):
                subpath = case[0][index:]   # Progressively longer suffixes

                is_suffix = case[1].endswith(subpath)
                is_dir = subpath.startswith('/') or (index > 0 and case[0][index-1] == '/')
                is_longest = index > 0 and case[0][index-1] == '/'

                if is_suffix and is_dir and is_longest:
                    longest_common_suffix = subpath

        return longest_common_suffix

    @classmethod
    def find_most_similar_path(cls, target_paths: List[str], path: str) -> Optional[str]:
        """
        Finds the path in the list that is most similar to the given path.
        The similarity is calculated using the get_path_similarity function.

        Args:
            target_paths: The list of paths to compare against.
            path: The path to compare.

        Returns:
            The path in the list that is most similar to the given path, or None
        """
        best_similarity = 0.0
        best_path = None
        for target in target_paths:
            similarity = cls.get_path_similarity(target, path)
            if similarity > best_similarity:
                best_similarity = similarity
                best_path = target
        return best_path
