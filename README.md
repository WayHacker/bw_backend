# About

A backend written for Build Watchdog system, use postgres and python

![current snapshot](./snapshot.jpg)

# API 
## Objects
1. **[GET]** http://77.221.141.68:20/objects/ - *list of all objects*
2. **[POST]** http://77.221.141.68:20/objects/ - *creates an object*  
    ```json
    {name: "Alpha"}
    ```
3. **[GET]** http://77.221.141.68:20/objects/{id} - *list only one object by id*

4. **[DELETE]** http://77.221.141.68:20/objects/{id} - *delete the object by id*

5. **[GET]** http://77.221.141.68:20/objects/{id}/users - *get all **users** that assignment to this object*

6. **[GET]** http://77.221.141.68:20/objects/{id}/tasks - *return all **tasks** that assignment to this object*

7. **[GET]** http://77.221.141.68:20/objects/{id}/object_calc - *returns fact, plan and prediction for this object*

8. **[GET]** http://77.221.141.68:20/objects/{id}/done_tasks - *return all done tasks in object*

9. **[GET]** http://77.221.141.68:20/objects/{id}/undone_tasks - *return all undone tasks in object*

## Tasks

1. **[GET]** http://77.221.141.68:20/tasks/ - *list of all tasks*

2. **[POST]** http://77.221.141.68:20/tasks/ - *create one tasks*
    
    Input types:
    ```json
    {
    user_count_by_plan: int
    plan_per_hour: int
    shift: int
    done_scope: Optional[int] = 0
    work_scope: int
    object_id: uuid
    description: str
    user_count: Optional[int] = 0
    start_date: datetime
    }
    ```

3. **[GET]** http://77.221.141.68:20/tasks/{id} - *list only one task*

4. **[DELETE]** http://77.221.141.68:20/tasks/{id} - *delete task by id*

5. **[PUT]** http://77.221.141.68:20/tasks/{id} - *update task by id*

    Input types:
    ```json
    {
    task_id: uuid
    user_count_by_plan: int
    plan_per_hour: int
    shift: int
    done_scope: Optional[int] = 0
    work_scope: int
    object_id: uuid.UUID
    description: str
    user_count: Optional[int] = 0
    start_date: datetime
    }
    ```


## Assignments
Assignments object -> user 

1. **[GET]** http://77.221.141.68:20/assignments/ - *list of all assignments*
2. **[POST]** http://77.221.141.68:20/assignments/ - *create one assignment*
    
    Input types:
    ```json
    {
    object_id: uuid,
    user_id: uuid,
    description: str
    }
    ```
3. **[GET]** http://77.221.141.68:20/assignments/{id} - *list only one assingment by id*

4. **[DELETE]** http://77.221.141.68:20/assignments/{id} - *delete assignment by id*


## User to Tasks
Assignments user -> task 

1. **[GET]** http://77.221.141.68:20/user_tasks/ - *list of all assignments*
2. **[POST]** http://77.221.141.68:20/user_tasks/ - *create one assignment*
    
    Input types:
    ```json
    {
    task_id: uuid,
    user_id: uuid,
    description: str
    }
    ```

#### You can create user -> task assignment only if task and user are in one object!
After it, prediction and user_count will be updated

3. **[GET]** http://77.221.141.68:20/user_tasks/{id} - *list only one assingment by id*

4. **[DELETE]** http://77.221.141.68:20/user_tasks/{id} - *delete assignment by id*