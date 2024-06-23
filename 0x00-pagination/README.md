# README

This document provides a brief description of the concepts covered in this directory.

## Pagination Techniques in REST API Design

### 1. Paginating with Simple Page and Page Size Parameters

When paginating a dataset using simple page and page size parameters, you can follow these steps:

1. **Define Your API Endpoint:**
   - Create an API endpoint that returns a paginated list of resources.
   - Accept query parameters like `page` (for the current page number) and `page_size` (for the number of items per page).

2. **Retrieve Data:**
   - Fetch the relevant data from your data source (e.g., database, API).
   - Apply pagination logic to select the appropriate subset of data based on the provided parameters.

3. **Python Implementation:**
   ```python
   def get_paginated_data(page, page_size):
       # Fetch data from your data source (e.g., database)
       all_data = get_all_data()
       
       # Calculate start and end indices for the current page
       start_idx = (page - 1) * page_size
       end_idx = start_idx + page_size
       
       # Return the paginated data
       return all_data[start_idx:end_idx]
   ```

### 2. Paginating with Hypermedia Metadata (HATEOAS)

HATEOAS (Hypermedia as the Engine of Application State) allows clients to discover API navigation based on the current state. Here's how to incorporate it:

1. **Include Links in Responses:**
   - Along with the paginated data, include links to related resources (e.g., next page, previous page, first page, last page).
   - Use link relation types (e.g., `next`, `prev`, `first`, `last`) to guide clients.

2. **Python Implementation:**
   ```python
   def get_paginated_data_with_links(page, page_size):
       # Fetch data as before
       all_data = get_all_data()
       
       # Calculate start and end indices
       start_idx = (page - 1) * page_size
       end_idx = start_idx + page_size
       
       # Create links for pagination
       links = {
           "self": f"/api/data?page={page}&page_size={page_size}",
           "next": f"/api/data?page={page + 1}&page_size={page_size}",
           "prev": f"/api/data?page={page - 1}&page_size={page_size}"
       }
       
       # Return paginated data with links
       return {
           "data": all_data[start_idx:end_idx],
           "_links": links
       }
   ```

### 3. Deletion-Resilient Pagination

To paginate in a deletion-resilient manner (even when items are removed), consider using cursor-based pagination:

1. **Use Cursors:**
   - Instead of relying on page numbers, use a cursor (e.g., an item's unique identifier) to track the position.
   - Clients provide the cursor for the next page, and the server returns the next set of items.

2. **Python Implementation:**
   ```python
   def get_paginated_data_with_cursor(cursor, page_size):
       # Fetch data and sort by unique identifier (e.g., timestamp)
       all_data = get_all_data_sorted_by_id()
       
       # Find the index of the cursor
       cursor_idx = find_index_of_item_with_id(all_data, cursor)
       
       # Calculate start and end indices
       start_idx = cursor_idx + 1
       end_idx = start_idx + page_size
       
       # Return paginated data
       return all_data[start_idx:end_idx]
   ```