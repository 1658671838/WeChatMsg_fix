import os
import sys
import time
import re
import jieba
import collections
from collections import Counter, defaultdict
import datetime
import urllib.request
import ssl
import html

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from wxManager import DatabaseConnection, MessageType
from wxManager.model import Me
from wxManager.parser.link_parser import wx_sport

def generate_report_data():
    print("开始生成个性化年度报告数据...")
    
    # 1. Setup DB
    db_dir = r'e:\WeChatMsg\wxid_g4pshorcc0r529\db_storage'
    db_version = 4
    conn = DatabaseConnection(db_dir, db_version)
    db = conn.get_interface()
    
    # Load Self Info
    Me().load_from_json(os.path.join(db_dir, 'info.json'))
    self_wxid = Me().wxid
    self_name = Me().name
    print(f"当前用户: {self_name} ({self_wxid})")
    
    # 2. Setup Paths
    report_root = r"e:\WeChatMsg\AnnualReport\report-2025\single"
    js_file = os.path.join(report_root, "src", "js", "getdata.js")
    avatar_dir = os.path.join(report_root, "public", "header")
    
    if not os.path.exists(avatar_dir):
        os.makedirs(avatar_dir)
        
    # 3. Helper: Save Avatar
    def get_avatar_path(wxid):
        # Try to get avatar buffer
        try:
            buf = db.get_avatar_buffer(wxid)
            if buf:
                filename = f"{wxid}.jpg"
                filepath = os.path.join(avatar_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(buf)
                return f"'./header/{filename}'"
        except Exception as e:
            pass
        return "'./header/header12.webp'" # Default

    # Save Self Avatar
    self_avatar_src = get_avatar_path(self_wxid)

    # 4. Helper: Get Name
    contact_cache = {}
    all_contacts = db.get_contacts()
    for c in all_contacts:
        contact_cache[c.wxid] = c

    def get_name(wxid):
        if wxid in contact_cache:
            c = contact_cache[wxid]
            # Prefer remark, then nickname, then wxid
            if hasattr(c, 'remark') and c.remark:
                return c.remark
            if hasattr(c, 'nickname') and c.nickname:
                return c.nickname
        return wxid

    # 5. Analyze Messages
    print("正在分析消息记录 (仅统计私聊)...")
    
    # Stats
    total_sent = 0
    total_received = 0
    total_words = 0
    
    # Time stats
    hour_counts = [0] * 24
    daily_msg_counts = defaultdict(int) # '2025-01-01' -> count
    
    # Friend stats
    friend_msg_counts = Counter()
    friend_word_counts = Counter()
    friend_monthly_counts = defaultdict(lambda: defaultdict(int)) # '1月' -> {wxid: count}
    
    # Emoji stats
    emoji_counter = Counter()
    emoji_urls = {}

    # Keywords
    text_content = []
    
    # Step data (微信运动)
    daily_step_counts = defaultdict(int)  # '2025-01-01' -> steps
    
    # Date range for 2025
    start_2025 = datetime.datetime(2025, 1, 1).timestamp()
    end_2025 = datetime.datetime(2026, 1, 1).timestamp()
    
    sessions = db.session_db.get_session()
    session_users = [s[0] for s in sessions]
    
    processed_count = 0
    for username in session_users:
        processed_count += 1
        if processed_count % 50 == 0:
            print(f"已处理 {processed_count}/{len(session_users)} 个会话...")
            
        # STRICT FILTER: Only private chats
        # Exclude chatrooms, official accounts (gh_), filehelper, openim (Enterprise WeChat), and specific IDs
        # BUT we need to read "微信运动" (gh_43f2581f6fd6) for step data
        if username == 'gh_43f2581f6fd6':
            # 微信运动公众号 - 读取步数数据
            sport_msgs = db.get_messages(username)
            if sport_msgs:
                for msg in sport_msgs:
                    ts = msg.timestamp
                    if ts <= 0: continue
                    dt = datetime.datetime.fromtimestamp(ts)
                    date_str = dt.strftime('%Y-%m-%d')
                    if start_2025 <= ts < end_2025:
                        if msg.type == MessageType.LinkMessage and hasattr(msg, 'xml_content') and msg.xml_content:
                            try:
                                sport_data = wx_sport(msg.xml_content)
                                if sport_data and sport_data.get('score'):
                                    score_str = str(sport_data.get('score', '0')).replace(',', '')
                                    steps = int(score_str) if score_str.isdigit() else 0
                                    if steps > 0:
                                        # 取每天最大的步数（可能有多条记录）
                                        daily_step_counts[date_str] = max(daily_step_counts[date_str], steps)
                            except:
                                pass
            continue
            
        if username.endswith('@chatroom') or username.startswith('gh_') or username == 'filehelper' or username.endswith('@openim') or username.endswith('@qy_u') or username == 'jQ4jTweaBCAFtdK':
            continue
            
        msgs = db.get_messages(username)
        if not msgs: continue
        
        for msg in msgs:
            ts = msg.timestamp
            if ts <= 0: continue
            
            # Only count 2025 data for the report? 
            # The user complained about "960 days". Let's focus on 2025 for the main charts.
            # But for "Total Days", we might check min/max of all time.
            # Let's stick to 2025 for the "Annual" part.
            
            dt = datetime.datetime.fromtimestamp(ts)
            date_str = dt.strftime('%Y-%m-%d')
            
            # Global stats (All time or 2025? Usually annual report is for that year)
            # Let's filter for 2025 for the report content
            if start_2025 <= ts < end_2025:
                daily_msg_counts[date_str] += 1
                hour_counts[dt.hour] += 1
                
                if msg.is_sender:
                    total_sent += 1
                else:
                    total_received += 1
                
                if msg.type == MessageType.Text and msg.content:
                    l = len(msg.content)
                    total_words += l
                    friend_msg_counts[username] += 1
                    friend_word_counts[username] += l
                    
                    month_key = f"{dt.month}月"
                    friend_monthly_counts[month_key][username] += 1
                    
                    # Keywords source - ONLY FROM SENDER (ME)
                    if msg.is_sender and len(text_content) < 50000: # Limit for memory
                        text_content.append(msg.content)
                
                elif msg.type == 47 and msg.is_sender:
                    # Emoji
                    if hasattr(msg, 'md5') and msg.md5:
                        emoji_counter[msg.md5] += 1
                        if hasattr(msg, 'url') and msg.url:
                            emoji_urls[msg.md5] = msg.url

    # 6. Process Data
    print("正在计算统计数据...")
    print(f"读取到 {len(daily_step_counts)} 天的步数数据，总计 {sum(daily_step_counts.values())} 步")
    
    # Days in 2025 (so far)
    # If today is in 2025, use today. If later, use 365.
    now = datetime.datetime.now()
    if now.year == 2025:
        days_in_year = (now - datetime.datetime(2025, 1, 1)).days + 1
    elif now.year > 2025:
        days_in_year = 365
    else:
        days_in_year = 1 # Should not happen based on context
        
    # Top Friends
    top_friends = friend_msg_counts.most_common(5)
    chat_friends_data = []
    for wxid, count in top_friends:
        chat_friends_data.append({
            'name': get_name(wxid),
            'messageCount': f"{count}条消息",
            'wordCount': f"{friend_word_counts[wxid]}字",
            'avatarSrc': get_avatar_path(wxid)
        })
        
    # Monthly Top Friends
    month_friends_data = []
    for i in range(1, 13):
        m_key = f"{i}月"
        if m_key in friend_monthly_counts:
            top_month = max(friend_monthly_counts[m_key].items(), key=lambda x: x[1])
            wxid = top_month[0]
            month_friends_data.append({
                'month': m_key,
                'nickname': get_name(wxid),
                'className': 'passion',
                'num': top_month[1],
                'avatar': get_avatar_path(wxid)
            })
            
    # Keywords
    print("正在生成关键词...")
    # full_text = "\n".join(text_content) # Changed to per-message processing
    word_counter = Counter()
    stop_words = {
        '的', '了', '我', '是', '你', '在', '也', '就', '不', '有', '啊', '吧', '吗', '呢', '哈', '去', '都', '那', '一个', '这个', '什么', '怎么', '可以', '知道', '现在', '今天', '就是', '还是', '没有', '不是', '但是', '因为', '所以', '如果', '那个', '觉得', '其实', '应该', '可能', '然后', '时候', '感觉', '一下', '一点', '真的', '已经', '只是', '出来', '起来', '看着', '看到', '自己', '我们', '你们', '他们', '图片', '表情', '收到', '链接', '视频', '语音', 'https', 'http', 'com', 'cn', 'www', '美团', '红包', 'net', 'org', 'html', 'htm',
        '或者', '还有', '微信', '没事', '直接', '明天', '数据', '消息', '东西', '里面', '问号', '朋友', '人家', '之前', '哪个', '开始', '问题', '感情', '晚上', '意思', '学校', '手机', '不能', '一会', '这种', '宝宝', '不行', '我草', '谢谢', '多少', '不到', '的话', '别人', '我要', '左右', '组家', '警这种关系左石东西号1号0号0老狐函我草HШ李睢', '_别乐w月', '或者192', '捂脸', '笑哭', '呲牙', '偷笑', '调皮', '阴险', '晕', '衰', '骷髅', '敲打', '再见', '擦汗', '抠鼻', '鼓掌', '糗大了', '坏笑', '左哼哼', '右哼哼', '哈欠', '鄙视', '委屈', '快哭了', '亲亲', '吓', '可怜', '菜刀', '西瓜', '啤酒', '篮球', '乒乓', '咖啡', '饭', '猪头', '玫瑰', '凋谢', '示爱', '爱心', '心碎', '蛋糕', '闪电', '炸弹', '刀', '足球', '瓢虫', '便便', '月亮', '太阳', '礼物', '拥抱', '强', '弱', '握手', '胜利', '抱拳', '勾引', '拳头', '差劲', '爱你', 'NO', 'OK', '爱情', '飞吻', '跳跳', '发抖', '怄火', '转圈', '磕头', '回头', '跳绳', '挥手', '激动', '街舞', '献吻', '左太极', '右太极'
    }
    
    for msg_text in text_content:
        words = jieba.cut(msg_text)
        unique_words_in_msg = set()
        for w in words:
            # Filter: Length > 1, not in stop_words, not digit, not containing digits
            if len(w) > 1 and w not in stop_words and not w.isdigit() and not any(char.isdigit() for char in w):
                # Strict filter: Must contain at least one Chinese character or be a valid English word
                # This filters out garbage like "HШ" or random symbols
                if re.search(r'[\u4e00-\u9fa5]', w) or (w.isalpha() and len(w) > 2):
                     unique_words_in_msg.add(w)
        word_counter.update(unique_words_in_msg)
            
    common_words = word_counter.most_common(50)
    keywords_list = [[w, c] for w, c in common_words]
    
    top_keyword = "无"
    top_keyword_num = 0
    if keywords_list:
        top_keyword = keywords_list[0][0]
        top_keyword_num = keywords_list[0][1]

    # Heatmap Data (Step Data) - 真正的微信运动步数
    # Format: [['2025-01-01', 10000], ...]
    heatmap_data_js = "[\n"
    for date_str, steps in daily_step_counts.items():
        heatmap_data_js += f"        ['{date_str}', {steps}],\n"
    heatmap_data_js += "    ]"

    # Top Emoji
    top_emoji_src = "'./header/header48.webp'" # Default
    if emoji_counter:
        top_md5, top_count = emoji_counter.most_common(1)[0]
        print(f"最常用表情包 MD5: {top_md5} (使用 {top_count} 次)")
        
        cdn_url = emoji_urls.get(top_md5)
        
        try:
            if not cdn_url:
                emoticon_db_path = os.path.join(db_dir, 'emoticon', 'emoticon.db')
                if os.path.exists(emoticon_db_path):
                    import sqlite3
                    conn_emo = sqlite3.connect(emoticon_db_path)
                    cursor_emo = conn_emo.cursor()
                    cursor_emo.execute("select cdn_url, thumb_url from kNonStoreEmoticonTable where md5=?", (top_md5,))
                    row = cursor_emo.fetchone()
                    conn_emo.close()
                    if row:
                        cdn_url = row[0] or row[1]

            if cdn_url:
                cdn_url = html.unescape(cdn_url)
                print(f"下载表情包: {cdn_url}")
                emoji_filename = f"emoji_{top_md5}.jpg"
                emoji_path = os.path.join(avatar_dir, emoji_filename)
                
                ssl_context = ssl._create_unverified_context()
                req = urllib.request.Request(cdn_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, context=ssl_context) as response, open(emoji_path, 'wb') as out_file:
                    out_file.write(response.read())
                
                top_emoji_src = f"'./header/{emoji_filename}'"
        except Exception as e:
            print(f"获取表情包失败: {e}")

    # 7. Update File
    print(f"正在更新前端文件: {js_file}")
    
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace Welcome_data
    # Use self_avatar_src
    welcome_js = f"""export const Welcome_data = reactive({{
    avatarSrc: {self_avatar_src},
    nickname: "{self_name}",
    descriptionText: {{
        hello: "Hello World!",
        text1: "时光荏苒，转眼间我们又走过了一年。",
        text2: "在过去的365天里，从深夜的长谈到清晨的祝福，从好友间的调侃到工作中的忙碌……",
        text4: "这些聊天记录，是属于你的独家记忆。",
        text7: "打开报告，开启你的专属年度记忆吧！"
    }}
}});"""
    content = re.sub(r'export const Welcome_data = reactive\(\{[\s\S]*?\}\);', welcome_js, content)

    # Replace statsData
    content = re.sub(r'export var statsData = \{[^}]+\};', 
                   f'export var statsData = {{\n    daysInWeChat: {days_in_year},\n    numOfFriends: {len(friend_msg_counts)},\n    messagesSent: {total_sent},\n    messagesReceived: {total_received},\n    totalWords: {total_words}\n}};' , 
                   content)

    # Replace yAxisData (Hours)
    content = re.sub(r'export var yAxisData = \[[^\]]+\];', 
                   f'export var yAxisData = {hour_counts};', 
                   content)
                   
    # Replace chatFriendsData
    friends_js = "export const chatFriendsData = reactive({\n    chatFriends:[\n"
    for f in chat_friends_data:
        friends_js += f"        {{\n            name: \"{f['name']}\",\n            messageCount: \"{f['messageCount']}\",\n            wordCount: \"{f['wordCount']}\",\n            avatarSrc: {f['avatarSrc']}\n        }},\n"
    friends_js += "    ]\n});"
    content = re.sub(r'export const chatFriendsData = reactive\(\{[\s\S]*?\}\);', friends_js, content)
    
    # Replace monthFriendsData
    month_js = "export const monthFriendsData = reactive(\n    {\n        month_data:[\n"
    for m in month_friends_data:
        month_js += f"            {{ month: \"{m['month']}\", nickname: \"{m['nickname']}\", className: \"{m['className']}\", num: {m['num']}, avatar: {m['avatar']} }},\n"
    month_js += "      ]\n    }\n)"
    content = re.sub(r'export const monthFriendsData = reactive\(\s*\{[\s\S]*?\}\s*\)', month_js, content)
    
    # Replace keywordsData
    keywords_js = "export const keywordsData = reactive({\n"
    keywords_js += f"    keyword: \"{top_keyword}\",\n"
    keywords_js += f"    keyword_num: {top_keyword_num},\n"
    keywords_js += "    messages : [],\n" # Clear dummy messages
    keywords_js += "    chart_option:{},\n"
    keywords_js += "    word_counter:[\n"
    for w, c in keywords_list:
        keywords_js += f"        [\"{w}\",{c}],\n"
    keywords_js += "    ]\n});"
    content = re.sub(r'export const keywordsData = reactive\(\{[\s\S]*?\}\);', keywords_js, content)
    
    # Replace stepData (Heatmap)
    # Find "export var stepData = ...;"
    # It might be "getVirtualData('2024')" in the original file
    content = re.sub(r'export var\s+stepData\s+=\s+[^;]+;', f'export var stepData = {heatmap_data_js};', content)
    
    # Find max day (步数最高的一天)
    max_day_str = '2025-01-01'
    max_day_count = 0
    if daily_step_counts:
        max_day_str = max(daily_step_counts, key=daily_step_counts.get)
        max_day_count = daily_step_counts[max_day_str]
    
    max_date = datetime.datetime.strptime(max_day_str, '%Y-%m-%d')
    
    # 计算年度总步数和距离
    total_steps = sum(daily_step_counts.values())
    distance_km = int(total_steps * 0.0007)  # 大约每步0.7米
    earth_rounds = round(distance_km / 40075, 2)  # 地球周长约40075公里

    # Update stepdescription - 真实的步数统计
    step_desc_js = """export const stepdescription = {
    sumUp: '行万里路',
    left: {
        totalStepsPrefix: '年度总步数',
        totalSteps: %d,
        distancePrefix: '相当于走了',
        distance: %d,
        distanceSuffix: '公里',
        earthPrefix: '绕了地球',
        earthRounds: %s,
        earthSuffix: '圈',
    },
    right: {
        year: '%s',
        month: '%02d',
        day: '%02d',
        stepsPrefix: '达成',
        steps: %d,
        stepsSuffix: '步',
        message: '这一天，走过的是未知的风景，留下的是每一步的精彩',
    },
};""" % (total_steps, distance_km, str(earth_rounds), str(max_date.year), max_date.month, max_date.day, max_day_count)
    
    content = re.sub(r'export const stepdescription = \{[\s\S]*?\};', step_desc_js, content)

    # Update Summary Card (wechatReportData)
    summary_friends_js = "friends : [\n"
    for f in chat_friends_data:
            summary_friends_js += f"        {{ name: '{f['name']}', avatarSrc: {f['avatarSrc']} }},\n"
    summary_friends_js += "    ],"
    content = re.sub(r'friends : \[[\s\S]*?\],', summary_friends_js, content)
    
    content = re.sub(r"\{ label: '聊天联系人', value: \d+, unit: '人' \}", f"{{ label: '聊天联系人', value: {len(friend_msg_counts)}, unit: '人' }}", content)
    content = re.sub(r"\{ label: '发送消息', value: \d+, unit: '条' \}", f"{{ label: '发送消息', value: {total_sent}, unit: '条' }}", content)
    content = re.sub(r"\{ label: '收到消息', value: \d+, unit: '条' \}", f"{{ label: '收到消息', value: {total_received}, unit: '条' }}", content)
    content = re.sub(r"\{ label: '发送总字数', value: \d+, unit: '' \}", f"{{ label: '发送总字数', value: {total_words}, unit: '' }}", content)
    content = re.sub(r"\{ label: '年度关键词', value: '[^']+' \}", f"{{ label: '年度关键词', value: '{top_keyword}' }}", content)
    content = re.sub(r"\{ label: '常用表情包', image: '[^']+' \}", f"{{ label: '常用表情包', image: {top_emoji_src} }}", content)

    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("生成完成！请刷新网页查看。")

if __name__ == '__main__':
    generate_report_data()
