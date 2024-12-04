# Define configs

1. Create file `configs.json`
2. Load initial structure
```json
{
    "configs": [
        {
            ...objects
        }
    ]
}
```
3. Add configs
   **Required fields**:
   - `id`
   - `description`
   - `config`
     - At least one parameter
  
   **Examples**
```json
{
    "configs": [
        {
            "id": 1,
            "description": "Family",
            "config": {
                "groupName": "Family",
                "savePath": "/Users/user/Documents/family"
            }
        },
        {
            "id": 2,
            "description": "Work",
            "config": {
                "groupName": "work",
                "savePath": "/Users/user/Documents/work",
                "startDate": "01-07-2024",
                "endDate": "01-12-2024"
            }
        }
    ]
}
```