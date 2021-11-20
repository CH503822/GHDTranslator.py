version_info='2.9.5 beta2'
update_info='20211120'

import os, sys, getopt, shutil, re, alive_progress, readchar
from alive_progress.utils.colors import * # MAGIC
# BLUE GREEN YELLOW RED MAGENTA CYAN ORANGE BOLD DIM IT(ALIC) UNDER(LINE)

# Formats
modetxt=lambda x:YELLOW('\n>>> '+x)
mode=lambda x:print(modetxt(x))
error=lambda x:print(RED('[error] '+x))
warning=lambda x:print(ORANGE('[warning] ')+x)
info=lambda x:print(CYAN('[info] ')+x)
ok=lambda x:print(GREEN('[ok] ')+x)
confirm=lambda x:input1(YELLOW('[confirm] ')+x+' [Y/n] ').upper()=='Y'
errorcmd=lambda x:{'':None}[(str(error(x))+str(print('\n'+help_text)))[:0]]
inputo=input
def input1(x=''):
    try:
        print(x,end='',flush=True)
        y=readchar.readchar().decode()
        print('')
    except:
        y=''
    return y
def input(x=''):
    try:
        y=inputo(x) # Never interrupt this
    except:
        print('')
        y=''
    return y

# Texts
title_text='=== '+ORANGE('[GitHub Desktop Translator zh_CN] ')+ORANGE_IT('(ver '+version_info+')')+' ==='
version_text='\n'+'='*42+BOLD('\n GitHub Desktop translation '+version_info)+'''
   --by Zetaspace '''+update_info+f'''\n
 {CYAN("Link: GitHub.com/ZetaSp/GHDTranslator.py")}\n
 Thank you for using!\n'''+'='*42
help_text=BOLD(os.path.split(sys.argv[0])[1])+f''' {ITALIC("<options>")}
-y                Automatically finish everything
-d --dir {ITALIC("<dir>")}    Specify a target dir, app folder like \'app-'''+version_info.replace(' ','-')+'''\'
-r --restore      Restore from auto-backup file, using with --dir
-u --update       Check for updates from github (mirror fastgit)
-h --help         Show this message
-v --version      Show version info'''

# Check version code
try:
    if len(str(int(update_info)))!=8:raise ValueError
except:
    error("Version '"+update_info+"' is wrong. It should be a proper date.")
    sys.exit(999)

# Print title
print(title_text)

# Function
def check_update():
    try:
        print(YELLOW('>>> Check update'))
        # Not using GitHub API, because I'm always "rate limited"...
        # Using raw version.json instead.
        #api='https://raw.githubusercontent.com/ZetaSp/GHDTranslator.py/main/version.json'    
        # Githubusercontent.com is unreachable in China; using mirror fastgit.org.
        api='https://raw.fastgit.org/ZetaSp/GHDTranslator.py/main/version.json'

        with alive_progress.alive_bar(3, title=CYAN('[info] Connecting'), spinner='dots_waves', bar=None, enrich_print=False, stats=False, elapsed=False) as bar:
            bar()
            info('Current: ver '+version_info+' update '+update_info)
            import requests
            bar()
            try:
                req=requests.get(api,timeout=(2,2))
                bar()
            except:
                # Any connection error.
                bar()
                error('Connection failed. Please check it manually.')
                raise KeyboardInterrupt
            try:
                req=req.json()
                version=req['version']
                update=req['update']
                download=req['download']
                action=req['action']
            except:
                # Any parsing error.
                bar()
                error('Update data error.\nPlease check it manually.')
                sys.exit(1)
            info('Newest:  ver '+version+' update '+update+'\n')
            
        if update_info==update:
            ok('You are using the newest version!')
            sys.exit(0)
        else:
            # Different update
            try:
                diff=int(update)>int(update_info)
            except:
                # Not a number???
                warning(BOLD('LOWER VERSION')+'('+update+') available.')
                if confirm('Update?'):
                    ok('Sure.')
                else:
                    ok('Canceled.')
                    sys.exit(1)
            else:
                if diff:
                    # Larger update
                    ok('New version('+update+') available!')
                else:
                    # Smaller update?
                    warning(BOLD('LOWER VERSION')+'('+update+') available.')
                    if confirm('Update?'):
                        ok('Sure.')
                    else:
                        ok('Canceled.')
                        sys.exit(1)
            if action=='open':
                try:
                    import webbrowser
                    webbrowser.get()
                except:
                    # Web browser not available. Plz open manually.
                    info('Goto: '+BLUE_UNDER(download))
                else:
                    info('Opening: '+download)
                    webbrowser.open(download)
            sys.exit(1)
    except KeyboardInterrupt:
        print('')
        ok('Canceled.')
        sys.exit(1)

'=== Main ==='
# Get cmdline args
#if sys.argv[1:]==[]:sys.argv[1:]=['-h']
if sys.argv[-1]=='-d':sys.argv+=['""']
try:
    opts,args=getopt.getopt(sys.argv[1:],'hvyd:ru',['help','version','dir=','restore','update'])
except getopt.GetoptError:
    errorcmd('Unknown options: '+' '.join(sys.argv[1:])) # Unknown args
    sys.exit(1)

autopatch=False
restore=False
appdir=''
exist=os.path.exists
copy=shutil.copy2
for opt,arg in opts:
    if opt in ('-h','--help'):
        print(modetxt('Help\n')+help_text)
        sys.exit(0)
    elif opt in ('-v','--version'):
        print(modetxt('Version')+version_text)
        sys.exit(0)
    elif opt in ('-u','--update'):
        check_update()
        sys.exit(0)
    elif opt in ('-y'):
        autopatch=True
    elif opt in ('-r','--restore'):
        restore=True
    elif opt in ('-d','--dir'):
        appdir=arg
mode('Locate')
if not type(appdir)is str:
    error('Error dir: '+str(appdir)) # Not str
    sys.exit(0)
if appdir=='-y':
    appdir,autopatch='',True
if appdir!='':
    while(appdir[0]=="'"and appdir[-1]=="'")or(appdir[0]=='"'and appdir[-1]=='"'):
        appdir=appdir[1:-1]
        if appdir=='':break
if appdir=='':
    # Blank target dir
    while True:
        if sys.platform=='win32':PATH=';'
        elif sys.platform=='darwin' or sys.platform=='linux' or sys.platform=='cygwin':PATH=':'
        else:break
        PATH=re.split(PATH,os.getenv('PATH'))
        for i in PATH:
            if i=='':continue
            if(i[0]=="'"and i[-1]=="'")or(i[0]=='"'and i[-1]=='"'):i=i[1:-1]   # Cut ''
            if not exist(i):continue
            p=os.path.abspath(i)
            if 'github'in os.listdir(p):    # ...\GitHubDesktop\bin\github file
                appdir=os.path.abspath(os.path.join(p,'..'))
        if appdir!='':
            if(appdir[0]=="'"and appdir[-1]=="'")or(appdir[0]=='"'and appdir[-1]=='"'):appdir=appdir[1:-1] # Cut ''
            dirs=[]
            for i in os.listdir(appdir):
                if exist(os.path.abspath(os.path.join(appdir,i))+'\\resources\\app'):
                    dirs+=[i]
            appdir=os.path.abspath(os.path.join(appdir,sorted(dirs,reverse=True)[0]))
            del dirs
            info('Found GitHub Desktop in \''+appdir+'\'')
            if autopatch:break
            if confirm('Patch this one?'):
                break
        confirm
        appdir=input('Please type in your GitHub Desktop install path, like \'app-'+version_info.replace(' ','-')+'\' or \'GitHubDesktop\':\n> ')
        if appdir=='':error('Not typing.');sys.exit(0)
        break
if(appdir[0]=="'"and appdir[-1]=="'")or(appdir[0]=='"'and appdir[-1]=='"'):appdir=appdir[1:-1] # Cut ''
if not exist(appdir):
    error('Not exist: '+appdir)  # Target dir not exist
    sys.exit(0)
if not exist(os.path.abspath(appdir)+'\\resources\\app')and exist(appdir):
    dirs=[]
    for i in os.listdir(appdir):
        if exist(os.path.abspath(os.path.join(appdir,i))+'\\resources\\app'):
            dirs+=[i]
    else:
        error('No any GitHub Desktop here :(')  # Not exist target dir
        sys.exit(0)
    appdir=os.path.abspath(os.path.join(appdir,sorted(dirs,reverse=True)[0]))
    del dirs
if not exist(appdir):
    error('Not exist: '+appdir)  # Not exist target dir
    sys.exit(0)

