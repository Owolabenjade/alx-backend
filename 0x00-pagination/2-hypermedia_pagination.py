#!/usr/bin/env python3
"""
Hypermedia pagination module.
"""
import csv
import math
from typing import List, Tuple, Dict, Any


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Return a tuple of size two containing a start index and an end index
    corresponding to the range of indexes to return in a list for those
    particular pagination parameters.

    Args:
        page (int): The page number (1-indexed)
        page_size (int): The number of items per page

    Returns:
        Tuple[int, int]: A tuple containing the start and end indexes
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Return the appropriate page of the dataset based on pagination params.

        Args:
            page (int, optional): The page number (1-indexed). Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 10.

        Returns:
            List[List]: The paginated dataset.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        # Get the full dataset
        dataset = self.dataset()
        
        # If the parameters are out of range, return an empty list
        if page > len(dataset) or page_size <= 0:
            return []
        
        # Use index_range to get the start and end indexes
        start_idx, end_idx = index_range(page, page_size)
        
        # Return the appropriate page (if end_idx is out of range, it'll just return
        # all elements from start_idx to the end of the list)
        if start_idx >= len(dataset):
            return []
            
        return dataset[start_idx:end_idx]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Return hypermedia pagination information including the data and
        metadata for navigation.

        Args:
            page (int, optional): The page number (1-indexed). Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 10.

        Returns:
            Dict[str, Any]: A dictionary containing hypermedia pagination info.
        """
        data = self.get_page(page, page_size)
        total_items = len(self.dataset())
        
        # Calculate total_pages
        total_pages = math.ceil(total_items / page_size) if page_size > 0 else 0
        
        # Determine next_page
        next_page = page + 1 if page < total_pages else None
        
        # Determine prev_page
        prev_page = page - 1 if page > 1 else None
        
        # Return hypermedia dictionary
        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }