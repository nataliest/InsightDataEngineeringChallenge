
# coding: utf-8

# <h1>Test notebook 1</h1>

# In[37]:


import pandas as pd


# In[38]:


def insert_relevant_entries(all_entries_list, wrapper_list):
    relevant_indeces = [0, 10, 13, 14]
    add_list = []
    for index in relevant_indeces:
        if index == 10 and len(all_entries_list[index]) > 5: # if provided zip-code has 9 digits, use only the first 5
            add_list.append(all_entries_list[index][:5])
        else:
            add_list.append(all_entries_list[index])
    wrapper_list.append(add_list)


# Setup all relevant data structures

# In[39]:


f = open("/Users/sangencre/Desktop/NYU/fall_17/Insight_DE_challenge/my_solution/tests/tests/test_1/input/itcont.txt")

wrap = []
keep_track_of_donations = {}


# In[40]:


next = f.readline()
while next != "":
    curr = next.split('|')
    if curr[15] == '': # if OTHER_ID non-empty, ignore the record
        curr[-1] = curr[-1].rstrip()
        insert_relevant_entries(curr, wrap)
        if curr[0] in keep_track_of_donations:
            keep_track_of_donations[curr[0]] += 1
        else:
            keep_track_of_donations[curr[0]] = 1
    next = f.readline()
for el in wrap:
    print(el)
for el in keep_track_of_donations:
    print(el)
    print(keep_track_of_donations[el])
df = pd.DataFrame(wrap)
df.head(7)
f.close()


# In[42]:


f_out = open("/Users/sangencre/Desktop/NYU/fall_17/Insight_DE_challenge/my_solution/tests/tests/test_1/input/out_file.txt", "w")
for el in wrap:
    for el2 in el[:-1]:
        f_out.write(el2 + '|')
    f_out.write(el[-1] + '\n')
f_out.close()