# Basically Verified
appdir=os.path.abspath(appdir+'\\resources\\app')
resdir=os.path.abspath(os.getcwd())
jsdir0=appdir+'\\main.js'
jsdir1=appdir+'\\renderer.js'
jsdir0b=jsdir0+'.bak'
jsdir1b=jsdir1+'.bak'
extra=['\\static\\cherry-pick-intro.png']
if restore: # Restore
    if not(exist(jsdir0b)and exist(jsdir1b)):
        print(error("Can't find js files to restore.")) # Not the right target dir
    else:
        # Verified, Restore
        mode('Restore')
        with alive_progress.alive_bar(3,title=CYAN('[info] Restoring'),spinner=None,enrich_print=False) as bar:
            bar()
            ok(os.path.split(jsdir0)[-1])
            copy(jsdir0b,jsdir0)
            bar()
            ok(os.path.split(jsdir1)[-1])
            copy(jsdir1b,jsdir1)
            bar()
            for f in extra:
                ok(f)
                copy(appdir+f+'.bak',appdir+f)
        ok('Restore finished.')
else:   # Patch
    if not(exist(jsdir0)and exist(jsdir1)):
        print(error("Can't find js files to patch."))  # Not the right target dir
    else:
        if sum(map(lambda f:int(not exist(resdir+f)),extra))!=0:
            resdir=os.path.abspath(os.path.split(sys.argv[0])[0])   # Can't find in current dir,
        if sum(map(lambda f:int(not exist(resdir+f)),extra))!=0:    # Try py file dir
            print(error_text("Can't find extra resources."))    # Can't find resources
        else:
            # Verified, Patch
            print(title_text+'\nPatch files.\n')
            print('Target dir: '+appdir+'\nResource dir: '+resdir)

            # Backup
            print('\nBackuping...')
            if not exist(jsdir0b):
                print('  \\main.js ==> bak')
                copy(jsdir0,jsdir0b)
            if not exist(jsdir1b):
                print('  \\renderer.js ==> bak')
                copy(jsdir1,jsdir1b)
            for f in extra:
                if not exist(appdir+f+'.bak'):
                    print('  '+f+' ==> bak')
                    copy(appdir+f,appdir+f+'.bak')

            # Restore all
            print('\nRestoring...')
            print('  \\main.js <== bak')
            copy(jsdir0b,jsdir0)
            print('  \\renderer.js <== bak')
            copy(jsdir1b,jsdir1)
            for f in extra:
                print('  '+f+' <== bak')
                copy(appdir+f+'.bak',appdir+f)

            # Patch
            print('\nPatch start.')
            
            #  Copy extra files
            print('\nCopying extra files...')
            for f in extra:
                print('  '+f+' <== Translated')
                copy(resdir+f,appdir+f)
                
            #  Patch js
            print('\nTranslating js...')
            js=['','']
            with open(jsdir0,'r',encoding='utf-8')as j:js[0]=j.read()
            with open(jsdir1,'r',encoding='utf-8')as j:js[1]=j.read()
            
            import re
            w=0
            def sub(mode):
                global w,js
                if mode=='':
                    return None
                elif mode[0]=='#':
                    return None
                elif mode=='mainjs':  # main.js
                    print('  [main.js]')
                    w=0
                elif mode=='renjs': # renderer.js
                    print('  [renderer.js]')
                    w=1
                elif '>'in mode:
                    m=mode.split('>')
                    n='>'.join(m[1:])
                    m=m[0]
                    #m,n=mode.split('>')
                    if'&'in m and m[0]!='!'and'&'not in n and m[0]!='^':
                        n+='(&'+m[m.index('&')+1].upper()+')'
                    if'...'in m and m[0]!='!'and m[0]!='^':
                        n+='...'
                    if'…'in m and m[0]!='!'and m[0]!='^':
                        n+='…'
                    if m[0]!='!'and m[0]!='^':
                        x=''
                        m='"'+m+'"'
                        n='"'+n+'"'
                        nword=n
                    elif m[0]=='!':
                        x=m[0]
                        m=m[1:]
                        nword=n
                        n=eval(n)
                    else:
                        x=m[0]
                        m=m[1:]
                        nword=n
                    if x=='^'or(x!='!' and not('\\'in m or'*'in m or'?'in m)):
                        c=js[w].count(m)
                        print('  '+m+' ==> '+n+' ['+str(c)+']')
                        if not c==0:
                            js[w]=js[w].replace(m,n)
                        else:
                            print('  '+'^'*len('  '+m+' ==> '+n+' ['+str(c)+']'))
                    else:
                        c=len(re.findall(m,js[w]))
                        print('  REGEX: '+m+' ==> '+nword+' ['+str(c)+']')
                        if not c==0:
                            js[w]=re.sub(m,n,js[w])
                        else:
                            print('  '+'^'*len('  REGEX: '+m+' ==> '+nword+' ['+str(c)+']'))
                else:
                    return None
                
            a='''
mainjs
default branch>默认分支

&File>文件
New &repository…>新建储存库
Add &local repository…>添加本地储存库
Clo&ne repository…>克隆储存库
&Options…>选项
E&xit>退出

&Edit>编辑
&Undo>撤销
&Redo>恢复
Cu&t>剪切
&Copy>复制
&Paste>粘贴
Select &all>全选
&Find>查找

&View>视图
&Changes>更改内容
&History>历史记录
Repository &list>储存库列表
&Branches list>分支列表
Go to &Summary>摘要
#以下两个，js中在更下面一点
Sho&w stashed changes>显示已储存的更改
H&ide stashed changes>隐藏已储存的更改
Toggle &full screen>切换全屏
Reset zoom>重置缩放
Zoom in>放大
Zoom out>缩小
&Reload>刷新
&Toggle developer tools>开发人员工具
P&ush>推送
Force P&ush…>强制推送
Force P&ush>强制推送

&Repository>储存库
Pu&ll>拉取
&Remove…>移除
&Remove>移除
&View on GitHub>在 GitHub 上查看
!"O&pen in "(.*)"Command Prompt"\)>lambda x:'"在 "'+x.group(1)+'"命令提示符")+" 中打开(&P)"'
renjs
Command Prompt>命令提示符
mainjs
Show in E&xplorer>打开文件夹
!"&Open in "(.*)"external editor"\)>lambda x:'"在 "'+x.group(1)+'"外部编辑器")+" 中打开(&O)"'
renjs
Visual Studio Code>VS Code
Visual Studio Code (Insiders)>VS Code 测试版
IntelliJ IDEA Community Edition>IntelliJ IDEA 社区版
mainjs
Create &issue on GitHub>在 GitHub 上创建议题
Repository &settings…>储存库设置

&Branch>分支
New &branch…>新建
&Rename…>重命名
&Delete…>删除
Discard all changes…>放弃所有更改
&Stash all changes…>存储所有更改
&Stash all changes>存储所有更改
!"&Update from "[ ]?\+[ ]?p>'"从 " + p + " 更新"'
&Compare to branch>比较分支
&Merge into current branch…>合并到当前分支
Squas&h and merge into current branch…>汇聚合并到当前分支
R&ebase current branch…>变基合并到当前分支
Compare on &GitHub>在 &GitHub 上比较
Show &pull request>显示拉取请求
Create &pull request>创建拉取请求

&Help>帮助
Report issue…>报告问题
Failed opening issue creation page>无法打开问题创建页面
&Contact GitHub support…>联系 Github 支持
Failed opening contact support page>无法打开联系支持页面
Show User Guides>打开用户指南
Failed opening user guides page>无法打开用户指南页面
Show keyboard shortcuts>打开快捷键表
Failed opening keyboard shortcuts page>无法打开键盘快捷键页面
S&how logs in Explorer>打开日志文件夹
Failed opening logs directory>无法打开日志文件夹
&About GitHub Desktop>关于 GitHub Desktop

renjs
!"Press "(.*)" to exit fullscreen">lambda x:'"按 "'+x.group(1)+'" 退出全屏"'

Ok>确定
Cancel>取消
Save>保存
Close>关闭
Delete>删除
Continue>继续
Yes>是
No>否

Name>名称
Email>邮箱
Other>其他
Sign in>登入
Sign out>登出
Learn more>了解更多
Learn more.>了解更多

Check for Updates>检查更新
Quit and Install Update>退出并安装更新
Unknown update status >未知更新状态
Checking for updates…>正在检查更新
Downloading update…>正在下载更新
You have the latest version (last checked>已是最新版本 (检查于
An update has been downloaded and is ready to be installed.>更新下载完成，等待安装。
Couldn't determine the last time an update check was performed. You may be running an old version. Please try manually checking for updates and contact GitHub Support if the problem persists>无法确定上一次检查更新的时间。你可能正在运行旧版软件。如果问题仍然存在，请尝试手动检查更新，并联系 GitHub 支持
release notes>发布说明
Version >版本 
Terms and Conditions>条款与条件
License and Open Source Notices>许可与开源声明

Options>选项
Accounts>账户
Sign in to your GitHub.com account to access your repositories.>登入到 GitHub 帐户来访问你的存储库。
If you have a GitHub Enterprise or AE account at work, sign in to it to get access to your repositories.>如果你拥有 GitHub 企业版或 GitHub AE 帐户，请登入该帐户来访问你的存储库。
Unknown sign in type: >未知登入类型:
Sign in using your browser>通过浏览器登入
Continue with browser>转到浏览器
To improve the security of your account, GitHub now requires you to sign in through your browser.>为了确保账户安全，你需要通过浏览器登入 GitHub。
Your browser will redirect you back to GitHub Desktop once you've signed in. If your browser asks for your permission to launch GitHub Desktop please allow it to.>登入后，浏览器会重定向回 GitHub Desktop。请允许浏览器打开 GitHub Desktop 的请求（若是有的话）。
Enterprise address>企业网址
Unable to authenticate with the GitHub Enterprise instance. Verify that the URL is correct, that your GitHub Enterprise instance is running version 2.8.0 or later, that you have an internet connection and try again.>GitHub 企业版实例身份验证失败。请检查网址是否输入有误，实例是否支持（支持的实例版本为 ≥2.8.0），并确定你连上网了，然后再试一次。
Integrations>集成
Applications>应用程序
External editor>外部编辑器
No editors found.>无可用编辑器
Install >试试 
Shell>命令行
Git
⚠️ This email address doesn't match >⚠️ 邮箱与
, so your commits will be wrongly attributed.>不匹配，你的提交将被错误归属。
^`your ${this.props.accounts[0].endpoint===Wt()?"GitHub":"GitHub Enterprise"} account`>`你的 ${this.props.accounts[0].endpoint===Wt()?"GitHub ":"GitHub 企业版"}账号`
either of your GitHub.com nor GitHub Enterprise accounts>你的非 GitHub 账号
Default branch name for new repositories>默认分支名
Other…>其他
These preferences will edit your global Git config.>这些选项会更改全局 Git 配置
Appearance>外观
Light>简洁
The default theme of GitHub Desktop>默认主题，梦的开始
Dark>暗夜
GitHub Desktop is for you too, creatures of the night>你的主场，夜之精灵
High Contrast>高对比度
Customizable High Contrast Theme>易于分辨，可自定义
Customize:>自定义
Reset to High Contrast defaults>重置为默认配色
!"background",[ ]?"Background">'"background","背景"'
!"border",[ ]?"Border">'"border","边框"'
!"text",[ ]?"Text">'"text","文本"'
!"activeItem",[ ]?"Active">'"activeItem","选中项"'
!"activeText",[ ]?"Active Text">'"activeText","选中文本"'
System>自动
Automatically switch theme to match system theme.>跟随系统，自动切换
Prompts>提示
^"Show a confirmation dialog before...">"显示确认对话框"
Removing repositories>删除存储库
Discarding changes>放弃更改
Force pushing>强制推送
Advanced>高级
^"If I have changes and I switch branches...">"发生更改后切换了分支"
Ask me where I want the changes to go>询问如何处理
Always bring my changes to my new branch>把更改带到新的分支
Always stash and leave my changes on the current branch>暂存当前分支更改，然后切换分支
Background updates>后台刷新
Periodically fetch and refresh status of all repositories>定期获取并刷新所有存储库的状态
Allows the display of up-to-date status indicators in the repository list. Disabling this may improve performance with many repositories.>允许在存储库列表中显示最新状态标识。如果有大量储存库，关闭此功能可以提高性能。
SSH
Use system OpenSSH (recommended)>使用系统 OpenSSH (推荐)
Usage>使用情况
!"Help GitHub Desktop improve by submitting"(.*)"usage stats"\)>lambda x:'"通过发送"'+x.group(1)+'"使用情况统计信息")," 来帮助改进 GitHub Desktop"'

'''
            for x in a.split('\n'):
                if x!='':sub(x)
            
            print('Write back.')
            with open(jsdir0,'w',encoding='utf-8')as j:j.write(js[0])
            with open(jsdir1,'w',encoding='utf-8')as j:j.write(js[1])

            print('\nDone.')
            sys.exit(0)

# EOF
sys.exit(0)
