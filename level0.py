records=[66, 84, 82, 53, 11, 59, 5, 77, 97, 25, 25, 68, 31, 56, 29, 56, 88, 38, 12, 21, 49, 48, 62, 47, 87, 34, 83, 62, 63, 80]
total=sum(records)
verage=round(total/30,1)
max_day=max(records)
index=records.index(max_day)

more=[x for x in records if x>50]

print(f"总人数：{total}")
print(f"平均人数：{verage}")
print(f"最高人数：{max_day}(第{index+1}天）)")
print(f"超过50天的人数：{more}")

