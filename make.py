# coding=utf-8
import sys, os, zipfile, shutil, fileinput, re

def printHelp():
    print('Invalid options')
    print('Usage: python/python3 make.py [options]')
    print('-n, --name:\tname to be used for the template')

def copyImages(directoryName):
    bgFound = False;
    thumbFound = False;
    wechatFound = False;
    for filename in os.listdir("."):
        if filename == "背景.jpg":
            bgFound = True;
            # os.rename(filename, filename[7:])
        if filename == "入口.jpg":
            thumbFound = True;
            # os.rename(filename, filename[7:])
        if filename == "微信.jpg":
            wechatFound = True;
            # os.rename(filename, filename[7:])
    if bgFound and thumbFound and wechatFound:
        try:
            shutil.copyfile('背景.jpg', '{:s}/thumb-bg.jpg'.format(directoryName))
            shutil.copyfile('入口.jpg', '{:s}/thumb.jpg'.format(directoryName))
            shutil.copyfile('微信.jpg', '{:s}/wx-thumb.jpg'.format(directoryName))
        except Exception as e:
            return False, 'Copy images failed: {:s}'.format(str(e))
        else:
            return True, 'Copy images: successful'
    else:
        return False, 'Copy images failed: failed to find all images'

def createDirectory(directoryName):
    if not os.path.exists(directoryName):
        try:
            os.makedirs(directoryName)
        except Exception:
            return False, 'Create directory failed: please check your permissions and make sure there is no directory with the same name'
        else:
            return True, 'Create directory ({:s}): successful'.format(directoryName)
    else:
        return False, 'Create directory failed: directory already exists'

def unzipFile(templateName):
    for filename in os.listdir("."):
        if filename.endswith('.zip'):
            unzip(filename, '{:s}/page1'.format(templateName))
            return True, 'Unzip compressed file ({:s}): successful'.format(filename)
    return False, 'Unzip compressed file failed: unable to find .zip file'

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)

def copyMp3(templateName):
    mycwd = os.getcwd()
    os.chdir("..")
    for filename in os.listdir('.'):
        if filename.endswith('.mp3'):
            try:
                shutil.copyfile(filename, '{:s}/{:s}/{:s}.mp3'.format(mycwd, templateName, templateName))
            except Exception as e:
                return False, 'Copy mp3 failed: {:s}'.format(str(e))
            else:
                return True, 'Copy mp3: successful'
            finally:
                os.chdir(mycwd) # go back to previous directory
    os.chdir(mycwd) # go back to previous directory
    return False, 'Copy mp3 failed: file not found'

def copyScript(templateName):
    print(os.getcwd())
    for filename in os.listdir('.'):
        if filename == 'publish.py':
            try:
                shutil.copy(filename, templateName)
            except Exception as e:
                return False, 'Copy publish.py failed: {:s}'.format(str(e))
            else:
                return True, 'Copy publish.py: successful'
    return False, 'Copy publish.py failed: publish.py is not found in current directory'

def generateTemplateIndex(directoryName):
    for filename in os.listdir('.'):
        if filename == 'index.html':
            try:
                with open('{:s}/index.html'.format(directoryName), "wt") as fout:
                    with open("index.html", "rt") as fin:
                        for line in fin:
                            if '<audio id=\"player\" src=\"\"' in line:
                                fout.write(line.replace('<audio id=\"player\" src=\"\"', '<audio id=\"player\" src=\"{:s}.mp3\"'.format(directoryName)))
                            else:
                                fout.write(line)
            except Exception as e:
                return False, 'Generate template index.html failed: {:s}'.format(str(e))
            else:
                return True, 'Generate template index.html: successful'
    return False, 'Generate template index.html failed: source html file not found'

def modifyPageIndex(templateName):
    pageIndex = '{:s}/page1/index.html'.format(templateName)
    lines = []
    try:
        with open(pageIndex) as infile:
            for line in infile:
                # Replace enabler.js
                if 'Enabler.js' in line:
                    line = '<script src="/template/assets/js/gwd.enabler.js"></script>\n'
                    lines.append(line)
                # Append resize script
                elif 'creativeProperties' in line:
                    widthMatch = re.search('\"minWidth\":(.+?),', line)
                    width = widthMatch.group(1)
                    heightMatch = re.search('\"minHeight\":(.+?),', line)
                    height = heightMatch.group(1)
                    line = line.replace('</body></html>', '')
                    lines.append(line)
                    lines.append("<script> var width = " + width + "; var height = " + height + "; function f2s() { var z = Math.min(window.innerWidth / width, window.innerHeight / height); var z = { x: window.innerWidth / width, y: window.innerHeight / height }; var pageWrapper = document.querySelector('.gwd-page-wrapper'); pageWrapper.style.transform = 'scale(' + z.x + ', ' + z.y + ')'; pageWrapper.style.oTransform = 'scale(' + z.x + ', ' + z.y + ')'; pageWrapper.style.webkitTransform = 'scale(' + z.x + ', ' + z.y + ')'; pageWrapper.style.mozTransform = 'scale(' + z.x + ', ' + z.y + ')'; pageWrapper.style.transformOrigin = '0 0'; pageWrapper.style.webkitTransformOrigin = '0 0'; pageWrapper.style.mozTransformOrigin = '0 0'; }; window.onresize = f2s; f2s(); </script> </body> </html>")
                else:
                    lines.append(line)
        with open(pageIndex, 'w') as outfile:
            for line in lines:
                outfile.write(line)
    except Exception as e:
        return False, 'Modify page1 index.html failed: {:s}'.format(str(e))
    else:
        return True, 'Modify page1 index.html: successful'

def printResult(result, hint):
    if (result):
        print(hint)
    else:
        print(hint)
        print('Make aborted!')

def main():
    readArg = False; # Indicate when to read next argument as template name
    templateName = None;
    for arg in sys.argv: # Get template name from arguments
        if readArg:
            templateName = arg
        elif arg == '-n' or arg == '--name':
            readArg = True;
    if templateName is None:
        printHelp()
    else:
        # Create template directory
        created, hint = createDirectory(templateName)
        printResult(created, hint)
        if not created:
            return 9
        # Copy images
        copied, hint = copyImages(templateName)
        printResult(copied, hint)
        if not copied:
            return 9
        # Copy mp3
        copied, hint = copyMp3(templateName)
        printResult(copied, hint)
        if not copied:
            return 9
        # Copy publish script file
        copied, hint = copyScript(templateName)
        printResult(copied, hint)
        if not copied:
            return 9
        # Generate template index.html
        generated, hint = generateTemplateIndex(templateName)
        printResult(generated, hint)
        if not generated:
            return 9
        # unzip compressed file to template directory
        unzipped, hint = unzipFile(templateName)
        printResult(unzipped, hint)
        if not unzipped:
            return 9
        # Modify page1 index.html
        modified, hint = modifyPageIndex(templateName)
        printResult(modified, hint)
        if not modified:
            return 9
        print('Make finished!')


main()
