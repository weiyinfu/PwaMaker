import json
import os
import re
import shutil
import subprocess as sp
import sys
from os.path import *

current_folder = dirname(abspath(__file__))
pwa_folder = abspath(join(current_folder, "../pwa"))


class Conf:
    def __init__(self, conf, config_path):
        self.config_path = abspath(config_path)
        self.name: str = conf["name"].strip()
        self.index: str = conf["index"].strip()
        self.icon: str = conf["icon"].strip()
        if self.icon.startswith('./'):
            self.icon = abspath(join(dirname(self.config_path), self.icon))
        self.product_name: str = conf["productName"].strip()

    def __repr__(self):
        obj = {}
        for i in dir(self):
            if not i.startswith('_'):
                v = getattr(self, i)
                if not callable(v):
                    obj[i] = v
        return str(obj)


def check_params(conf: Conf):
    if not conf.name:
        print("应用名称不能为空")
        exit(-1)
    if not re.match("[a-z\\-]+", conf.name):
        print(f"name字段必须为小写字母+下划线:{conf.name}")
        exit(-1)
    if not conf.product_name:
        print("产品名称不能为空")
        exit(-1)

    def icon_exists():
        for icon_suffix in ("png", "ico", "icns"):
            icon_path = conf.icon + "." + icon_suffix
            if exists(icon_path):
                return True
        return False

    if not icon_exists():
        print(f"图标不存在 {conf.icon}")
        exit(-1)
    if not conf.index:
        print(f"index URL不能为空 {conf.index}")
        exit(-1)


def generate(conf: Conf):
    gen_folder = join(dirname(conf.config_path), "gen", conf.name)
    shutil.rmtree(gen_folder)

    def my_ignore(folder, names):
        return ['node_modules']

    shutil.copytree(pwa_folder, gen_folder, ignore=my_ignore)
    # 生成package.json
    package_path = join(gen_folder, 'package.json')
    package_json = json.load(open(join(pwa_folder, 'package.json')))
    package_json["name"] = conf.name
    package_json["productName"] = conf.product_name
    json.dump(package_json, open(package_path, 'w'), ensure_ascii=False, indent=2)

    # 生成forge.config.js
    forge_config_path = join(gen_folder, 'forge.config.js')
    forge_config = open(join(pwa_folder, 'forge.config.js')).read()
    forge_config = re.sub('icon:".+?"', f'icon:"{conf.icon}"', forge_config)
    open(forge_config_path, 'w').write(forge_config)

    # 生成config.json
    config_path = join(gen_folder, 'src/config.json')
    config_json = {"index": conf.index}
    json.dump(config_json, open(config_path, 'w'), ensure_ascii=False, indent=2)

    # 执行命令
    sp.check_call(f"""
    yarn install
    yarn package
    """, shell=True, cwd=gen_folder, env=os.environ)

    app_path = join(gen_folder, 'out')
    print(f"生成成功:{app_path}")


def main():
    if len(sys.argv) < 2:
        print("请指定配置文件")
        return -1
    config_path = sys.argv[1]
    conf = Conf(json.load(open(config_path, encoding='utf8')), config_path)
    print(f"正在校验参数:{conf}")
    check_params(conf)
    print("校验参数完成")
    generate(conf)


if __name__ == '__main__':
    main()
