# coding=utf-8
import sys, os
from datetime import date

def printHelp():
    print('Invalid options')
    print('Usage: python/python3 publish.py [options]')
    print('--test:\t\tto publish the test index page')
    print('--production:\tto publish the production index page')

def checkDirectory():
    if 'yingxiao-fe/template/normal/' not in os.getcwd() and 'yingxiao-fe/template/festival/' not in os.getcwd():
        return False, 'Check directory failed:\n-> Script running from incorrect directory, please make sure you run this script from yingxiao-fe/template/normal(festival)/[your-template-directory]'
    else:
        return True, 'Check directory: successful'

def publish(publishType):
    pageName = 'index.html' if publishType == 'production' else 'index_for_test.html'
    templateName = os.path.basename(os.getcwd())
    templateType = 'normal' if 'normal' in os.getcwd() else 'festival'
    print('Template type: {:s}'.format(templateType))
    testIndex = '../../' + pageName
    lines = []
    try:
        # Check if template is already published
        if "template: '" + templateName + "'" in open(testIndex).read():
            return False, 'Modify ' + pageName + ' failed: template already published'
        with open(testIndex) as infile:
            for line in infile:
                version = date.today().strftime('%Y%m%d')
                if templateType == 'normal':
                    if 'type-normal' in line:
                        lines.append(line)
                        lines.append("          <li><a href=\"{{link('edit.html', { template: '" + templateName + "', source: 'meijia', ver: '" + version + "' })}}\"><img src=\"/template/normal/" + templateName + "/thumb.jpg?date=" + version + "\" alt=\"\"></a></li>\n")
                    else:
                        lines.append(line)
                else:
                    if 'type-festival' in line:
                        lines.append(line)
                        lines.append("          <li><a href=\"{{link('edit.html', { template: '" + templateName + "', source: 'meijia' })}}\"><img src=\"/template/festival/" + templateName + "/thumb.jpg\" alt=\"\"></a></li>\n")
                    else:
                        lines.append(line)
        with open(testIndex, 'w') as outfile:
            for line in lines:
                outfile.write(line)
    except Exception as e:
        return False, 'Modify ' + pageName + ' failed: {:s}'.format(str(e))
    else:
        return True, 'Modify ' + pageName + ': successful'

def printResult(result, hint):
    if (result):
        print(hint)
    else:
        print(hint)
        print('Publish for testing aborted!')

def main():
    publishTypes = []
    for arg in sys.argv:
        if arg == '--test':
            publishTypes.append('test')
        elif arg == '--production':
            publishTypes.append('production')
    if len(publishTypes) == 0:
        printHelp()
        return 9
    else:
        # Check if running from correct directory
        correctDir, hint = checkDirectory()
        printResult(correctDir, hint)
        if not correctDir:
            return 9
        # Publish
        for publishType in publishTypes:
            if publishType == 'test' or publishType == 'production':
                published, hint = publish(publishType)
                printResult(published, hint)
                if not published:
                    return 9
            elif publishType == 'production':
                print(publish(publishType))
            else:
                continue
        print('Publishing finished!')
    # else:
    #     # Publish to template/index_for_test.html
    #     published, hint = publish()
    #     printResult(published, hint)
    #     if not published:
    #         return 9
    #     print('Publish for testing finished!')

main()
