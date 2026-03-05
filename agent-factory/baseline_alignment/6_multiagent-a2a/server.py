from mcp.server.fastmcp import FastMCP
from employee_data import SKILLS, EMPLOYEES

mcp = FastMCP("employee-server", stateless_http=True, host="0.0.0.0", port=8082)

@mcp.tool()
def get_skills() -> set[str]:
    """
    Get all available skills in the employee database.
    
    This tool returns the complete list of skills that employees may have.
    Useful for discovering what skills to search for or understanding
    the skill taxonomy.
    
    Returns:
        set[str]: Set of all unique skills in the database
    """
    print("🔍 Tool called: get_skills")
    return SKILLS

@mcp.tool()
def get_employees_with_skill(skill: str) -> list[dict]:
    """
    Find all employees who have a specific skill.
    
    This tool searches the employee database for anyone with the specified
    skill. The search is case-insensitive.
    
    Args:
        skill (str): The skill to search for (e.g., "Python", "AWS", "React")
    
    Returns:
        list[dict]: List of employees with the skill, each containing:
            - name: Full name (First Last)
            - skills: List of all skills the employee has
    
    Raises:
        ValueError: If no employees have the specified skill
    """
    print(f"🔍 Tool called: get_employees_with_skill(skill='{skill}')")
    
    skill_lower = skill.lower()
    employees_with_skill = []
    for employee in EMPLOYEES:
        for s in employee["skills"]:
            if s.lower() != skill_lower:
                continue
            else:
                employees_with_skill.append(employee)

    if not employees_with_skill:
        raise ValueError(f"No employees have the '{skill}' skill")
    
    return employees_with_skill