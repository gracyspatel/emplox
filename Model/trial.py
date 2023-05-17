import pandas as pd

data = [['Database', 'css,java,python,database'],
        ['Python & ML', 'html,css,java,python,ml'],
        ['Python & ML', 'ml,newdata,c,c++,c,c++'],
        ['Python & ML', 'ml,newdata,c,c++,c,c++'],
        ['Python & ML', 'ml,newdata,c,c++,c,c++,lmno'],
        ['Java', 'java,java,java,java,java'],
        ['Java', 'coding']]

df = pd.DataFrame(data, columns=["Department", "Technical Skills"])

# Create a dictionary with Department as keys and Technical Skills as values (as sets)
department_skills_dict = {}
for index, row in df.iterrows():
    department = row["Department"]
    skills = row["Technical Skills"].split(",")  # Convert skills to a list

    if department in department_skills_dict:
        department_skills_dict[department].update(skills)  # Update the existing set with new skills
    else:
        department_skills_dict[department] = set(skills)  # Create a new set for the department's skills

print(department_skills_dict)
