#!/usr/bin/env python3
import re
import os
import os.path
import datetime
import shutil

jekyll_dir = os.path.dirname(__file__)
os.chdir(jekyll_dir)
os.system('rm -rvf _posts/*')

# 列出markdown文件
file_list = []
os.chdir(os.path.join(jekyll_dir, '..'))
for root, dirs, files in os.walk('.'):
    if root.startswith('./.'):
        continue
    root = root.strip('./')
    if root.startswith('jekyll'):
        continue
    for file_name in files:
        if file_name.endswith('.md'):
            file_path = os.path.join(root, file_name)
            match_obj = re.search('(\d\d\d\d-\d\d-\d\d)-(.*)\.md', file_name)
            if not match_obj:
                print('File name not match: ', file_name)
                continue
            # month = int(match_obj.group(1))
            # date = int(match_obj.group(2))
            title = match_obj.group(2)
            # try:
            #     file_date = datetime.datetime(year, month, date).strftime('%Y-%m-%d')
            #  except ValueError:
            #     print('date not match: ', file_name)
            #     continue
            new_path = 'jekyll/_posts/%s' % (file_name)
            file_list.append(new_path)
            if not os.path.exists(new_path) or os.path.getmtime(new_path) < os.path.getmtime(file_path):
                # 拷贝文件
                print('# Writing %s' % (new_path))
                with open(new_path, 'w') as new_file:
                    file_content = open(file_path).read()
                    matter_dict = {
                        'layout': 'posts',
                        'title': title,
                    }
                    if file_content.startswith('---'):
                        matter_splits = file_content.split('---', 2)
                        for matter_line in matter_splits[1].split('\n'):
                            matter_line = matter_line.strip('\r\n\t')
                            if not matter_line:
                                continue
                            matter_name, matter_value = matter_line.split(':', 1)
                            matter_dict[matter_name.strip('\r\n\t')] = matter_value.strip('\r\n\t ')
                        file_content = matter_splits[2]
                    new_file.write('---\n')
                    for matter_name in matter_dict.keys():
                        matter_value = matter_dict[matter_name]
                        new_file.write('%s: %s\n' % (matter_name, matter_value))
                    new_file.write('---\n')
                    new_file.write(file_content)
# TODO: 删除旧文件

# 编译网站
os.chdir(jekyll_dir)
os.system('bundle exec jekyll build')
os.system('ln -svf ../../images _site/assets/')

