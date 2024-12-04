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
   - `description`
   - `config`
     - At least one parameter
  
   **Examples**
```json
{
    "configs": [
        {
            "description": "Family",
            "config": {
                "groupName": "Family",
                "savePath": "/Users/user/Documents/family"
            }
        },
        {
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