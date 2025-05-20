import csv

personnel_data = [
    {"peronnel_id": "R001", "name": "Alice", "skills": ["Java", "Cloud"], "availability": 2},
    {"peronnel_id": "R002", "name": "Bob", "skills": ["Python", "SQL"], "availability": 2},
    {"peronnel_id": "R003", "name": "Charlie", "skills": ["HTML"], "availability": 1},
    {"peronnel_id": "R004", "name": "Alison", "skills": ["SQL", "Python", "Cloud"], "availability": 2},
    # {"peronnel_id": "R004", "name": "Alison", "skills": ["SQL", "Python"], "availability": 2},
]

projects_data = [
    {"project_id": "P001", "name": "Data Analysis", "required_skills": ["Python", "SQL"], "urgency": 3, "budget": 1000},
    {"project_id": "P002", "name": "Web App", "required_skills": ["Java", "Cloud"], "urgency": 4, "budget": 15000},
    {"project_id": "P003", "name": "ML", "required_skills": ["Python"], "urgency": 5, "budget": 50000},
    {"project_id": "P004", "name": "Web Development", "required_skills": ["HTML"], "urgency": 3, "budget": 15000},
    {"project_id": "P005", "name": "ML Pipeline", "required_skills": ["Python"], "urgency": 5, "budget": 5000},
    {"project_id": "P006", "name": "Web App", "required_skills": ["Java", "Cloud"], "urgency": 4, "budget": 1500},
    {"project_id": "P007", "name": "Performace Check", "required_skills": ["Cloud"], "urgency": 1, "budget": 1000},
]

projects_months_data = [
    {
        "January": [
        {"project_id": "P001", "name": "Data Analysis", "required_skills": ["Python", "SQL"], "urgency": 3, "budget": 1000},
        {"project_id": "P003", "name": "ML", "required_skills": ["Python"], "urgency": 5, "budget": 50000},
        ]

    }
]

# def priorities(projects):
#     p = len(projects)
#     pri = [[0 for _ in range(3)] for _ in range(p)]

#     proj_ind = -1
#     for p in projects:
#         proj_ind = proj_ind + 1
#         keys = list(p.keys())
#         pri[proj_ind][0], pri[proj_ind][1], pri[proj_ind][2] = p[keys[0]] + "_" + p[keys[1]], p[keys[3]], p[keys[4]]

#     urg, budg = [], []
#     for i in pri:
#         if i[1] not in urg:
#             urg.append(i[1])
#         if i[2] not in budg:
#             budg.append(i[2])
#     urg.sort(reverse=True)
#     budg.sort(reverse=True)
    
#     for u in range(len(urg)):
#         for b in range(len(budg)):
#             for i in range(len(pri)):
#                 if(pri[i][1] == urg[u]) and (pri[i][2] == budg[b]):
#                     pri.append(pri[i])
#                     pri.pop(i)
#     return pri
# # p = priorities(projects_data)
# # for i in p:
# #     print(i)
# # print()

def priorities(projects):
    proj = projects
    urg, budg = [], []
    for p in proj:
        urg.append(p[list(p.keys())[3]])
        budg.append(p[list(p.keys())[4]])
    
    urg.sort(reverse=True)
    budg.sort(reverse=True)

    for u in range(len(urg)):
        for b in range(len(budg)):
            for i in range(len(proj)):
                if(proj[i][list(proj[i].keys())[3]] == urg[u]) and (proj[i][list(proj[i].keys())[4]] == budg[b]):
                    proj.append(proj[i])
                    proj.pop( proj.index(projects[i]) )         
    return proj

def res_to_proj(resources, projects, prioritized_proj = True):
    r, p = len(resources), len(projects)
    matched = [[0 for _ in range(r+1)] for _ in range(p+1)] # rows are projects, cols are resources
    
    # Step 1 (optional): Prioritize projects
    if(prioritized_proj): 
        proj = priorities(projects)
    else:
        proj = projects
    
    # Step 2: Assign personnel to projects
    proj_ind = 0
    for p in proj:
        proj_ind, proj_name, req_skills = proj_ind + 1, p[list(p.keys())[0]] + "_" + p[list(p.keys())[1]], p[list(p.keys())[2]]
        matched[proj_ind][0] = proj_name
        
        res_ind = 0
        res = resources
        for r in res:
            res_ind, res_name, skills, avail = res_ind + 1, r[list(r.keys())[0]] + "_" + r[list(r.keys())[1]], r[list(r.keys())[2]], r[list(r.keys())[3]]
            a = sum( [i[res_ind] for i in matched[1:]] )
            matched[0][res_ind] = res_name
            
            count = 0
            for s in skills:
                if(s in list(req_skills)):
                    count += 1
                    if(count == len(req_skills)):
                        if(a < avail):
                            req_skills.clear()
                            matched[proj_ind][res_ind] = 1
                            count = 0
                            break
                    continue
                else:
                    continue
        
        # Step 3: Personnel requirements for unassigned projects
        needed = {}
        if(len(req_skills) > 0):
            needed[proj_name] = req_skills

    return matched, needed
assigned, missing = res_to_proj(personnel_data, projects_data)
# for i in assigned:
#     print(i)
# print()
# for i in missing:
#     print(i, missing[i])
# print()

def write_csv(file_path, assigned_data, missing_data):
    with open(file_path, mode = 'w', newline="") as file:
        writer = csv.writer(file)
        draft = []
        for i in assigned_data:
            draft.extend(i)
            for j in missing_data:
                if(i[0] == j):
                    draft.append(" **")
                    draft.extend(missing_data[j])
            writer.writerow(draft)
            draft = []
write_csv("FinalPres/final.csv", assigned, missing)