import random

FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", 
    "Jennifer", "Michael", "Linda", "William", "Elizabeth"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", 
    "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"
]


SKILLS = {
    "Kotlin", "Java", "Python", "JavaScript", "TypeScript",
    
    "React", "Angular",
    
    "Spring Boot", "Node.js",
    
    "AWS", "Docker", "Kubernetes", "DevOps", "CI/CD",
    
    "SQL", "MongoDB",
    
    "Git", "REST API", "GraphQL",
    
    "Machine Learning"
}

EMPLOYEES = list({
    emp["name"]: emp for emp in [
        {
            "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "skills": random.sample(list(SKILLS), random.randint(2, 5))
        }
        for i in range(100)
    ]
}.values())