import re


html = """
23423
```python
<div>abdd111dff\n</div>
```
asdfa
sdf

```python
<div>abd2222ddff\n</div>
```
sfasf
"""

pattern_str = r'```python.*?```'

print('\n================== re.sub (not working) ===================\n')
print(re.sub(pattern_str, '___', html))

print('\n================= re.sub (re.DOTALL works) ====================\n')
print(re.sub(pattern_str, '___', html, flags=re.DOTALL))

print('\n================= re.findall (find all) ====================\n')
results = re.findall(pattern_str, html, re.DOTALL)
for result in results:
    print(result)

print('\n================= re.search (find one) ====================\n')
result = re.search(pattern_str, html, re.DOTALL)
print(result.group(0))
