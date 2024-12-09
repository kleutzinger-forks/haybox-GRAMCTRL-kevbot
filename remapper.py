# LHS is original button placement, RHS is new button
import re

with open('original_text.txt', 'r') as file:
    original_text = file.read()


# remember manual replace of InputState::up,InputState::midshield
remaps = """\
left
right
down
up,midshield
up2
c_left
c_right,c_down
c_down,c_up
c_up,c_right
a,b
b,l
x,y
y,r
l,a
r,x
z,lightshield
lightshield,up
midshield,z
select
start
home
mod_x
mod_y
"""

rewrites = []
for line in remaps.split("\n"):
    if "," not in line:
        continue
    lhs, rhs = line.split(",")
    lhs, rhs = lhs.strip(), rhs.strip()
    lhs, rhs = "inputs." + lhs, "inputs." + rhs

    rewrites.append((lhs, rhs))

print(rewrites)


# do rewrites on inputs.KEY to the new inputs.KEY, careful that l is a prefix of left and lightshield
# do two passes

def replace_all(text, rewrites):
    # First create a mapping dictionary
    remap = {}
    for lhs, rhs in rewrites:
        remap[lhs] = rhs

    # Sort patterns by length (longest first) to avoid prefix issues
    patterns = sorted(remap.keys(), key=len, reverse=True)

    # First pass: Store original values with temporary markers
    temp_text = text
    for i, pattern in enumerate(patterns):
        temp_marker = f"__TEMP_{i}__"
        temp_text = re.sub(r"\b" + re.escape(pattern) + r"\b", temp_marker, temp_text)

    # Second pass: Replace temporary markers with final values
    final_text = temp_text
    for i, pattern in enumerate(patterns):
        temp_marker = f"__TEMP_{i}__"
        final_value = remap[pattern]
        final_text = final_text.replace(temp_marker, final_value)

    return final_text


print(replace_all(original_text, rewrites))
with open("src/modes/Melee21Button.cpp", "w") as f:
    f.write(replace_all(original_text, rewrites))
