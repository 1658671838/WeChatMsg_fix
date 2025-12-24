#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time        : 2025/3/11 20:46 
@Author      : SiYuan 
@Email       : 863909694@qq.com 
@File        : wxManager-2-contact.py 
@Description : 
"""
import sys
import os
# 动态添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import time
import codecs

from wxManager import DatabaseConnection

db_dir = 'wxid_g4pshorcc0r529/db_storage'  # 第一步解析后的数据库路径，例如：./wxid_xxxx/db_storage
db_version = 4  # 数据库版本，4 or 3

conn = DatabaseConnection(db_dir, db_version)  # 创建数据库连接
database = conn.get_interface()  # 获取数据库接口

# 打开文件保存联系人信息
contacts_file = codecs.open('contacts.txt', 'w', encoding='utf-8')

def write_output(text):
    """同时输出到控制台和文件"""
    try:
        print(text)
    except UnicodeEncodeError:
        # 如果控制台编码有问题，尝试用替代字符
        print(str(text).encode('gbk', errors='replace').decode('gbk', errors='replace'))
    contacts_file.write(str(text) + '\n')

st = time.time()
cnt = 0
contacts = database.get_contacts()
for contact in contacts:
    write_output(contact)
    contact.small_head_img_blog = database.get_avatar_buffer(contact.wxid)
    cnt += 1
    if contact.is_chatroom:
        write_output('*' * 80)
        write_output(contact)
        chatroom_members = database.get_chatroom_members(contact.wxid)
        write_output(f'{contact.wxid} 群成员个数： {len(chatroom_members)}')
        for wxid, chatroom_member in chatroom_members.items():
            chatroom_member.small_head_img_blog = database.get_avatar_buffer(wxid)
            write_output(chatroom_member)
            cnt += 1

et = time.time()

write_output(f'联系人个数：{cnt} 耗时：{et - st:.2f}s')
contacts_file.close()
