import re
from collections import defaultdict

messages = [
    "我想报名！姓名：张三；电话：13577889900；项目：COSPLAY",
    "姓名王五 电话 18812345678 活动 跑酷",
    "【报名】李四-18900011223-摊位：手作饰品",
    "想参加活动！赵六：13399887766，报名项目：街舞",
    "报名|姓名：周七|手机 16622331155|项目 摄影",
    "名字：钱八；手机号：abc123；项目：魔术",  # 无效
    "报名 填写信息：姓名=孙九，电话=15566778899，参与：汉服巡游",
    "刘十 · 13155667788 · 节目：小品表演",
    "我是吴一一，电话 19922334455 ，节目 想报名 合唱",
    "姓名：郑十二；学号不需要；手机号：18811223344；项目：绘画",
    "报名 姓名十三 电话 17799887766 活动 器乐独奏",
    "活动申请-何十四-13955667788-报名-话剧",
    "姓名：施十五；手机：16634561234；参与项目：电竞赛",
    "【社团招新】 姓名：贺十六； 18511112222； 加入 社团 摄影",
    "我要报名！姓名十七 手机号 13311112222 活动 街舞",
]

def parse_messages(messages):
    """
    使用生成器逐条处理短信，提取姓名、电话和项目信息
    """
    for message in messages:
        # 提取姓名
        name = "信息错误"
        name_patterns = [
            r'姓名[：:\s=]*([\u4e00-\u9fa5]{2,4})',
            r'名字[：:\s=]*([\u4e00-\u9fa5]{2,4})',
            r'^([\u4e00-\u9fa5]{2,4})[\s·\-]',
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, message)
            if match:
                name = match.group(1)
                if 2 <= len(name) <= 4:
                    break
                else:
                    name = "信息错误"
        
        # 如果还没找到姓名，尝试简单的中文匹配
        if name == "信息错误":
            chinese_match = re.search(r'([\u4e00-\u9fa5]{2,4})', message)
            if chinese_match:
                name = chinese_match.group(1)
        
        # 提取电话号码
        phone_match = re.search(r'1[3-9]\d{9}', message)
        phone = phone_match.group(0) if phone_match else "信息错误"
        
        # 提取项目
        project = "信息错误"
        project_keywords = ['项目', '活动', '节目', '参与', '加入', '摊位']
        
        for keyword in project_keywords:
            pattern = f'{keyword}[：:\s=]*([\u4e00-\u9fa5a-zA-Z]+)'
            match = re.search(pattern, message)
            if match:
                project_candidate = match.group(1)
                # 过滤无效项目名称
                invalid_words = {'想报名', '报名', '申请', '项目', '社团', '填写信息', '活动申请', '我是', '不需要', '招新'}
                if project_candidate not in invalid_words:
                    project = project_candidate
                    break
        
        # 最终验证
        if not re.match(r'^1[3-9]\d{9}$', phone):
            phone = "信息错误"
        if not re.match(r'^[\u4e00-\u9fa5]{2,4}$', name):
            name = "信息错误"
        if not re.match(r'^[\u4e00-\u9fa5a-zA-Z]{2,10}$', project):
            project = "信息错误"
        
        yield name, phone, project

def process_registration(messages):
    """
    处理报名信息并返回分组结果
    """
    parsed_data = list(parse_messages(messages))
    
    # 按项目分组
    project_groups = defaultdict(list)
    valid_count = 0
    
    for name, phone, project in parsed_data:
        if phone != "信息错误" and project != "信息错误":
            project_groups[project].append((name, phone))
            valid_count += 1
        else:
            # 对于无效记录，可以单独处理或记录到"信息错误"组
            project_groups["信息错误"].append((name, phone))
    
    print(f"总记录数: {len(messages)}条")
    print(f"有效报名记录: {valid_count}条")
    print(f"无效记录: {len(messages) - valid_count}条")
    
    # 计算每个项目的报名人数（排除信息错误组）
    valid_project_counts = {project: len(participants) for project, participants in project_groups.items() 
                           if project != "信息错误"}
    
    # 找出报名人数最多的前3个项目
    top_3_projects = sorted(valid_project_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    print("\n各项目报名人数:")
    for project, count in sorted(valid_project_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {project}: {count}人")
    
    print("\n报名人数最多的前3个项目:")
    for i, (project, count) in enumerate(top_3_projects, 1):
        print(f"  第{i}名: {project} - {count}人")
    
    return dict(project_groups)

# 执行处理
result = process_registration(messages)

print("\n分组结果:")
for project, participants in sorted(result.items()):
    if project != "信息错误":  # 只显示有效项目
        print(f"{project}: {participants}")

# 显示要求的字典格式
print("\n最终结果字典:")
required_format = {k: v for k, v in result.items() if k != "信息错误"}
print(required_format)